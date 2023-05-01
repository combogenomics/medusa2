from mummer_parser import *
from medusa_lib import *
import os, logging
import networkx as nx
import Bio.SeqIO.FastaIO
from optparse import OptionParser, OptionGroup

######################################

if __name__ == '__main__':
    usage = """ %prog [options]
	"""
    ############ 'python netcon_mummer.py mapping_dir query_genome gexf_out [wscheme] [testing]'
    parser = OptionParser(usage=usage)
    # mandatory
    group1 = OptionGroup(parser, "Mandatory Arguments")
    group1.add_option("-i", "--input", dest="query_genome",
                      help="target genome to be scaffolded", metavar="FILE")
    group1.add_option("-f", "--files", dest="mapping_dir",
                      help="DIR where the comparison genomes are stored", metavar="DIR")
    parser.add_option_group(group1)
    group1.add_option("-o", "--output", dest="out",
                      help="write graph to FILE", metavar="FILE")
    # optional
    group2 = OptionGroup(parser, "Optional Arguments")
    group2.add_option("-w", "--weightingscheme", dest="scheme", action="store_true", default=False,
                      help="use a weighting scheme based on sequence similarity")
    group2.add_option("-t", "--testing", dest="testing", action="store_true", default=False,
                      help="outputs a pkl object for testing [OLD]")
    group2.add_option("-d", "--distanceEstimation", dest="gap", default=0,
                      help="choose how to compute gap length: 0 fixed distance (100bp) [default], 1 mean, 2 median, 3 most similar")
    parser.add_option_group(group2)
    (options, args) = parser.parse_args()
    if not options.query_genome or not options.mapping_dir or not options.out:
        parser.print_help()
        parser.error('Mandatory Arguments missing')
    query_genome, mapping_dir, out, scheme, testing, gap = options.query_genome, options.mapping_dir, options.out, options.scheme, options.testing, int(
        options.gap)
    if not mapping_dir.endswith('/'): mapping_dir += '/'


######################################
# create a list of edges in the form of list of 2 elements (contig_target_1, contig_target_2)
# It exists an edge between these two contig exactly because contig_target_1 and contig_target_2
# map on the same contig of genoma reference.
def sort_(clusters):
    edges = []
    for cl in clusters.values():
        if len(cl) == 1: continue
        cl.sort(key=lambda x: int(x.rstart))
        for i in range(len(cl) - 1):
            edges.append((cl[i], cl[i + 1]))
    edges.sort()
    return edges


def update_edges_(G, Edge):
    """ old function """
    u, v, distance, orientation, weight, seqSimilarity = Edge.name1, Edge.name2, Edge.distance, Edge.orientation, Edge.weight, Edge.seqSimilarity
    w = G.get_edge_data(u, v, {'weight': 0})['weight'] + weight
    d = G.get_edge_data(u, v, {'distance': 0})['distance'] + distance
    o = G.get_edge_data(u, v, {'orientation': []})['orientation']
    s = G.get_edge_data(u, v, {'seqSim': []})['seqSim'] + [seqSimilarity]
    o.append(orientation)
    G.add_edge(u, v, weight=w, distance=d, orientation=o)


def update_edges(G, Edge):
    u, v, distance, orientation, weight, seqSimilarity = Edge.name1, Edge.name2, Edge.distance, Edge.orientation, Edge.weight, Edge.seqSimilarity
    # print(str(u)+";"+str(v)+";"+str(weight))
    if G.has_edge(u, v):
        G[u][v]['weight'] += weight
        G[u][v]['distance'] += [distance]
        G[u][v]['orientation'] += [orientation]
        G[u][v]['seqSim'] + [seqSimilarity]
    else:
        G.add_edge(u, v, weight=weight, distance=[distance], orientation=[orientation], seqSim=[seqSimilarity])
        # print(G[u][v])


