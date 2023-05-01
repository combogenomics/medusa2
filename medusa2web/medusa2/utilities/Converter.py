#!/usr/bin/python
# -*- coding: utf-8 -*-

#############
# Imports   #
#############
import csv
import sys
import networkx as nx


def oriMax(orientation_max):
    o = orientation_max
    oriRev = []
    for s in o.split('=='):
        inv = s.split(':')[0]+":"+str(int(s.split(':')[1]) * -1)
        oriRev.append(inv)
    oriRevString = oriRev[1]+"=="+oriRev[0]
    return oriRevString



if __name__ == "__main__":

    G1 = nx.read_gexf('/home/desk/PycharmProjects/mds2tool/scripts/initBCEN_OG.gexf')



    for u,v in G1.edges():
        tempOri = G1[u][v]['orientation_max']
        tempOris = tempOri.split("===")
        if len(tempOris) == 1:
            if not tempOris[0].startswith(u):
                k = oriMax(tempOris[0])
                G1[u][v]['orientation_max'] = k
        else:
            count = 0
            total = ''
            for temp in tempOris:
                if not temp.startswith(u):
                    k = oriMax(temp)
                else:
                    k = temp

                if count != 0 and count != len(temp):
                    total = total + "===" + k
                else:
                    total = total + k

                count = count + 1
            G1[u][v]['orientation_max'] = total

    # nx.write_gexf(G1,'/home/desk/Desktop/TEST_PLAN_Mds1Mds2/0_StessoInitMDS1/networkBCEN_mds1_OGv2_o_py.gexf')
    nx.write_gexf(G1,'/home/desk/PycharmProjects/mds2tool/scripts/initBCEN_OG_Convert.gexf')


