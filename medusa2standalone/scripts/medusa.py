	#!/usr/bin/python

"""
MeDuSa: A draft genome scaffolder that uses multiple
reference genomes in a graph-based approach
"""
import multiprocessing
import netcon_mummer
from medusa_lib import *
import logging, os
from optparse import OptionParser,OptionGroup
import time
import multiprocessing_lib
import sys



#################
# Opt parsing   #
#################
if __name__ == "__main__":

	logo = """

 /$$      /$$               /$$                            /$$$$$$ 
| $$$    /$$$              | $$                           /$$__  $$
| $$$$  /$$$$ /$$$$$$  /$$$$$$$/$$   /$$ /$$$$$$$ /$$$$$$|__/  \ $$
| $$ $$/$$ $$/$$__  $$/$$__  $| $$  | $$/$$_____/|____  $$ /$$$$$$/
| $$  $$$| $| $$$$$$$| $$  | $| $$  | $|  $$$$$$  /$$$$$$$/$$____/ 
| $$\  $ | $| $$_____| $$  | $| $$  | $$\____  $$/$$__  $| $$      
| $$ \/  | $|  $$$$$$|  $$$$$$|  $$$$$$//$$$$$$$|  $$$$$$| $$$$$$$$
|__/     |__/\_______/\_______/\______/|_______/ \_______|________/
                                                                   

"""

	#print(logo)

	usage=""" 



python %prog [options]
	"""

	def outGraphCallback1(option, opt_str, value, parser):
		# Used with option --g (graph)
		# scallback=outGraphCallback1, write scaffolding network and path using a prefix of the output directory
		if value == None: value = ''
		else: value += '_'
		setattr(parser.values, option.dest, value)

	parser = OptionParser(usage=usage)

	# mandatory
	# Target genome to be scaffolded
	group1 = OptionGroup(parser, "Mandatory Arguments")
	group1.add_option("-i", "--input", dest="target",
					  help=" target genome to be scaffolded ", metavar="FILE")

	# directory containing all reference genomes to be compared (file .fna.inp)
	# es. /home/desk/PycharmProjects/mds2tool/datasets_medusa1/BCEN/reference_genomes/Burkholderia_cenocepacia_H111_uid180971.fna.inp
	group1.add_option("-f", "--files", dest="comparison_dir",
					  help=" DIR where the comparison genomes are located ", metavar="DIR")

	parser.add_option_group(group1)
	# optional
	group2 = OptionGroup(parser, "Optional Arguments")
	# output directory for scaffolds.agp and scaffold.fasta
	group2.add_option("-o", "--output_dir", dest="output_dir",default=None,help="""
						write output to DIR. If unset Medusa will generate a new directory formatted using local time as it follows: ./DDMMYYYY.HHMMSS/""", metavar="DIR")

	group2.add_option("-a","--alignerMinimap2", dest="aligner", action="store_true", default=False,
					  help=" Use Minimap2 as aligner, default is MUMmer ")

	group2.add_option("--verboseMUMmer", dest="verbose", action="store_true",default=False,
					  help=" print to STDOUT the information given by MUMmer ")

	#edges with same scores, introduces randomness
	group2.add_option("-r", "--random", dest="random", action="store_true",default=False,
	                  help="allow for random choice when best edges have the same score. This might lead to variable results!")

	#weight scheme, basically uses weightScheme2
	group2.add_option("-w", "--weight", dest="weightScheme2", action="store_true",default=False,
	                  help=" allow for sequence similarity based weighting scheme. May lead to better results.")

	#skip mapping step, mummer files will be search in specified directory, file .coords and .delta for each reference genoma
	group2.add_option("-s", "--skipMapping", dest="skipMap",default=None,
	                  help=" Skip the mapping step. MUMmer output files will be searched in DIR. Option -m will be ignored ",metavar = "DIR")

	#writes XML graph in output directory, specifying filename (except for export to verify)
	group2.add_option("-g", "--graph", dest="outGraph", metavar="PREFIX",action="callback",callback=outGraphCallback1,
	                  help=""" write scaffolding network and path covers using the prefix FILE in the output directory.
					  Without any prefix, names will have a generic one """)

	#distance between couples of contig, 100NS = 100 nucletoditi,
	group2.add_option("-d", "--distance", dest="distance", action="store_true",default=False,
	                  help=""" allow for the estimation of distance between pairs of contigs 
								based ond the reference genome(s): in this case the scaffolded contigs
								will be separated by a number of N characters equal to the estimate. 
								The estimated distances are also saved in the <targetGenome>_distanceTable file.
								By default, the scaffolded contigs are separated by 100 Ns. """)

	group2.add_option("-c","--cleanUp",dest="cleanUp",action="store_true",default=False,
						help="clean temporary files (mummer files and graphs)")

	#number threads to specify
	group2.add_option("-t","--threads",dest="threads",default=1,
					  help="number of threads for multiprocessing")


	group2.add_option("-v","--verbosity",dest="logLevel",type=int,default=2,
					  help="set the logger verbosity level to 0,1,2 or 3 (no log,warning,info,debug)")

	group2.add_option("--inputGraph",dest="inputGraph",default=None,
					  help="""resume analysis from a previous scaffolding graph. The option `-f` will be ignored.""")


	parser.add_option_group(group2)

	(options, args) = parser.parse_args()
	if not options.target or not options.comparison_dir:
		parser.print_help()
		parser.error('Mandatory Arguments missing')


	##########
	# Logger #
	##########

	logging_level = [logging.ERROR,logging.WARNING,logging.INFO,logging.DEBUG][options.logLevel]
	logger = logging.getLogger(__name__)
	#logging.basicConfig(level=logging_level,format='[%(asctime)s] %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M:%S',handlers=[
    #    logging.FileHandler("debug.log"),
    #    logging.StreamHandler()
    #])

	logging.basicConfig(level=logging_level, format='[%(asctime)s] %(levelname)-8s %(message)s',
						datefmt='%m-%d %H:%M:%S', handlers=[
			logging.FileHandler("debug.log"),
			logging.StreamHandler()
		])


	########
	# Main #
	########
	#print("Number of cpu : ", multiprocessing.cpu_count())
	start=time.time()
	print("start")

	wd = options.output_dir
	if wd == None: wd = time.strftime("./%d%m%y.%H%M%S/")
	target,comparison_dir,wd = map(os.path.abspath,[options.target,options.comparison_dir,wd])

	#File and directory checks, if not present one to be generated using timestamp

	logging.info(greenText('Phase 0: checking the inputs...\n'))
	logging.info('Working directory is [%s]...' %wd)
	checkExistence(target)