def compute_distances(G, method=0, outlier=1):
    """ Estimate the distance for each edge """

    import numpy as np
    skip = method == 0
    for u, v in G.edges():
        if not skip:
            distances = np.array(G[u][v]['distance'])
            seqSims = np.array(G[u][v]['seqSim'])
            if method == 1:
                dist = distanceEstimation_mean(distances, outlier)
            elif method == 2:
                dist = distanceEstimation_median(distances, outlier)
            elif method == 3:
                dist = distanceEstimation_MSH(distances, seqSims, outlier)
            else:
                dist = distanceEstimation_mean(distances, outlier)
        else:
            dist = 100
        G[u][v]['distance'] = dist
        G[u][v]['seqSim'] = ''


def distanceEstimation_mean(dist_list, method=1):
    """ Estimate the distance between two contigs, by computing the
		average of all distances found for these in the reference
		genomes. A method for outlier detection is used in order to
		obtain reliable mean."""

    # print "using mean..."
    import numpy as np
    v = np.array(dist_list)
    if method == 1:
        mask = madBasedOutlier(v)
    else:
        mask = percentileBasedOutlier(v)
    distance = v[~mask].mean()
    return int(distance)


def distanceEstimation_median(dist_list, method=1):
    """ As the mother function, except that it uses the median instead
		of the mean."""

    # print "using median..."
    import numpy as np
    v = np.array(dist_list)
    return int(np.median(v))


# try to remove outlier detection?
# if method == 1: mask=madBasedOutlier(v)
# else: mask=percentileBasedOutlier(v)
# distance=np.median(v[-mask])
# return distance

def distanceEstimation_MSH(dist_list, seqSim_list, method=1):
    """ As the mother function, except that it uses the most similar
		hit's distance."""

    # print "using most similar hit..."
    import numpy as np
    similarities, v = np.array(seqSim_list), np.array(dist_list)
    # should remove outlier detection here
    if method == 1:
        mask = madBasedOutlier(v)
    else:
        mask = percentileBasedOutlier(v)
    distance = v[np.where(max(similarities))][0]
    return int(distance)


def madBasedOutlier(points, thresh=3.5):
    """ return outliers based on median-absolute-deviation (MAD)
		This performs better on small data samples (<20).
		Require numpy object."""

    import numpy as np
    np.seterr(divide='ignore', invalid='ignore')
    # from IPython import embed
    if len(points.shape) == 1: points = points[:, None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median) ** 2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)
    modified_z_score = 0.6745 * diff / med_abs_deviation
    # if med_abs_deviation == 0: embed()
    return modified_z_score > thresh


def percentileBasedOutlier(data, threshold=95):
    """ return outliers based on percentiles
		This performs better on big data samples (>20).
		Require numpy object."""

    import numpy as np
    diff = (100 - threshold) / 2.0
    minval, maxval = np.percentile(data, [diff, 100 - diff])
    return (data < minval) | (data > maxval)


# create the graph whose nodes are genoma target contigs,
# # at the end of this method graph has only nodes.
def initialize_graph(genome):  # genome path burkholdria_target.fna sotto datasets_medusa1
    import networkx as nx
    from Bio.SeqIO import parse
    logging.info('Instanciating scaffolding network for [%s] ...' % genome)
    G = nx.Graph()

    #with open(genome) as handle:
    #    for title, seq in FastaTwoLineParser(handle):
    #        print("%s = %s..." % (title, seq[:3]))

    with open(genome) as handle:
        for c in Bio.SeqIO.FastaIO.FastaIterator(handle):
            id_, length = c.id, len(c.seq)
            G.add_node(id_, length=length)
    #contigs = parse(genome, 'fasta')
    #for c in contigs:
    #    id_, length = c.id, len(c.seq)
    #    G.add_node(id_, length=length, seq=c.seq)
    numbNodes = len(G.nodes())
    if numbNodes == 0:
        logging.error(redText('Could not find contigs in %s, please check your input and retry' % genome))
        sys.exit()
    logging.info(greenText('Success! A total of %s nodes have been included' % numbNodes))
    return G


