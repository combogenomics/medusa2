#!/usr/bin/python
# -*- coding: utf-8 -*-

#############
# Imports   #
#############
import csv
import sys
from collections import OrderedDict
from os import uname_result

import networkx as nx
from optparse import OptionParser, OptionGroup


def oriMax(orientation_max):
    o = orientation_max
    oriRev = []
    for s in o.split('=='):
        inv = s.split(':')[0]+":"+str(int(s.split(':')[1]) * -1)
        oriRev.append(inv)
    oriRevString = oriRev[1]+"=="+oriRev[0]


    return oriRevString


def compare_cover_init(csv_row):
    #per comparare grafi sotto forma di gexf dando prima la cover e poi l'init
    print("###################################################")
    f = open(csv_row['DIR_Compare']+csv_row['Output'], "w")
    f.write("COMPARE NETWORK GEXF GRAPH\n\n")
    for key in csv_row:
        tempString=str(key)+" : "+str(csv_row[key])
        print(tempString)
        f.write(tempString+"\n")


    G1 = nx.read_gexf(csv_row['DIR_Compare']+csv_row['Grafo1'])
    G2 = nx.read_gexf(csv_row['DIR_Compare']+csv_row['Grafo2'])

    #G2 init_new è l'init contenente solo gli archi e i nodi presenti in cover per fare il confronto delle orientation
    G2_init_new = nx.Graph()

    print("Creo G2 init (G2_init_new) con gli stessi archi di G1(Cover) e ognuno con i propri attributi")
    for u,v in G1.edges:
        G2_init_new.add_edge(u,v)
        try:
            G2_init_new[u][v]['orientation_max']=G2[u][v]['orientation_max']
        except:
            fake = 0
            #print("G2["+u+"]["+v+"]['orientation_max'] NON Trovata")

    listaUguali = []
    listaOrientationG1 = []
    listaOrientationG2 = []
    listaEquivalenti = []

    for u, v in G1.edges:
        tempOri = G1[u][v]['orientation_max']
        tempOris = tempOri.split("===")
        for k in tempOris:
            listaOrientationG1.append(k)


    tempLungG1 = "Lunghezza = "+str(len(listaOrientationG1))+" Orientation G1_cover = "+str(listaOrientationG1)

    print(tempLungG1)
    f.write("\n"+tempLungG1+"\n")


    for u, v in G2_init_new.edges:
        try:
            tempOri2 = G2_init_new[u][v]['orientation_max']
            tempOris2 = tempOri2.split("===")
            #print(tempOris2)
            for k in tempOris2:
                listaOrientationG2.append(k)
        except:
            fake = 0
            #print("G2_init_new[u][v]['orientation_max'] non trovata")

    tempLungG2 = "Lunghezza = "+str(len(listaOrientationG2))+" Orientation G2_init_new = "+str(listaOrientationG2)
    tempLenEdge = "\nArchi G2_init_new = " + str(nx.number_of_edges(G2_init_new)) + "\nArchi G1_Cover = " + str(nx.number_of_edges(G1))
    print(tempLungG2+"\n"+tempLenEdge)
    f.write(tempLungG2+"\n")

    if (len(listaOrientationG1) >= len(listaOrientationG2)):
        listTempG1 = listaOrientationG1.copy()
        listTempG2 = listaOrientationG2.copy()
    else:
        f.write("\n" + "------> Inverted Orientation List - First List Smaller <------" + "\n")
        print("------> Inverted Orientation List - First List Smaller <------")
        temp = listaOrientationG1.copy()
        listaOrientationG1 = listaOrientationG2.copy()
        listaOrientationG2 = temp.copy()
        listTempG1 = listaOrientationG1.copy()
        listTempG2 = listaOrientationG2.copy()

    # UTILIZZO DEI SET INVECE DELLE LISTE
    setlistTempG1 = set(listTempG1)
    setlistTempG2 = set(listTempG2)

    if (len(listaOrientationG1) <= len(listaOrientationG2)):
        print("Lunghezza Orientation Set G1_cover = " + str(len(setlistTempG1)) + " - " + str(setlistTempG1))
        print("Lunghezza Orientation Set G2_init_new = " + str(len(setlistTempG2)) + " - " + str(setlistTempG2))
    else:
        print("Lunghezza Orientation Set G2_init_new = " + str(len(setlistTempG1)) + " - " + str(setlistTempG1))
        print("Lunghezza Orientation Set G1_cover = " + str(len(setlistTempG2)) + " - " + str(setlistTempG2))

    listTempG1 = list(setlistTempG1)
    listTempG2 = list(setlistTempG2)

    for elem in listTempG1:
        for elem2 in listTempG2:
            if elem == elem2:
                listaUguali.append(elem)
                listaOrientationG1.remove(elem)
                listaOrientationG2.remove(elem2)
                break

    tempUguali = "Lunghezza = " + str(len(listaUguali)) + " Uguali = "+str(listaUguali)
    print(tempUguali)
    f.write(tempUguali+"\n")


    setlistTempG1 = set(listaOrientationG1)
    setlistTempG2 = set(listaOrientationG2)
    listTempG1 = list(setlistTempG1)
    listTempG2 = list(setlistTempG2)


    for elem in listTempG1:
        for elem2 in listTempG2:
            elem2inv = oriMax(elem2)
            eleminv = oriMax(elem)
            if elem == elem2inv or eleminv == elem2:
                listaEquivalenti.append(elem)
                listaOrientationG1.remove(elem)
                listaOrientationG2.remove(elem2)
                break

    tempEq = "Lunghezza = " + str(len(listaEquivalenti)) + " Equivalenti = " + str(listaEquivalenti)
    tempErr = "Lunghezza = " + str(len(listaOrientationG1)) + " Errore = " + str(listaOrientationG1)
    tempErr1 ="Lunghezza = " + str(len(listaOrientationG2)) + " Errore = " + str(listaOrientationG2)

    print(tempEq)
    f.write(tempEq+"\n")
    print(tempErr)
    f.write(tempErr+"\n")
    print(tempErr1)
    f.write(tempErr1+"\n")


    tempString, temp1String,tempLenNodesString,tempArchiMancanti,tempNodiMancanti = None,None,None,None,None
    f.close()