#	logging.info('Input File: '+target+' --- Sha256: '+hashFile(target))
	checkExistence(comparison_dir)
	logging.info(greenText('Input files found'))

	#Mummer output directory check, where file .coords e .delta are located
	coords = []
	coordsDir = getMummerOutDir(wd)

	## do MUMmer for each pair
	logging.info(greenText('Phase 1: mapping contigs to reference genome(s)\n'))
	#if -s skipMap option is not present and no one inputgraph is provided, mapping has to be performed

	if options.skipMap == None and options.inputGraph == None:
		#process reference genomes .fna.inp files to perform the compare
		comparisons = [os.path.join(comparison_dir,f) for f in os.listdir(comparison_dir) if os.path.join(comparison_dir,f) != target]
		#logging.info(comparisons)

 		#debug mode logging
		if(logging.DEBUG):
			for f in comparisons:
				logging.debug('Comparison File: ' +f)
				#logging.debug('Sha256: ' + hashFile(f))

		n = len(comparisons)
		if n >= 1: logging.info('A total of %s reference genomes have been found! Mapping the contigs...\n' %str(n))
		else:
			logging.error(redText('No files have been found in %s... please change your input and retry' %comparison_dir))
			sys.exit()

		#change directory on mummer output directory
		os.chdir(coordsDir)

		if options.aligner == False:
			iterable_aligner_args = [(
						(target,c),
						{'verbose':options.verbose,'outputDir':options.output_dir,
						'threads':options.threads,'logging_info':'File number %s: %s' %(i+1,c),
						'fxn':runMummer}
					) for i,c in enumerate(comparisons)]
		else:
			iterable_aligner_args = [(
				(target, c),
				{'verbose': options.verbose, 'outputDir': options.output_dir,
				 'threads': options.threads, 'logging_info': 'File number %s: %s' % (i + 1, c),
				 'fxn': runMinimap2}
			) for i, c in enumerate(comparisons)]

		coords = multiprocessing_lib.poolWrapper(int(options.threads), iterable_aligner_args)

		afterAlign = time.time()
		#print(afterAlign)
		#print("1 - Tempo Allineamento:\t" + str(afterAlign - start))


	else:
		if options.inputGraph == None:
			#if input graph is not present but skipmap option selected, .coords previously generated are used
			coordsDir = os.path.abspath(options.skipMap)
			logging.info(greenText('Option -s (--skipMap) selected. MUMmer .coords files will be searched in %s' %coordsDir))
			checkExistence(coordsDir)
			if options.aligner==False:
				coords = [os.path.join(coordsDir,f) for f in os.listdir(coordsDir) if f.endswith('.coords')]
			else:
				coords = [os.path.join(coordsDir,f) for f in os.listdir(coordsDir) if f.endswith('.paf')]
		else:
			if options.skipMap != None and options.inputGraph != None:
				#if skipMap option is selected and (.gexf xml) inputgraph is selected
				logging.info(yellowText('\nOptions -s (--skipMap) and --inputGraph were selected... --skipMap will be ignored!'))
			logging.info(greenText('\nOption --inputGraph selected... will directly analyse the scaffolding graph %s' %options.inputGraph))
			providedGraph = os.path.abspath(options.inputGraph)
			checkExistence(providedGraph)

	beforeScaffoldGraph = time.time()
	#print(beforeScaffoldGraph)


	## from MUMmer to network
	readNet = True
	try: Scaffolding_graph = providedGraph
	#providedGrph is not null only if skipMap option has been valued and
	#an inputGraph has been provided.
	except:
		readNet = False
		logging.info(greenText('Phase 2: parse mummer output(s) and create a scaffolding graph'))
		logging.warning(yellowText('This step is very time-consuming...'))

		#Create scaffolding graph inserting one node for each contig
		Scaffolding_graph = netcon_mummer.initialize_graph(target)
		if len(coords) >= 1: logging.info('A total of %s .coords/paf files have been found! Adding network edges...\n' %str(len(coords)))
		else:
			logging.error(redText('No files have been found in %s... please change your input and retry' %comparison_dir))
			sys.exit()
		#for each row of each coords file create an object for the best_hits dictionary, if 2 rows have "query/name" choose the best one based on covg parameter

		netcon_mummer.coords2graph(coords,Scaffolding_graph,distanceEstimation=options.distance,altWeightScheme=options.weightScheme2, aligner=options.aligner)#,out='/home/desk/PycharmProjects/mds2tool/scripts/network')
	# from network 2 scaffold

	#print(Scaffolding_graph.edges)

	#prova prendendo lo stesso grafo xml

	#Scaffolding_graph = read_gexf("network_orig_java");
	#Scaffolding_graph = read_gexf("network_orig_java");

	#print(nx.is_isomorphic(Scaffolding_graph,Scaffolding_graph2))

	afterScaffoldGraph = time.time()
	#print(afterScaffoldGraph)
	#print("2 - Tempo Creazione Scaffoldgraph:\t"+str(afterScaffoldGraph-beforeScaffoldGraph))


	logging.info(greenText('Phase 3: from network to scaffolds\n'))
	scaffolder = Scaffolder()
	outScaffoldsFileName = os.path.abspath(os.path.join(wd,'scaffolds'))
	scaffolder.job(Scaffolding_graph,outScaffoldsFileName,target,readNet=readNet,distanceEstimation=options.distance)

	exitTime = time.time()
	#print("5 - Tempo Totale Esecuzione:\t" + str(exitTime - start))

	#os.system('ls -l')

	#bash pipe_testing_benchmark.sh ../ scripts / outputBCEN / scaffolds.fasta.. / datasets_medusa / BCEN / Burkholderia_target.fna.. / medusa_testing / AllTargets / bcen.mapping


	# export results
	if options.cleanUp:
		logging.info(greenText('Optional: cleaning up output directory'))
		cleanUp(coordsDir)
	if options.outGraph != None:
		logging.info(greenText('Optional: producing output graphs'))
		prefix = os.path.join(wd,options.outGraph) #'/home/desk/PycharmProjects/mds2tool/scripts/outputBCEN/'
		scaffolder.exportGraphs(prefix)

	#logging.info(greenText('Phase 4: exporting results'))

	############
	#  TODOS   #
	############


