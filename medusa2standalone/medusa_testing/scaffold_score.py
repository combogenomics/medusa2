import networkx as nx
from IPython import embed

def parse_mapping(f):
	G=nx.Graph()
	G2=nx.Graph()
	lines=[l.strip().split() for l in open(f)]
	for i,t in enumerate(lines):
		if i == len(lines)-1: break
		if len(t) != 5: continue
		if len(lines[i+1]) != 5: continue
		u,v=t[0],lines[i+1][0]
		ori='%s:%s_%s:%s' %(u,t[-1],v,lines[i+1][-1])
		G.add_edge(u,v,orientation=ori)
	return G

def convert_orientations(e,ori_list):
	''' convert elements of a list i.e. a:1,b:-1 to b:1,a:-1 '''
	n1,n2=e
	ori_new=[]
	for l in ori_list:
		if l[0].split(':')[0] != n1:
			n1,v1,n2,v2=[i for j in l for i in j.split(':')]
			v1,v2=int(v1)*-1,int(v2)*-1
			l=['%s:%s' %(n2,v2),'%s:%s' %(n1,v1)]
		ori_new.append(l)
	return ori_new	

def convert_orientation_string(ori_string):
	""" convert orientation string to the complementary one 
		i.e. '9517:-1_9693:1' to '9693:-1_9517:1' """
	l=ori_string.split('&')[0].split('_')
	n1,v1,n2,v2=[i for j in l for i in j.split(':')]
	v1,v2=int(v1)*-1,int(v2)*-1
	l=['%s:%s' %(n2,v2),'%s:%s' %(n1,v1)]
	out='_'.join(l)
	return out


def get_ok_orientations(s,max_ori):
	l=s.split('_')
	n1,v1,n2,v2=[i for j in l for i in j.split(':')]
	e=n1,n2
	lista=max_ori.split('__')
	for l in lista:
		if l == s: return True
	for l in convert_orientations(e,[i.split('_') for i in lista]):
		l='_'.join(l)
		if l == s: return True
	return False

def get_right_edges(G,G2):
	""" G2 has the right edges. Fxn extract edges from G that are in G2"""
	same_edges,different_edges=set(),set()
	for e in G.edges():
		n1,n2=e
		if G2.has_edge(n1,n2): same_edges.add(e)
		else: different_edges.add(e)
	return same_edges,different_edges
	
def write_report(out):
	out=open(out,'w')
	out.write('total number of joins : %s' %total_joins)
	out.write('number of misplacements: %s (%s%s)' %(total_misplace,misplace_perc,"%"))
	out.write('number of incorrect orientations: %s (%s%s)' %(total_disori,disori_perc,"%"))
	out.close()

def AddEdgeFromScaffold(G,scaffold,inverse=False):
	for i,t in enumerate(scaffold):
		if i == len(scaffold)-1: break		
		u,v=t,scaffold[i+1]
		if not inverse: ori='%s_%s' %(u,v)
		else: ori='%s:%s_%s:%s' %(u.split(':')[0],int(u.split(':')[1])*-1,v.split(':')[0],int(v.split(':')[1])*-1)
		u,v=u.split(':')[0],v.split(':')[0]
		G.add_edge(u,v,orientation=ori)
	return 

def ComputeInverseGraph(G):
	G2=nx.Graph()
	for e in G.edges():
		n1,n2=e
		ori=G[n1][n2]['orientation']
		ori_new=convert_orientation_string(ori)
		G2.add_edge(n1,n2,orientation=ori_new)
	return G2

def scaffold_scoring(scaffold):
	# declare global variables
	global total_joins # total number of edges
	global total_misplace # total number of wrong placements
	global total_disori # total number of wrong orientations
	# for each scaffold:
	G=nx.Graph()
	scaffold=scaffold.strip().split()
	AddEdgeFromScaffold(G,scaffold) # transform the scaffold into a chain graph
	total_joins= total_joins + len(G.edges()) # add the number of edges to total_joins
	right_ones,misplaced=get_right_edges(G,G2)
	visited_edges=set()
	total_misplace+= len(misplaced)
	# set a leaf as starting node
	from_=get_leaves(G)[0]
	chosen_way,check,to_=None,False,None
	misoriented=set()
	while True:
		# print from_
		# if you are arriving from a node, set the old destination as starting node (else do nothing)
		if to_ != None: from_=to_
		to_=None
		# iterate over edges starting from the starting node
		edges=nx.edges_iter(G,from_)
		for edge in edges:
			to_pick=None
			# pick the un-visited edge, if all are visited, signal ends of while-True cycle
			inverse_edge=(edge[1],edge[0])
			if (edge in visited_edges) or (inverse_edge in visited_edges): continue
			else:
				to_pick=edge
				break
		if to_pick == None: break
		to_=edge[-1]
		# visit the edge
		visited_edges.add(edge)
		# if edge in misplaced, skip it
		if (edge in misplaced) or (inverse_edge in misplaced): continue
		n1,n2=from_,to_
		if chosen_way!=None:
			# if edge orientation is wrong, add the edge to misoriented, reset the chosen_way and go to the next one
			if G[n1][n2]['orientation'] != chosen_way[n1][n2]['orientation']:
				misoriented.add(edge)
				chosen_way=None
				continue
			# else... do nothing!
			else: pass
		else:
			# choose a "way" that match the edge orientation
			if G[n1][n2]['orientation'] == G2[n1][n2]['orientation']:
				chosen_way=G2
				continue
			elif G[n1][n2]['orientation'] == G3[n1][n2]['orientation']:						
				chosen_way=G3
				continue
			# if nothing match the edge orientation, add the edge to misoriented, and go to the next one
			else:
				misoriented.add(edge)
				continue
	# add misoriented to global variable and finish task
	total_disori=len(misoriented) + total_disori
	return

def get_leaves(G):
	leaves=[n for n in nx.degree(G) if nx.degree(G)[n]==1]	
	return leaves

if __name__ == '__main__':
	import sys
	usage=''' python scaffold_score.py order_file mapping_file '''
	args=sys.argv
	try: input1,input2=args[1],args[2]
	except:
		print(usage)
		sys.exit()
	print('loading mapping file',input2)
	G2=parse_mapping(input2)
	G3=ComputeInverseGraph(G2)
	print('loading order file',input1)
	total_joins,total_misplace,total_disori=0,0,0
	scaffolds=[l.strip().split() for l in open(input1)]
	for scaffold in open(input1): scaffold_scoring(scaffold)
	
	misplace_perc=total_misplace/float(total_joins)
	misplace_perc=round(misplace_perc,4)
	#total_disori=results['negative']
	disori_perc=total_disori/float(total_joins - total_misplace)
	disori_perc=round(disori_perc,4)

	print('total number of joins :',total_joins)
	print('number of misplacements: %s (%s%s)' %(total_misplace,misplace_perc,"%"))
	print('number of incorrect orientations: %s (%s%s)' %(total_disori,disori_perc,"%"))
	write_report(input1+'_scaffold_score')
