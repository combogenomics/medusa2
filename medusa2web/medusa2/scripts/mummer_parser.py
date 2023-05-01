import sys,logging

#######################

if __name__=='__main__':
	usage="""
	python mummer_parser.py coord_file out_file """
	args=sys.argv
	coords=args[1]
	out=args[2]

#######################

#process an input file, skip first 5 rows (header)
#and for each row scanned a mummer_hit object is created
def parse(coords_file):
	forbid={0,1,2,3,4}
	for i,l in enumerate(open(coords_file)):
		if i in forbid: continue 
		yield mummer_hit(l.strip())

def parseMinimap(paf_file):
	with open(paf_file) as f:
		for line in f:
			yield minimap_hit(line.strip())



def get_bestHits(hits,attr='covq'):
	query_contigs=set([h.query for h in hits])
	best_hits=[]
	for c in query_contigs:
		best_hit=max([h for h in hits if h.query == c],key=lambda x: float(x.__getattribute__(attr)))
		best_hits.append(best_hit)
	return best_hits

#########################
# start of experimental
#########################

def compare(x,y,attr):
	return float(x.__getattribute__(attr)) > float(y.__getattribute__(attr))

def compare2(x,y):
	return float(x.covq)*float(x.percidy) > float(y.covq)*float(y.percidy)

	
def getBestHits(coords,attr='covq',aligner=False):
	""" experimental version of get_bestHits with better performances. 
		Improvements:
			- use of generators
			- use of a dictionary for best hits:
				. key = hit.query
				. value = hit
			- use of a dictionary for hit clusters:
				. key = hit.reference
				. value = [hit1,hit2,...,hitn]
				. hits are added in order to compare the 
				"""
	best_hits={}
	if aligner == False:
		for h in parse(coords):
			if h.query not in best_hits:
				best_hits[h.query]=h
				continue
			if compare(h,best_hits[h.query],attr): best_hits[h.query]=h
	else:
		for h in parseMinimap(coords):
			if h.query not in best_hits:
				best_hits[h.query]=h
				continue
			if compare(h,best_hits[h.query],attr): best_hits[h.query]=h
	return best_hits.values()

def getBestHits2(hits):
	""" same as previous, but with different comparison """
	best_hits={}
	for h in parse(coords):
		if h.query not in best_hits:
			best_hits[h.query]=h
			continue
		if compare2(h,best_hits[h.query]): best_hits[h.query]=h
	yield best_hits.values()
		
#########################
# end of experimental
#########################


def get_bestHits2(hits):
	query_contigs=set([h.query for h in hits])
	best_hits=[]
	for c in query_contigs:
		best_hit=max([h for h in hits if h.query == c],key=lambda x: float(x.covq)*float(x.percidy))
		best_hits.append(best_hit)
	return best_hits

#It returns a dictionary {(key, list_of_values)} that stores the association
#between reference genoma and target genoma contigs that map on the same
#genoma reference contig.
def get_Clusters(best_hits):
	clusters={}
	for h in best_hits:
		clusters[h.reference]=clusters.get(h.reference,[])
		clusters[h.reference].append(h)	
	return clusters

def write_Clusters(clusters,out):
	out=open(out,'w')
	for cl in clusters.values():
		cl.sort(key=lambda x:int(x.rstart))
		# print '\n'.join([c.query for c in cl]),'\n'
		out.write('\n'.join([c.query for c in cl])+'\n\n')

def parse_mummer(coords):
	best_hits=getBestHits(coords,aligner=False)
	clusters=get_Clusters(best_hits)
	return clusters

def parse_minimap2(paf):
	best_hits=getBestHits(paf,aligner=True)
	clusters=get_Clusters(best_hits)
	return clusters

def parse_mummer2(coords):
	hits=parse(coords)
	best_hits=get_bestHits2(hits)
	clusters=get_Clusters(best_hits)
	return clusters
	
def do_overlap(a,b):
	'''return true if a (a1,a2) overlap with b (b1,b2)'''
	sol=	((max(a) > min(b)) and (max(a) < max(b))) or \
		((min(a) > min(b)) and (min(a) < max(b)))
	return sol
	
def doMapWithin(hit1,hit2):
	'''return true if a (a1,a2) maps within b (b1,b2) or viceversa - se a1,a2 sono inclusi in b1,b2 o viceversa'''
	#   a1 ------- a2
	#       b1--b2
	a,b=[int(hit1.rstart),int(hit1.rend)],[int(hit2.rstart),int(hit2.rend)]
	if ((max(a) > max(b)) and (min(a) < min(b))): logging.debug('%s maps within %s !!!' %(hit2.name, hit1.name))
	elif ((max(b) > max(a)) and (min(b) < min(a))): logging.debug('%s maps within %s !!!' %(hit1.name, hit2.name))
	return 
	

#######################


class mummer_hit(object):
	def __init__(self,line):
		self.qstart, self.qend, self.rstart, self.rend, self.len1, self.len2, self.percidy, \
		self.lenr, self.lenq, self.covq, self.covr, self.query, self.reference = [i for l in line.split(' | ') for i in
																				  l.split()]
		self.name = self.query
		self.weight1 = float(self.percidy)
		self.weight2 = float(self.percidy) * float(self.covq)
		self.weightNaif = 1
		if int(self.rstart) > int(self.rend):
			self.orientation = -1
		else:
			self.orientation = 1
	def distance_from(self,hit):
		a1,a2,b1,b2=int(self.rstart),int(self.rend),int(hit.rstart),int(hit.rend)
		if do_overlap([a1,a2],[b1,b2]): return 0
		distances=[a1-b1,a1-b2,a2-b1,a2-b2]
		distance=min([abs(i) for i in distances])
		return distance
	def __lt__(self, other):
		return self.name < other.name

class minimap_hit(object):
	def __init__(self,line):

		line = line.split("\t")
		self.reference = line[0]
		self.lenr = line[1]
		self.rstart = line[2]
		self.rend = line[3]
		self.strand = line[4]
		self.query = line[5]
		self.lenq =	line[6]
		self.qstart = line[7]
		self.qend = line[8]
		self.len1 =	line[9]
		self.len2 =	line[10]
		self.mappingQuality = line[11]

		self.name=self.query
		self.covq=float(int(self.len2)/int(self.lenq))
		percidy=float(self.mappingQuality)
		'''weight1 e weight2 calculated starting from percId param value (see mummer_hit class)
		   are used in order to calculate weight scheme if wscheme is not equal to 0.
		'''
		percidy = float(int(self.len1)/int(self.len2))*100
		self.weight1=percidy
		self.weight2=percidy*float(self.covq)
		self.weightNaif=1
		if self.strand.__eq__('-'):
			copyRStart = self.rstart
			self.rstart = self.rend
			self.rend = copyRStart
			self.orientation=-1
		else: self.orientation=1
	def distance_from(self,hit):
		a1,a2,b1,b2=int(self.rstart),int(self.rend),int(hit.rstart),int(hit.rend)
		if do_overlap([a1,a2],[b1,b2]): return 0
		distances=[a1-b1,a1-b2,a2-b1,a2-b2]
		distance=min([abs(i) for i in distances])
		return distance
	def __lt__(self, other):
		return self.name < other.name


#######################

if __name__=='__main__':
	clusters=parse_mummer(coords)
	#embed()
	