def compare(csv_row):
    #per comparare grafi sotto forma di gexf
    print("###################################################")
    f = open(csv_row['DIR_Compare']+csv_row['Output'], "w")
    f.write("COMPARE NETWORK GEXF GRAPH\n\n")
    for key in csv_row:
        tempString=str(key)+" : "+str(csv_row[key])
        print(tempString)
        f.write(tempString+"\n")


    G1 = nx.read_gexf(csv_row['DIR_Compare']+csv_row['Grafo1'])
    G2 = nx.read_gexf(csv_row['DIR_Compare']+csv_row['Grafo2'])

    #numero nodi
    tempLenNodesString= "Nodi G1 = "+str(nx.number_of_nodes(G1))+"\nNodi G2 = "+str(nx.number_of_nodes(G2))
    tempLenEdgeString = "\nArchi G1 = " + str(nx.number_of_edges(G1)) + "\nArchi G2 = " + str(nx.number_of_edges(G2))
    print(tempLenNodesString, tempLenEdgeString)
    f.write(tempLenNodesString)
    f.write(tempLenEdgeString)


    #confronto nodi
    #Attenzione: se prendo 2 grafi identici e rimuovo da xml un arco, il confronto sugli archi fa notare la cosa, ma il numero di nodi rimane lo stesso
    #viceversa se rimuovo solo gli oggetti nodo, gli archi rimangono lo stesso numero e il numero di nodi viene preso dagli archi.
    #Nel caso che elimino tutti i nodi da XML viene preso in considerazione solo gli edge e vengono calcolati da essi il numero di nodi
    # ----> Far si che i nodi che sono negli edge siano gli stessi negli oggetti node in XML

    g1_nodeSet = set(nx.nodes(G1))
    g2_nodeSet = set(nx.nodes(G2))
    diffNode12 = g1_nodeSet.difference(g2_nodeSet)
    diffNode21 = g2_nodeSet.difference(g1_nodeSet)
    tempNodiMancanti = "\nNodi Mancanti in G1:" + str(diffNode12) + "\nNodi Mancanti in G2:" + str(diffNode21)
    print(tempNodiMancanti)
    f.write(tempNodiMancanti)

    #confronto archi
    g1_edgeSet = {tuple(sorted(e)) for e in G1.edges()}
    g2_edgeSet = {tuple(sorted(e)) for e in G2.edges()}
    diff12 = g1_edgeSet.difference(g2_edgeSet)
    diff21 = g2_edgeSet.difference(g1_edgeSet)
    tempArchiMancanti = "\nArchi Mancanti in G1:"+str(diff12)+"\nArchi Mancanti in G2:"+str(diff21)+"\n"
    print(tempArchiMancanti)
    f.write(tempArchiMancanti)

    # isomorfismo
