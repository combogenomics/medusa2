#!/usr/bin/env python

import string


def check_sequence(line: string):  # allowed characters: ATCGN
   good_sequency=0;
   if line[0] != ">":
    for c in line:
            if c.upper()=="A" or c.upper()=="T" or c.upper()=="C" or c.upper()== "G" or c.upper()=="N" or c =="\n":
                continue
            else:
                return 1
   if good_sequency ==0:
    return 0

def checkId(line: string):
       id = line.split("\n")
       return id[0]