def iterate(handle):
    """Parse the file and generate SeqRecord objects."""
    for title, sequence in Bio.SeqIO.FastaIO.FastaTwoLineParser(handle):
        try:
            first_word = title.split(None, 1)[0]
        except IndexError:
            assert not title, repr(title)
            # Should we use SeqRecord default for no ID?
            first_word = ""
        from Bio import SeqRecord
        from Bio import Seq
        yield SeqRecord(Seq(sequence), id=first_word, name=first_word,description=title)





def _force_alphabet(record_iterator, alphabet):
    """Iterate over records, over-riding the alphabet (PRIVATE)."""
    # Assume the alphabet argument has been pre-validated
    given_base_class = _get_base_alphabet(alphabet).__class__
    for record in record_iterator:
        if isinstance(_get_base_alphabet(record.seq.alphabet), given_base_class):
            record.seq.alphabet = alphabet
            yield record
        else:
            raise ValueError(
                "Specified alphabet %r clashes with "
                "that determined from the file, %r" % (alphabet, record.seq.alphabet)
            )



def adjust_orientations(G):
    id_ = 0

    for e in G.edges():
        n1, n2 = e
        #print(n1,n2)
        #print(G[n1][n2]['orientation'])
        G[n1][n2]['orientation'] = convert_orientations(e, G[n1][n2]['orientation'])
        #print(G[n1][n2]['orientation'])
        max_count = G[n1][n2]['orientation'].count(max(G[n1][n2]['orientation'],
                                                       key=lambda x: G[n1][n2]['orientation'].count(x)))
        # conta quante volte appare nella lista G[n1][n2][orientation] l'elemento che appare
        # più volte - orientamento più frequente
        G[n1][n2]['orientation_max'] = list(
            {tuple(i) for i in G[n1][n2]['orientation'] if G[n1][n2]['orientation'].count(i) == max_count})  # ???????

        # costruisce una lista di tuple ciascuna delle quali è relativa all'elemento i-esimo di G[n1][n2][orientation]
        # che occorre max_count volte
        # orientation_max lista con A:1 B:1 e A:1 B:-1 , spesso lista lunga 1 con una tupla
        # se con piu tuple a parimerito ne voglio tutte
        # data la lista di duple voglio la tupla piu presente, se ce ne sono + di una a parimerito le voglio tutte
        G[n1][n2]['orientation_max'] = '==='.join(['=='.join(i) for i in G[n1][n2]['orientation_max']])
        l = G[n1][n2]['orientation']
        # verificare se usata la freq counts
        # counts = {'_'.join(i):l.count(i)/float(len(l)) for i in l}
        G[n1][n2]['orientation'] = ''
        G[n1][n2]['id'] = id_
        id_ += 1


# edges=sorted(G.edges(), key=lambda x: G[x[0]][x[1]]['orientation_max'])
# for e in edges:
# n1,n2=e[:2]
# G[n1][n2]['id']=id_
# id_+=1
# embed()

def format_orientation_string(hit1, hit2):
    orientations = ['%s:%s' % (hit1.name, hit1.orientation), '%s:%s' % (hit2.name, hit2.orientation)]
    # orientations.sort()
    return orientations



def coords2graph(inputs, G, out=None, testing=False, altWeightScheme=False, distanceEstimation=0, aligner=False ):
    scheme, gap = altWeightScheme, distanceEstimation
    #print(inputs)
    inputs.sort()
    #print(inputs)
    for coord in inputs:
        #print('using input', coord)
