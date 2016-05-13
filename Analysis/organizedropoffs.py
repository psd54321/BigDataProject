#!/usr/bin/python

import sys
import os
import json
import csv

def OrganizeDropoffs():
    yearlydropoffs = {}
    inputfile = "evening.txt"
    flp = open(inputfile, 'rU')
    for line in flp:
        key, value = line.strip().split('\t')
        try: 
            keys=key.split(',')
            print'%s'%(keys)
            year = keys[0]
            neighborhood = keys[1]
            count = int(value)

        except:
            continue

        if neighborhood not in yearlydropoffs:
            yearlydropoffs[neighborhood] = {}
            yearlydropoffs[neighborhood][year] = count
        else:
            if year not in yearlydropoffs[neighborhood]:
                yearlydropoffs[neighborhood][year] = count
    
    return yearlydropoffs
        

if __name__ == '__main__':

    organizeddropoffs = OrganizeDropoffs()

    json_file = open('eveningdropoffs.json', 'w+')
    json.dump(organizeddropoffs, json_file)