#    temp1String = "\nIsomorfi = " + str(nx.is_isomorphic(G1, G2))
#    print(temp1String)
#    f.write(temp1String + "\n")

    listaUguali = []
    listaOrientationG1 = []
    listaOrientationG2 = []
    listaEquivalenti = []

    for u, v in G1.edges:
        tempOri = G1[u][v]['orientation_max']
        tempOris = tempOri.split("===")
        for k in tempOris:
            listaOrientationG1.append(k)


    tempLungG1 = "Lunghezza = "+str(len(listaOrientationG1))+" Orientation G1 = "+str(listaOrientationG1)
    print(tempLungG1)
    f.write("\n"+tempLungG1+"\n")


    for u, v in G2.edges:
        tempOri2 = G2[u][v]['orientation_max']
        tempOris2 = tempOri2.split("===")
        for k in tempOris2:
            listaOrientationG2.append(k)

    tempLungG2 = "Lunghezza = "+str(len(listaOrientationG2))+" Orientation G2 = "+str(listaOrientationG2)
    print(tempLungG2)
    f.write(tempLungG2+"\n")


    if(len(listaOrientationG1)>=len(listaOrientationG2)):
        listTempG1 = listaOrientationG1.copy()
        listTempG2 = listaOrientationG2.copy()
    else:
        f.write("\n"+"------> Inverted Orientation List - First List Smaller <------"+"\n")
        print("------> Inverted Orientation List - First List Smaller <------")
        temp = listaOrientationG1.copy()
        listaOrientationG1 = listaOrientationG2.copy()
        listaOrientationG2 = temp.copy()
        listTempG1 = listaOrientationG1.copy()
        listTempG2 = listaOrientationG2.copy()


#UTILIZZO DEI SET INVECE DELLE LISTE
    setlistTempG1 = set(listTempG1)
    setlistTempG2 = set(listTempG2)

    print("Lunghezza Orientation Set G1 = "+str(len(setlistTempG1))+" - "+str(setlistTempG1))
    print("Lunghezza Orientation Set G2 = "+str(len(setlistTempG2)) + " - " + str(setlistTempG2))

    listTempG1 = list(setlistTempG1)
    listTempG2 = list(setlistTempG2)


    for elem in listTempG1:
        for elem2 in listTempG2:
            if elem == elem2:
                listaUguali.append(elem)
                listaOrientationG1.remove(elem)
                listaOrientationG2.remove(elem2)
                break

    tempUguali = "Lunghezza = " + str(len(listaUguali)) + " Uguali = "+str(listaUguali)
    print(tempUguali)
    f.write(tempUguali+"\n")

    setlistTempG1 = set(listaOrientationG1.copy())
    setlistTempG2 =set(listaOrientationG2.copy())
    listTempG1 = list(setlistTempG1)
    listTempG2 = list(setlistTempG2)


    for elem in listTempG1:
        for elem2 in listTempG2:
            elem2inv = oriMax(elem2)
            eleminv = oriMax(elem)
            if elem == elem2inv or eleminv == elem2:
                listaEquivalenti.append(elem)
                listaOrientationG1.remove(elem)
                listaOrientationG2.remove(elem2)
                break

    tempEq = "Lunghezza = " + str(len(listaEquivalenti)) + " Equivalenti = " + str(listaEquivalenti)
    tempErr = "Lunghezza = " + str(len(listaOrientationG1)) + " Errore = " + str(listaOrientationG1)
    tempErr1 ="Lunghezza = " + str(len(listaOrientationG2)) + " Errore = " + str(listaOrientationG2)

    print(tempEq)
    f.write(tempEq+"\n")
    print(tempErr)
    f.write(tempErr+"\n")
    print(tempErr1)
    f.write(tempErr1+"\n")


    #necessario scypi installare nel repo per difference che però è un valore numerico e non ci interessa molto
    #print(nx.difference(G1,G2))

    #G1Test=nx.complete_graph(10)
    #G2Test=nx.complete_graph(20)
    #GDiff = nx.symmetric_difference(G1Test,G2Test)
    #diff =G1Test.edges() - G2Test.edges()
    #print(G1Test.edges() - G2Test.edges())
    #print(GDiff)

    tempString, temp1String,tempLenNodesString,tempArchiMancanti,tempNodiMancanti = None,None,None,None,None
    f.close()