#        logging.debug(coord + " --- " + hashFile(coord))
        logging.info(greenText('parsing %s' % coord))
        # prende il file coords, per ogni riga crea un oggetto per il dict best_hits, se 2 righe hanno la stessa "query/name" prende la migliore in base alla covg
        # una volta popolato best hits (es. file coord 1000 righe, best_hits 900) crea dei cluster in base alla h.reference (id parlante con pipe)
        # a questo punto per gli edges prima ordina i componenti dei cluster in base al RSTART e poi prende solo i cluster con > 1 mummer_hits
        # siamo sul file coord,i nodi sono in contig, gli edge sono i collegamenti tra contig in base al file .coords


        if aligner == False:
            clusters = parse_mummer(coord)
        else:
            clusters = parse_minimap2(coord)


        edges = sort_(clusters)

        for e in edges:
            if not testing:
                update_edges(G, Edge(*e, wscheme=scheme))
            else:
                update_edges(G, Edge(*e, wscheme=scheme))
    logging.info('adjusting orientations...')

    #for ee in G.edges:
    #    print(ee)

    # ---------------
    # aaa = []

    # for ee in G.edges:
    #   temp = [source, target, peso] = (
    #       ee[0], ee[1], G.edges[ee[0], ee[1]]['weight'])
    #   aaa.append(temp)
    # print(ee[0], ee[1], "id=" + str(G.get_edge_data(ee[0], ee[1])['id']),
    #     "weight=" + str(G.get_edge_data(ee[0], ee[1])['weight']))

    # for temp in aaa:
    #   print(str(temp[0]) + ";" + str(temp[1]) + ";" + str(temp[2]))
    # ---------------

    adjust_orientations(G)
    # ----------

    # aaa = []

    # for ee in G.edges:
    #   temp = [source, target, id, peso] = (
    #      ee[0], ee[1], G.get_edge_data(ee[0], ee[1])['id'], G.get_edge_data(ee[0], ee[1])['weight'])
    # aaa.append(temp)
    # print(ee[0], ee[1], "id=" + str(G.get_edge_data(ee[0], ee[1])['id']),
    #      "weight=" + str(G.get_edge_data(ee[0], ee[1])['weight']))
    # aaa.sort()

    # for temp in aaa:
    #   print(str(temp[0])+";"+str(temp[1])+";"+str(temp[2])+";"+str(temp[3]))

    compute_distances(G, method=gap)
    if out != None:
        if not testing:
            try:
                nx.write_gexf(G, out)
            except:
                GTemp = G.copy()
                for n in GTemp.nodes:
                    GTemp.nodes[n]['orientation'] = GTemp.nodes[n].get('orientation', [1])[-1]
                    GTemp.nodes[n]['seq'] = str(GTemp.nodes[n]['seq'])
                nx.write_gexf(GTemp, out)
        else:
            dump(G, open(out, 'w'))


def extractUpstream(r, f, leftmost=200):
    from Bio.SeqFeature import FeatureLocation

    location = f.location
    start, end, strand = location.start, location.end, location.strand
    if strand == 1:
        start_, end_ = start - 200, start
    else:
        start_, end_ = end + 1, end + 201

    fl = FeatureLocation(start_, end_, strand)
    upstream = fl.extract(r)
    upstream.id = f.qualifiers['locus_tag'][0]
    upstream.name, upstream.description = '', ''

    id_ = 0
    for e in G.edges():
        n1, n2 = e
        G[n1][n2]['orientation'] = convert_orientations(e, G[n1][n2]['orientation'])
        max_count = G[n1][n2]['orientation'].count(max(G[n1][n2]['orientation'],
                                                       key=lambda x: G[n1][n2]['orientation'].count(x)))
        # conta quante volte appare nella lista G[n1][n2][orientation] l'elemento che appare
        # più volte - orientamento più frequente
        G[n1][n2]['orientation_max'] = list(
            {tuple(i) for i in G[n1][n2]['orientation'] if G[n1][n2]['orientation'].count(i) == max_count})  # ???????
        # costruisce una lista di tuple ciascuna delle quali è relativa all'elemento i-esimo di G[n1][n2][orientation]
        # che occorre max_count volte
        # orientation_max lista con A:1 B:1 e A:1 B:-1 , spesso lista lunga 1 con una tupla
        # se con piu tuple a parimerito ne voglio tutte
        # data la lista di duple voglio la tupla piu presente, se ce ne sono + di una a parimerito le voglio tutte
        G[n1][n2]['orientation_max'] = '==='.join(['=='.join(i) for i in G[n1][n2]['orientation_max']])
        l = G[n1][n2]['orientation']
        # verificare se usata la freq counts
        # counts = {'_'.join(i):l.count(i)/float(len(l)) for i in l}
        G[n1][n2]['orientation'] = ''
        G[n1][n2]['id'] = id_
        id_ += 1


