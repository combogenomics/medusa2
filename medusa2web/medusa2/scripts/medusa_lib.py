import logging, sys, os

import Bio
import networkx as nx
from networkx import connected_components

import multiprocessing_lib


# general
from mummer_parser import do_overlap


def checkExistence(file_):
    if not os.path.exists(file_):
        logging.error(redText('Cannot find [%s]... please change destination and retry' % file_))
        sys.exit()


def getMummerOutDir(wd):
    outDir = wd
    if not os.path.exists(outDir): os.mkdir(outDir)
    logging.info("Mummer output files will be written in [%s]\n" % outDir)
    return outDir


def run_cmd(cmd, ignore_error=False, verbose=False):
    '''
    Run a command line command
    Returns True or False based on the exit code
    '''
    import subprocess, sys
    logging.debug('%s' % cmd)
    try:
        proc = subprocess.Popen(cmd, shell=(sys.platform != "win32"),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    except OSError as e:
        if not ignore_error: logging.error('Failed at running %s!\n%s' % (cmd, e.child_traceback))
        return False
    out = proc.communicate()
    return_code = proc.returncode
    if return_code != 0 and not ignore_error:
        logging.error(
            'Command (%s) failed w/ error %d\n\n\x1b[31m%s\x1b[0m\n' % (cmd, return_code, str(out[1].decode('utf-8'))))
        sys.exit()
    return bool(not return_code)


# seqIO parsing

def renameSeqFile(inp, new_name='renamed.fasta', tag='seq', threshold=1000, conv_table=None, loc='./'):
    """ Rename a target fasta file and its sequences. Produces a new file
     and (optionally) a conversion table. By default sequences shorter
     than 1000 are removed (see threshold option) """
    from Bio.SeqIO import parse, write
    sequences = [f for f in parse(inp, 'fasta')]
    i, renamed = 0, []
    if conv_table != None: ctable = open(loc + conv_table, 'w')
    for s in sequences:
        if len(s.seq) <= threshold: continue
        i += 1
        old_id, new_id = s.id, '%s_%s' % (tag, i)
        s.id, s.description = new_id, ''
        renamed.append(s)
        if conv_table != None: ctable.write('%s\t%s\n' % (old_id, new_id))
    write(renamed, loc + new_name, 'fasta')
    return


def convertWithCtable(file_, ctable, out):
    """ Convert the names of a fasta using a conversion table"""
    from Bio.SeqIO import parse, write
    d = {k: v for i in open(ctable) for k, v in i.strip().split()}
    sequences, renamed = [f for f in parse(file_, 'fasta')], []
    for s in sequences: s.id = d.get(s.id)
    write(sequences, out, 'fasta')
    return


# mummer

def runMummer(file1, file2, verbose, outputDir='.', **kwargs):
    """ Run nucmer aligner (required mummer to be installed) """
    import os.path as path
    fname1, fname2 = path.basename(file1), path.basename(file2)
    tag1, tag2 = fname1.split('.')[0], fname2.split('.')[0]
    prefix = "%s_%s" % (tag1, tag2)
    cmd = 'nucmer --prefix=%s %s %s' % (prefix, file1, file2)
    logging.info('running nucmer...')
    ecode = run_cmd(cmd, verbose=verbose)
    cmd = 'show-coords -lc %s > %s' % (prefix + '.delta', prefix + '.coords')
    logging.info('running show-coords...\n')
    ecode = run_cmd(cmd, verbose=verbose)
    if ecode: logging.info('Success for %s!' % file2)
    return os.path.abspath("%s.coords" % prefix)

def runMinimap2(file1, file2, verbose, outputDir='.', **kwargs):
    """ Run minimap2 aligner (required minimap2 to be installed) """
    import os.path as path
    fname1, fname2 = path.basename(file1), path.basename(file2)
    tag1, tag2 = fname1.split('.')[0], fname2.split('.')[0]
    prefix = "%s_%s" % (tag1, tag2)
    cmd = 'minimap2 %s %s > %s' % (file1, file2 , prefix+ '.paf')
    logging.info('running Minimap2...')
    ecode = run_cmd(cmd, verbose=verbose)
    if ecode: logging.info('Success for %s!' % file2)
    return os.path.abspath("%s.paf" % prefix)



class Mummer_hit(object):
    #
    def __init__(self, line):
        self.qstart, self.qend, self.rstart, self.rend, self.len1, self.len2, self.percidy, \
        self.lenr, self.lenq, self.covq, self.covr, self.query, self.reference = [i for l in line.split(' | ') for i in
                                                                                  l.split()]
        self.name = self.query
        if int(self.rstart) > int(self.rend):
            self.orientation = -1
        else:
            self.orientation = 1

    #
    def distance_from(self, hit):
        a1, a2, b1, b2 = int(self.rstart), int(self.rend), int(hit.rstart), int(hit.rend)
        if do_overlap([a1, a2], [b1, b2]): return 0
        distance = abs(min(a1 - b1, a1 - b2, a2 - b1, a2 - b2))
        return distance


# tmp files

def storeTmpFasta(dir_, file_, **rename_args):
    """ If dir_ exists, write a renamed fasta there, otherwise create
        dir and write a fasta there """
    import os
    if not os.path.exists(dir_): os.makedirs(dir_)
    rename_args['loc'] = dir_
    renameSeqFile(file_, **rename_args)
    return


def cleanUp(dir_):
    """ clean up temporary directory from mummer files """
    import os
    for i in os.listdir(dir_):
        if not (i.endswith(".coords") or i.endswith(".delta")): continue
        toRemove = os.path.join(dir_, i)
        os.unlink(toRemove)
    return


# estetic

class TestColors:
    __info__ = """ some ansi codes """
    RED = '\x1b[31m'
    GREEN = '\033[92m'
    YELLOW = '\x1b[33m'
    ENDC = '\033[0m'


def greenText(t):
    return TestColors.GREEN + t + TestColors.ENDC


def redText(t):
    return TestColors.RED + t + TestColors.ENDC


def yellowText(t):
    return TestColors.YELLOW + t + TestColors.ENDC


# scaffolding

## fnxs

def adjustNodes(G, oriDicts):
    """ set orientation of nodes in G from oriDict.
    THE RIGHT ORIENTATION IS THE LAST MEMBER OF THE RESULTING LIST """
    for oriDict in oriDicts:
        for n, v in oriDict.items():
            G.nodes[n]['orientation'] = G.nodes[n].get('orientation', []) + [v]
    return


def checkOri(current, G, dicts, prev_orientations=None):
    """ returns subdictionary for which orientations of current are consistent with
        those in G."""
    # simple version: look before. Pick a random choice if two are available.
    outs = []
    if G.nodes[current].get('orientation') is None: return dicts
    for d in dicts:
        if d[current] in G.nodes[current]['orientation']: outs.append(d)
    # break # this is used in the simple version
    # if prev_orientations:
    #	G.node[prev_orientations[0]]['orientation']=
    return outs


def oriToDict(orientation_max, current):
    """ convert an orientation string to a dict
        i.e. input: NODE1:1==NODE2:-1
            output:	[{NODE1:1,NODE2:-1}]
        when an orientation has multiple possibilities,
        it returns multiple dictionaries.
        """
    out = []
    oris = orientation_max.split('===')
    hasSameFrame = False
    if orientation_max.startswith('%s:' % current): hasSameFrame = True
    for o in oris:
        if hasSameFrame:
            d = {s.split(':')[0]: int(s.split(':')[1]) for s in o.split('==')}
        else:
            d = {s.split(':')[0]: int(s.split(':')[1]) * -1 for s in o.split('==')}
        out.append(d)
    return out


## classes

class NxEdge(object):
    def __init__(self, tuple_):
        self.u, self.v, self.d = tuple_
        self.id = self.d['id']
        self.weight = self.d['weight']


class Scaffolder(object):
    def __init__(self):
        self.version_major = 1
        self.version_minor = 0

    #
    def job(self, network, outputScaffolds, target, readNet=False, distanceEstimation=False, threads=1):
        """ wrap the steps leading from a raw scaffolding networks to the output files """
        import networkx as nx
        import copy,time
        if readNet: network = nx.read_gexf(network)

        beforeCoverCreation = time.time()
        #print(beforeCoverCreation)


        G = network.copy()
        self.G = G
        self.distanceEstimation = distanceEstimation
        self.cover, self.twins = self.greedyCover(G)
        # self.cover,self.twins = self.greedyCoverStrict(G)
        self.cleaned_cover = copy.deepcopy(self.cover)
        self.cleaned_cover.cleanOrientation()
        # embed()
        # self.cleaned_cover.addSeq(inpFastaRecords)

        afterCoverCreation = time.time()
        print("3 - Tempo creazione e pulizia Cover:\t"+str(afterCoverCreation-beforeCoverCreation))

        beforeWriteScaffold = time.time()
        #print(beforeWriteScaffold)

        self.cleaned_cover.writeScaffolds(outputScaffolds, target)

        afterWriteScaffold = time.time()
        print("4 - Tempo di scrittura Scaffold:\t"+str(afterWriteScaffold-beforeWriteScaffold))

    # TODO write short report about the scaffolds like medusa1

    #
    def greedyCover(self, G):
        from random import random
        from collections import OrderedDict
        # factor = 1. + sum(map(lambda x: x[2]['weight'], G.edges(data=True)))
        logging.info(greenText('Computing a greedy path cover...'))
        cover = Cover()
        cover.distanceEstimation = self.distanceEstimation
        cover.gaptype = "U"
        if cover.distanceEstimation: cover.gaptype = "N"
        cover.add_nodes_from(G.nodes(data=True))
        twins = {}
        for n in cover.nodes():
            #	n.setAdj()
            twins[n] = n

        enableRandom = True

        if enableRandom == True:

            candidateEdges = OrderedDict((d['id'], (u, v))
                                         for u, v, d in
                                         sorted(G.edges(data=True), key=lambda i: (i[2]['weight'], random()),
                                                reverse=False))
        else:
            candidateEdges = OrderedDict((d['id'], (u, v))
                                     for u, v, d in
                                     sorted(G.edges(data=True), key=lambda i: (i[2]['weight'], str(i[2]['id'])),
                                            reverse=False))


        # for i in range(len(candidateEdges.values()) - 1): # this seems like a check... i would avoid it
        #	if G.get_edge_data(*candidateEdges.values()[i])['weight'] < G.get_edge_data(*candidateEdges.values()[i+1])['weight']: print 'Error!' # add logger here
        popped = set()
        while len(candidateEdges) > 0:
            candidateId = next(reversed(candidateEdges))
            candidate = candidateEdges.pop(candidateId)
            logging.debug(yellowText("%s candidate edges remaining, working on candidate %s, having weight %s" \
                                     % (len(candidateEdges), candidate, str(G.get_edge_data(*candidate)['weight']))))
            # print G.get_edge_data(*candidate)['weight']
            # cover.remove_edge(*candidate)
            popped.add(candidateId)
            source, target = candidate
            if twins[source] == target: continue
            d = G[source][target]
            cover.add_edge(source, target, **d)
            ps, pt = twins[source], twins[target]
            twins[ps] = pt
            twins[pt] = ps
            for i_, n in enumerate(candidate):
                if cover.degree(n) > 1:
                    for u_, v_, d_ in G.edges(n, data=True):
                        if d_['id'] not in popped:
                            popped.add(d_['id'])
                            candidateEdges.pop(d_['id'])
                        # cover.remove_edge(u_,v_)
        logging.debug(yellowText("Remaining edges/Connected components %s/%s" % (
        len(cover.edges()), len(sorted(nx.connected_components(cover))))))
        # return cover
        return cover, twins

    #
    def greedyCoverStrict(self, G, sorting="size"):
        """ a strict python translation of Bea implementation """

        from collections import OrderedDict
        from random import random
        factor = 1. + sum(map(lambda x: x[2]['weight'], G.edges(data=True)))
        cover = Cover()
        cover.add_nodes_from(G)
        twins = {}
        for n in cover.nodes():
            #	n.setAdj()
            twins[n] = n
        candidateEdges = OrderedDict((d['id'], (u, v))
                                     for u, v, d in
                                     sorted(G.edges(data=True), key=lambda i: (i[2]['weight'] + factor, random()),
                                            reverse=True))
        for i in range(len(candidateEdges.values()) - 1):  # this seems like a check... i would avoid it
            if cover.get_edge_data(*candidateEdges.values()[i])['weight'] < cover.get_edge_data(*candidateEdges.values()[i + 1])['weight']: print
            'Error!'  # add logger here
        popped = set()
        while len(candidateEdges) > 0:
            # get the with most weighted edge
            candidateId = next(candidateEdges)
            candidate = candidateEdges.pop(candidateId)
            # print cover.get_edge_data(*candidate)['weight']
            cover.remove_edge(*candidate)
            # popped.add(candidateId)

            # be sure that you are not creating a cycle
            source, target = candidate
            if twins[source] == target: continue
            d = G[source][target]
            cover.add_edge(source, target, d)
            ps, pt = twins[source], twins[target]
            twins[ps] = pt
            twins[pt] = ps

            # finally, looking both at edge's source and target, check if the degree is greater than 1. If so, remove all the other edges from candidateEdges
            for i_, n in enumerate(candidate):
                if cover.degree(n) > 1:
                    for u_, v_, d_ in G.edges(n, data=True):
                        if d_['id'] not in popped:
                            popped.add(d_['id'])
                            candidateEdges.pop(d_['id'])
                            cover.remove_edge(u_, v_)
        print
        len(cover.edges()), len(sorted(nx.connected_components(cover)))
        # return cover
        return twins

    #
    def exportGraphs(self, output_prefix):  # TODO log written files
        """ export scaffolding graphs (initial and, if present, the cleaned one) """
        import networkx as nx
        import os
        graphs = [self.G, self.cover, self.cleaned_cover]
        paths = [os.path.join(output_prefix, i)
                 for i in ["scaffolding_graph.gexf", "cover_graph.gexf", "cleaned_cover_graph.gexf"]]
        for G, fileName in zip(graphs, paths):
            logging.info('writing graph %s' % fileName)
            try:
                nx.write_gexf(G, fileName)
            except:
                for n in G.nodes:
                    G.node[n]['orientation'] = G.node[n].get('orientation', [1])[-1]
                    G.node[n]['seq'] = str(G.node[n]['seq'])
                nx.write_gexf(G, fileName)


####################
# PER ROBE START
####################

class Cover(nx.Graph):
    #
    def __init__(self, *args, **kwargs):
        nx.Graph.__init__(self, *args, **kwargs)
        self._agpHeader = """##agp-version 2.0
# Format: object object_beg object_end part_number component_type component_id component_beg component_end  orientation
#   Gaps: object object_beg object_end part_number     N/U          gap_length   gap_type      linkage        evidence
"""

    def cleanOrientation(self, threads=1):
        """ clean the node orientation and remove edges """

        connected_components = [self.subgraph(c) for c in nx.connected_components(self)]
        #connected_components = nx.connected_component_subgraphs(self, copy=False)

        #single thread
        for cc in connected_components:
            self.tagEdgesToRemove(cc)

        #threads = len(connected_components)

        #iterable_args = [((self, cc),
        #                  {'fxn': tagEdgesToRemoveMulti})
        #                 for cc in connected_components]
        #multiprocessing_lib.poolWrapper(int(threads), iterable_args)

    # for cc in connected_components: self.tagEdgesToRemove(cc)
    # for edge in self.tagEdgesToRemove(cc): self.remove_edge(*edge)
    # end of cycle: do you still have something to do?
    #
    def addSeq(self, fasta):  # TODO REMOVE THIS
        """ add sequence to each node (contig) from `fasta` """

        from Bio.SeqIO import parse
        for cntg in parse(fasta, 'fasta'):
            self.node[cntg.id]['seq'] = cntg.seq

    #
    def writeScaffolds(self, out, target):
        """ wrapper taking advantage of generator-oriented write fxn by Bio """
        from Bio.SeqIO import write as fasta_write
        seq_generator = self.writeScaffoldsGen(out, target)
        fasta = out + ".fasta"
        records = list(seq_generator)
        fasta_write(records, fasta, "fasta")

    #
    def writeScaffoldsGen(self, out, target):
        """ write the scaffolds and .agp file """

        import Bio
        report = out + ".agp"

        #-----------
        keyToSequenceDict = {}
        with open(target) as handle:
            for c in Bio.SeqIO.FastaIO.FastaIterator(handle):
                key = c.id
                keyToSequenceDict[key] = c.seq


        #-----------

        with open(report, "w") as out_handler:
            out_handler.write(self._agpHeader)
            logging.debug(yellowText("opening a write buffer with file %s" % report))

            connected_componentsTemp = [self.subgraph(c) for c in nx.connected_components(self)]

            for i, cc in enumerate(connected_componentsTemp):
                for line in self.getConnectedComponentSequence(target, cc,keyToSequenceDict, "scaffold_%s" % i):
                    if type(line) != Bio.SeqRecord.SeqRecord: out_handler.write(line)
                seqRecord = line
                if type(seqRecord) != Bio.SeqRecord.SeqRecord: print
                "!!!!";
                pass  # TODO add some exception here (should never reach it tho)
                yield seqRecord

    #
    def getNodeOri(self, n):
        """ obtain orientation of a given node """
        if n == 'gap': return '+'
        node = self.nodes[n]
        ori = node.get('orientation', [1])[-1]
        return ori

    #
    def getNodeSeq(self, nodeInCcComponent, nodeInDict):
        """ obtain the sequence of a node """
        from Bio.Seq import Seq
        node = self.nodes[nodeInCcComponent]
        ori = node.get('orientation', [1])[-1]

        if ori == 1:
            return Seq(str(nodeInDict))
        else:
            return Seq(str(nodeInDict)).reverse_complement()

    #
    def getConnectedComponentSequence(self, target, cc, keyToSequenceDict, id_='scaffold'):
        """ obtain the sequence of a connected component by reading the nodes' sequences
        Also, report the relative position (start,end,scaffold) of each contig in a .agp file.
        Second part was inspired by github comment below:

        'Hello,
        in addition to what @ShaiberAlon mentioned, coordinates of contig x in scaffold y (start, end) would be very helpful.
        So maybe you could expand your output by a distinct and parsable (.tsv) file containing one line for each input contig:
            contig_number, contig_name, scaffold_name, contig_orientation, contig_start, contig_end
        Thanks a lot for this excellent tool!'

        """

        import networkx as nx
        from Bio.SeqRecord import SeqRecord
        from Bio.Seq import Seq
        oriMapper = {'1': '+', '-1': '-', 1: '+', -1: '-', '+': '+'}

#        keyToSequenceDict = {}
#        with open(target) as handle:
#            for c in Bio.SeqIO.FastaIO.FastaIterator(handle):
#                key = c.id
#                keyToSequenceDict[key] = c.seq

        if len(cc) == 1:
            items = list(cc.nodes().items())
            node = items[0][0]
            seq =  self.getNodeSeq(node, keyToSequenceDict[node])
            start, end = 0, len(seq)
            yield self.makeAGPInfo(node, id_, start, end, end)
            # yield map(str,[node,start,end,id_])
            yield SeqRecord(id=id_, seq=seq)

        else:
            seqOut = ''
            start, end, i = 0, 0, 0
            rootAndLeaf = []
            degree = sorted(nx.degree(cc))
            for temp in degree:
                if (temp[1] == 1):
                    try:
                        rootAndLeaf.append(int(temp[0]))
                    except:
                        rootAndLeaf.append(temp[0])
                elif (temp[1] > 2):
                    print("Degree > 2, abbiamo una Y nella comp connessa, errore costruz Cover")
            try:
                rootAndLeaf = sorted(rootAndLeaf, reverse=False)
            except:
                print("Not reversed")
                
            if (len(rootAndLeaf) == 2):
                a=0
                #print("ReL = " + str(rootAndLeaf) + "\n")
            else:
                return

            root = str(rootAndLeaf[0])
            leaf = str(rootAndLeaf[1])
            dfsList = [k for k in cc.edges]
            dfsList2 = dfsList.copy()
            dfsGood = []

            next = 0

            while (len(dfsList2) > 0):
                for ind, elem in enumerate(dfsList2):
                    if (root in elem):
                        if (elem[0] == root):
                            next = elem[1]
                        else:
                            next = elem[0]
                        dfsGood.append([root, next])
                        dfsList2.pop(ind)
                        break
                root = next
            dfs = dfsGood
#--------------------------------
            enableDFL = False
            if enableDFL == True:
                dflGood = []
                dfsGoodReverse = dfsGood.copy()
                dfsGoodReverse.reverse()
                for id, elem2 in enumerate(dfsGoodReverse):
                    dflGood.append([elem2[1], elem2[0]])

                dfs = dflGood
#-----------------------------

            #for i__, edge in enumerate(nx.dfs_edges(cc)):
            for i__, edge in enumerate(dfs):
                distance = cc.edges[edge]["distance"]
                if i == 0:
                    node1, node2 = edge

                    seq1 = self.getNodeSeq(node1, keyToSequenceDict[node1])
                    seq2 = self.getNodeSeq(node2, keyToSequenceDict[node2])

                    #seq1, seq2 = map(self.getNodeSeq, edge)
                    seqOut = seq1 + ('n' * distance) + seq2
                    end1 = start + len(seq1)
                    gapStart = end1
                    start2 = end1 + distance
                    gapEnd = start2
                    end = start2 + len(seq2)
                    #
                    ids, starts, ends, i_s = (
                    (node1, "gap", node2), (start, gapStart, start2), (end1, gapEnd, end), (1, 2, 3))
                    for t in zip(ids, starts, ends, i_s):
                        yield self.makeAGPInfo(t[0], id_, t[1], t[2], t[3], oriMapper[self.getNodeOri(t[0])])
                    i = 3
                else:
                    i += 1
                    start, end = end, end + distance
                    yield self.makeAGPInfo("gap", id_, start, end, i, oriMapper[self.getNodeOri("gap")])
                    node = edge[-1]

                    node_seq = self.getNodeSeq(node, keyToSequenceDict[node])
                    #node_seq = self.getNodeSeq(node)
                    seqOut += ('n' * distance) + node_seq
                    i += 1
                    start, end = end, end + len(node_seq)
                    yield self.makeAGPInfo(node, id_, start, end, i, oriMapper[self.getNodeOri(node)])
            yield SeqRecord(id=id_, seq=seqOut)

    #
    def makeAGPInfo(self, node, id_, start, end, counter='1', orientation='+'):
        """ build a string to be written in a .agp file """
        start += 1
        distance = end - start + 1
        gaptype = self.gaptype
        vars_ = locals()
        if node == "gap":
            myStr = "%(id_)s\t%(start)s\t%(end)s\t%(counter)s\t%(gaptype)s\t%(distance)s\tcontig\tno\talign_genus\n" % vars_
            return myStr
        #
        myStr = "%(id_)s\t%(start)s\t%(end)s\t%(counter)s\tW\t%(node)s\t1\t%(distance)s\t%(orientation)s\n" % vars_
        return myStr

    def tagEdgesToRemove(self, G):
        """ traverse the Graph G and return edges making node orientation inconsistent to be removed """

        G_ = G.copy()

#-------------------------
        rootAndLeaf = []
        degree = sorted(nx.degree(G_))
        for temp in degree:
            if (temp[1] == 1):
                try:
                    rootAndLeaf.append(int(temp[0]))
                except:
                    rootAndLeaf.append(temp[0])
            elif (temp[1] > 2):
                print("Degree > 2, abbiamo una Y nella comp connessa, errore costruz Cover")
        
        try:
            rootAndLeaf = sorted(rootAndLeaf, reverse=False)
        except:
            print("Not reversed")
            
        if (len(rootAndLeaf) == 2):
            a =0
            #print("ReL = " + str(rootAndLeaf) + "\n")
        else:
            return

        root = str(rootAndLeaf[0])
        leaf = str(rootAndLeaf[1])
        dfsList = [k for k in G_.edges]
        dfsList2 = dfsList.copy()
        dfsGood = []

        next = 0

        while (len(dfsList2) > 0):
            for ind, elem in enumerate(dfsList2):
                if (root in elem):
                    if (elem[0] == root):
                        next = elem[1]
                    else:
                        next = elem[0]
                    dfsGood.append([root, next])
                    dfsList2.pop(ind)
                    break
            root = next

        dfs = dfsGood
#------------------------------------
        enableDFL = False
        if enableDFL == True:
            dflGood =[]
            dfsGoodReverse = dfsGood.copy()
            dfsGoodReverse.reverse()
            for id, elem2 in enumerate(dfsGoodReverse):
                dflGood.append([elem2[1], elem2[0]])

            dfs=dflGood
#-----------------------------------

        #for edge in nx.dfs_edges(G_):
        for edge in dfs:
            current, nxt = edge
            ori = oriToDict(G[current][nxt]['orientation_max'], current)  #
            ori_ = checkOri(current, G, ori)
            if len(ori_) == 0:
                logging.debug("Edge %s has been tagged to be removed!" % str(edge))
                self.remove_edge(*edge)
            else:
                adjustNodes(G, ori_)


def tagEdgesToRemoveMulti(self, G, **kwargs):
    """ traverse the Graph G and return edges making node orientation inconsistent to be removed """

    G_ = G.copy()

    # -------------------------
    rootAndLeaf = []
    degree = sorted(nx.degree(G_))
    for temp in degree:
        if (temp[1] == 1):
            try:
                rootAndLeaf.append(int(temp[0]))
            except:
                rootAndLeaf.append(temp[0])
        elif (temp[1] > 2):
            print("Degree > 2, abbiamo una Y nella comp connessa, errore costruz Cover")
    
    try:
        rootAndLeaf = sorted(rootAndLeaf, reverse=False)
    except:
        print("Not reversed")
    
    
    if (len(rootAndLeaf) == 2):
        a = 0
        # print("ReL = " + str(rootAndLeaf) + "\n")
    else:
        return

    root = str(rootAndLeaf[0])
    leaf = str(rootAndLeaf[1])
    dfsList = [k for k in G_.edges]
    dfsList2 = dfsList.copy()
    dfsGood = []

    next = 0

    while (len(dfsList2) > 0):
        for ind, elem in enumerate(dfsList2):
            if (root in elem):
                if (elem[0] == root):
                    next = elem[1]
                else:
                    next = elem[0]
                dfsGood.append([root, next])
                dfsList2.pop(ind)
                break
        root = next

    dfs = dfsGood
    # ------------------------------------
    enableDFL = False
    if enableDFL == True:
        dflGood = []
        dfsGoodReverse = dfsGood.copy()
        dfsGoodReverse.reverse()
        for id, elem2 in enumerate(dfsGoodReverse):
            dflGood.append([elem2[1], elem2[0]])

        dfs = dflGood
    # -----------------------------------

    # for edge in nx.dfs_edges(G_):
    for edge in dfs:
        current, nxt = edge
        ori = oriToDict(G[current][nxt]['orientation_max'], current)  #
        ori_ = checkOri(current, G, ori)
        if len(ori_) == 0:
            logging.debug("Edge %s has been tagged to be removed!" % str(edge))
            self.remove_edge(*edge)
        else:
            adjustNodes(G, ori_)

####################
# PER ROBE END
####################