def compareListGraph(csv_row):
    #per comparare grafi sotto forma di lista (id, peso, source,target)
    # oggetto G1_dict è un dizionario con 4 chiavi e il value è l'ordine in cui quella chiave viene trovata nella lista (se vario il value vengono differenti e anche se ho chiavi diverse)
    fl = open(csv_row['DIR_Compare'] + csv_row['Output'], "w")
    fl.write("COMPARE NETWORK List GRAPH\n\n")
    for key in csv_row:
        tempString=str(key)+" : "+str(csv_row[key])
        print(tempString)
        fl.write(tempString+"\n")

    G1 = csv_row['DIR_Compare'] + csv_row['Grafo1']
    G2 = csv_row['DIR_Compare'] + csv_row['Grafo2']

    G1_dict = {}
    count = 0
    with open(G1, newline='') as csvfile:
        tempG = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        try:
            for rowG in tempG:
                G1_dict[rowG['ID'], rowG['SOURCE'], rowG['TARGET'], rowG['WEIGHT']] = count
                #G1_dict[rowG['SOURCE'],rowG['TARGET'],rowG['WEIGHT']] = count
                count += 1
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(G1, G1.line_num, e))
    #print(G1_dict)

    G2_dict = {}
    count2 = 0
    with open(G2, newline='') as csvfile:
        tempG2 = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        try:
            for rowG2 in tempG2:
                G2_dict[rowG2['ID'], rowG2['SOURCE'], rowG2['TARGET'], rowG2['WEIGHT']] = count2
                #G2_dict[rowG2['SOURCE'], rowG2['TARGET'], rowG2['WEIGHT']] = count2
                count2 += 1
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(G2, G2.line_num, e))


    #print(G2_dict)

    tempLenGraph = "Candidate Edges G1 = " + str(len(G1_dict)) + "\nCandidate Edges G2 = " + str(len(G2_dict))
    print(tempLenGraph)
    fl.write(tempLenGraph)
    is_equal = G1_dict == G2_dict
    #il value del dizionario è l'ordine di stampa, la chiave è la quadrupla id,source,target,weight
    tempEqual= "\nDizionari uguali = "+str(is_equal)
    print(tempEqual)
    fl.write(tempEqual)

    fl.close()



def compareCCGraph(csv_row):
    fl = open(csv_row['DIR_Compare'] + csv_row['Output'], "a")
    fl.write("COMPARE CC List GRAPH\n\n")
    for key in csv_row:
        tempString=str(key)+" : "+str(csv_row[key])
        print(tempString)
        fl.write(tempString+"\n")

    G1 = csv_row['DIR_Compare'] + csv_row['Grafo1']
    G2 = csv_row['DIR_Compare'] + csv_row['Grafo2']

    G1_dict = {}
    count = 0
    with open(G1, newline='') as csvfile:
        tempG = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        try:
            for rowG in tempG:
                G1_dict[rowG['SOURCE'],rowG['TARGET']]=rowG['CC_ID']
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(G1, G1.line_num, e))
    #print(G1_dict)

    G2_dict = {}
    count2 = 0
    with open(G2, newline='') as csvfile:
        tempG2 = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        try:
            for rowG2 in tempG2:
                G2_dict[rowG2['SOURCE'], rowG2['TARGET']]=rowG2['CC_ID']
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(G2, G2.line_num, e))

######################
    #print(G2_dict)
    setCC = set()
    setCC2 = set()

    #prendo tutte le componenti connesse di G1 prendendo i value del dict
    u_valueG1 = []
    for dic in G1_dict.values():
        if int(dic) not in u_valueG1:
            u_valueG1.append(int(dic))
    #li prendo numerici e li sorto
    u_valueG1=sorted(u_valueG1)
    #li rimetto in stringa per confronti come value sui dict
    u_valueG1str =[str(tt) for tt in u_valueG1]

    #G2
    u_valueG2 = []
    for dic in G2_dict.values():
        if int(dic) not in u_valueG2:
            u_valueG2.append(int(dic))
    # li prendo numerici e li sorto
    u_valueG2 = sorted(u_valueG2)
    # li rimetto in stringa per confronti come value sui dict
    u_valueG2str = [str(tt) for tt in u_valueG2]

    listCC1, listCC2 = [],[]

    for CC in u_valueG1str:
        for key,value in G1_dict.items():
            key1int = [int(i) for i in key]
            key1 = sorted(key1int)
            if CC == value:
                setCC.add(tuple(key1))

        #qui devo confrontare il set con gli altri di G2, setCC è CC di G1
        for CC2 in u_valueG2str:
            for key, value in G2_dict.items():
                #print(int(key))
                #converto in tutti int
                key2int=[int(i) for i in key]
                key2 = sorted(key2int)
                if CC2 == value:
                    setCC2.add(tuple(key2))

            if(len(setCC.difference(setCC2))==0):
                print(CC+" mdsFile1 <--> mdsFile2 "+CC2)
                listCC1.append(CC)
                listCC2.append(CC2)
                fl.write(CC+" mdsFile1 <--> mdsFile2 "+CC2+"\n")
            setCC2.clear()
        #-------
        setCC.clear()

    print()
    for CC in u_valueG1str:
        if(CC not in listCC1):
                print("CC: "+CC+" File1 non trovata su File2(Grafo2)")

    for CC2 in u_valueG2str:
        if(CC2 not in listCC2):
                print("CC: "+CC2+" File2 non trovata su File1(Grafo1)")

    print()
    fl.close()