# edges=sorted(G.edges(), key=lambda x: G[x[0]][x[1]]['orientation_max'])
# for e in edges:
# n1,n2=e[:2]
# G[n1][n2]['id']=id_
# id_+=1
# embed()

def format_orientation_string(hit1, hit2):
    orientations = ['%s:%s' % (hit1.name, hit1.orientation), '%s:%s' % (hit2.name, hit2.orientation)]
    # orientations.sort()
    return orientations


def convert_orientations(e, ori_list):
    ''' convert elements of a list i.e. a:1,b:-1 to b:1,a:-1 '''

    #--> Originale n1_, n2_ = e
    n1_, n2_ = e
    #n1_ = e

    ori_new = []
    for l in ori_list:
        if l[0].split(':')[0] != n1_:
            # print 'inverting!',l[0].split(':')[0],n1_, len(ori_list)
            n1, v1, n2, v2 = [i for j in l for i in j.split(':')]
            # se A e B sono entrambi + , guardo il genoma dopo sono sempre attaccati ma messi come B e A
            # A : 1 e B : 1 sono uguali a B : -1 e A : -1
            # se ho i ":"  nell'identificativo ho un problema
            v1, v2 = int(v1) * -1, int(v2) * -1
            l_ = ['%s:%s' % (n2, v2), '%s:%s' % (n1, v1)]
        else:
            l_ = l
        ori_new.append(l_)
    return ori_new




def extractUpstream(r, f, leftmost=200):
    from Bio.SeqFeature import FeatureLocation

    location = f.location
    start, end, strand = location.start, location.end, location.strand
    if strand == 1:
        start_, end_ = start - 200, start
    else:
        start_, end_ = end + 1, end + 201

    fl = FeatureLocation(start_, end_, strand)
    upstream = fl.extract(r)
    upstream.id = f.qualifiers['locus_tag'][0]
    upstream.name, upstream.description = '', ''


######################################

class Edge(object):
    def __init__(self, hit1, hit2, wscheme=0):
        self.name1, self.name2 = hit1.query, hit2.query
        self.distance = hit1.distance_from(hit2)
        self.seqSimilarity = hit1.weight2 + hit2.weight2  # perché usare weight2= %IDY x coverage????
        doMapWithin(hit1, hit2)  # serve solo per stampare, non ritorna un booleano????
        self.orientation = format_orientation_string(hit1, hit2)
        if wscheme == 0:
            self.weight = 1
        else:
            self.weight = self.seqSimilarity


#####################################

def testForPrune():
    """ function to profile the script """
    mapping_dir = './'
    out = 'prova.gexf'
    query_genome = 'test/Rhodobacter_target.fna'
    inputs = [f for f in os.listdir(mapping_dir) if f.endswith('.coords')]
    G = initialize_graph(query_genome)
    for coord in inputs:
        #print('using input', coord)
        clusters = parse_mummer(mapping_dir + coord)
        edges = sort_(clusters)
        for e in edges:
            if not testing:
                update_edges(G, Edge(*e, wscheme=scheme))
            else:
                update_edges(G, Edge(*e, wscheme=scheme))
    logging.info('adjusting orientations')
    adjust_orientations(G)
    compute_distances(G, method=gap)
    if not testing:
        nx.write_gexf(G, out)
    else:
        dump(G, open(out, 'w'))


######################################
import sys

if __name__ == '__main__':

    inputs = [f for f in os.listdir(mapping_dir) if f.endswith('.coords')]
    G = initialize_graph(query_genome)
    inputs.sort()
    for coord in inputs:
        #print('using input', coord)
        clusters = parse_mummer(mapping_dir + coord)
        edges = sort_(clusters)
        for e in edges:
            if not testing:
                update_edges(G, Edge(*e, wscheme=scheme))
            else:
                update_edges(G, Edge(*e, wscheme=scheme))
    print('adjusting orientations')
    adjust_orientations(G)
    compute_distances(G, method=gap)
    if not testing:
        nx.write_gexf(G, out)
    else:
        dump(G, open(out, 'w'))