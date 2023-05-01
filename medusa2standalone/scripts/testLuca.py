from collections import OrderedDict
import collections
import networkx as nx
import hashlib as ha

def take3(elem):
    return str(elem[2])

def take4(elem):
    return elem[3]

edgelist = [
    ('1', '3', {'id':10, 'weight':550}),
    (1, 4, {'id':6,'weight': 74}),
    (1, 5, {'id':9, 'weight': 3659}),
    (1, 2, {'id':100, 'weight': 36})

]

network='/home/desk/Desktop/TEST_PLAN_Mds1Mds2/3_Cover/BCEN_Cover_Compare/networkBCEN_mds1_cover.gexf'
network = nx.read_gexf(network)
network.remo
print(network['10389']['1115'])




################################### sort per peso
'''dictWeigth={}
for u,v,c in G.edges(data=True):
#    print(u,v,c)
    #(u,v,id,weight) = (u,v,G.get_edge_data(u,v)['id'],G.get_edge_data(u,v)['weight'])
    dictWeigth.update({c['id'] : ((u,v) , c['weight'])})

listaWeigth = sorted(dictWeigth.items(), key= lambda x: x[1][1])

ordered = collections.OrderedDict()
print(listaWeigth)
for temp in listaWeigth:
    ordered[temp[0]]=temp[1][0]

candidateReverse = OrderedDict(reversed(list(ordered.items())))
print(candidateReverse)




################################### sort per id lessicografico e poi per peso
d= {}

for u,v,c in G.edges(data=True):
#    print(u,v,c)
    #(u,v,id,weight) = (u,v,G.get_edge_data(u,v)['id'],G.get_edge_data(u,v)['weight'])
    d.update({c['id'] : ((u,v) , c['weight'])})

print(d)
lista = sorted(d.items(), key= lambda x: str(x[0]))

#print(lista)
h = collections.OrderedDict()
#####
for k in lista:
    h[k[0]]=k[1:]

#print(h)

lista2 = sorted(h.items(), key= lambda x: x[1][0][1])

candidateEdges=collections.OrderedDict()

for candidate in lista2:
    candidateEdges[candidate[0]]=candidate[1][0][0]

print(candidateEdges)
candidateReverse = OrderedDict(reversed(list(candidateEdges.items())))

print(candidateReverse)

	per medusa_lib
		d = {}
		for u, v, c in G.edges(data=True):
			d.update({c['id']: ((u, v), c['weight'])})

		#print(d)
		lista = sorted(d.items(), key=lambda x: str(x[0]))
		# print(lista)
		h = collections.OrderedDict()
		#####
		for k in lista:
			h[k[0]] = k[1:]
		# print(h)
		lista2 = sorted(h.items(), key=lambda x: x[1][0][1])
		candidateEdgesTemp = collections.OrderedDict()
		for candidate in lista2:
			candidateEdgesTemp[candidate[0]] = candidate[1][0][0]
		#print(candidateEdges)
		candidateEdges = OrderedDict(reversed(list(candidateEdgesTemp.items())))
'''