def compareEdgeList(csv_row):
    # per comparare grafi sotto forma di list di archi
    print("###################################################")

    for key in csv_row:
        tempString = str(key) + " : " + str(csv_row[key])
        print(tempString)

    G1 = csv_row['DIR_Compare'] + csv_row['Grafo1']
    G2 = csv_row['DIR_Compare'] + csv_row['Grafo2']

    G1_nx = nx.Graph()

    with open(G1, newline='') as csvfile:
        tempG = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        try:
            for rowG in tempG:
                G1_nx.add_edge(rowG['SOURCE'],rowG['TARGET'])
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(G1, G1.line_num, e))
    print(G1_nx.edges)

    G2_nx = nx.Graph()
    count2 = 0
    with open(G2, newline='') as csvfile:
        tempG2 = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        try:
            for rowG2 in tempG2:
                G2_nx.add_edge(rowG2['SOURCE'], rowG2['TARGET'])
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(G2, G2.line_num, e))

    print(G2_nx.edges)

    g1_edgeSet = {tuple(sorted(e)) for e in G1_nx.edges()}
    g2_edgeSet = {tuple(sorted(e)) for e in G2_nx.edges()}
    diff12 = g1_edgeSet.difference(g2_edgeSet)
    diff21 = g2_edgeSet.difference(g1_edgeSet)

    archiComuni = g1_edgeSet.intersection(g2_edgeSet)
    print("Archi Comuni = "+str(len(archiComuni))+" - "+str(archiComuni))
    tempArchiLen = "\nArchi G1: " + str(len(g1_edgeSet)) + "\nArchi G2: " + str(len(g2_edgeSet)) + "\n"
    print(tempArchiLen)
    tempArchiMancanti = "\nArchi Mancanti in G1: " + str(len(diff21)) +" - " + str(diff21) + "\nArchi Mancanti in G2:" + str(
        len(diff12)) +" - "+ str(diff12) + "\n"
    print(tempArchiMancanti)


if __name__ == "__main__":

    #-----------> Al momento Sui grafi sarebbe meglio per i confronti non portarsi le sequenze

    usage = "CompareMedusa1Medusa2.py -i settingFile.csv \n file format:\n\n" \
            "ID_Compare,TYPE_Compare,DIR_Compare,Grafo1,Grafo2,Output\n 1,graph or list,\"/home/desk/PycharmProjects/mds2tool/comparison/\",\"grafo1.gexf\",\"grafo2.gexf\",\"out1.txt\" "
    parser = OptionParser(usage=usage)

    #file di input per confronto grafi
    group1 = OptionGroup(parser, "Mandatory Arguments")
    group1.add_option("-i", "--input", dest="input",
                      help=" input file settings for comparing graph", metavar="FILE")


    (options, args) = parser.parse_args()
    if not options.input:
        parser.error('Mandatory Arguments missing')

    fileSettings = options.input
    #apertura file setting

    with open(fileSettings, newline='') as csvfile:
        temp = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        try:
            for row in temp:
                #skippa il confronto se l'id inizia con cancelletto
                if not row['ID_Compare'].startswith("#"):
                    if row['TYPE_Compare'] == 'graph':
                        compare(row)
                        print()
                    if row['TYPE_Compare'] == 'graph_cover_init':
                        compare_cover_init(row)
                        print()
                    if row['TYPE_Compare'] == 'list':
                        compareListGraph(row)
                        print()
                    if row['TYPE_Compare'] == 'listCC':
                        compareCCGraph(row)
                        rowTemp=row.copy()
                        row['Grafo1']= rowTemp['Grafo2']
                        row['Grafo2'] = rowTemp['Grafo1']
                        compareCCGraph(row)
                        print()
                    if row['TYPE_Compare'] == 'edgeList':
                        compareEdgeList(row)

        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(fileSettings, temp.line_num, e))
