#!/usr/bin/env python
import sys
sys.path.append('.')
import matplotlib
matplotlib.use('Agg')
from matplotlib.path import Path
from rtree import index as rtree
import numpy, shapefile, time
from datetime import datetime

def findNeighborhood(location, index, neighborhoods):
    match = index.intersection((location[0], location[1], location[0], location[1]))
    for a in match:
        if any(map(lambda x: x.contains_point(location), neighborhoods[a][1])):
            return a
    return -1

def readNeighborhood(shapeFilename, index, neighborhoods):
    sf = shapefile.Reader(shapeFilename)
    for sr in sf.shapeRecords():
        paths = map(Path, numpy.split(sr.shape.points, sr.shape.parts[1:]))
        bbox = paths[0].get_extents()
        map(bbox.update_from_path, paths[1:])
        index.insert(len(neighborhoods), list(bbox.get_points()[0])+list(bbox.get_points()[1]))
        neighborhoods.append((sr.record[6], paths))
    neighborhoods.append(('UNKNOWN', None))

def parseInput():
    for line in sys.stdin:
        line = line.strip('\n')
        if(line == '' or line == None): continue
        values = line.split(',')
        if len(values)>1 and (values[0]!='VendorID' or values[0]!='vendor_id'): 
            yield values

def mapper():
    index = rtree.Index()
    fileyear = None
    neighborhoods = ['Greenpoint','Chinatown','DUMBO-Vinegar Hill-Downtown','East Williamsburg','Hunters Point-Sunnyside-West','Lower East Side','North Side-South Side']
    gentrified = []
    readNeighborhood('geo_export.shp', index, neighborhoods)
    agg = {}
    for values in parseInput():
        try:
            dropoff_location = (float(values[9]), float(values[10]))
            d2 = float(values[9])
            d3 = float(values[10])
            p2 = float(values[5])
            p3 = float(values[6])
            dropoff = values[2]
            dt = datetime.strptime(dropoff, '%Y-%m-%d %H:%M:%S')
            year = dt.year
            month = dt.month
            day = dt.weekday()
            hr = dt.hour
            fileyear = year

        except:
            continue


        if p2 == 0 or p3 == 0 or dt is None or d2 == 0 or d3 == 0 :
            pass
        else:
            if day == 3:
                if hr >= 20:
                    dropoff_neighborhood = findNeighborhood(dropoff_location, index, neighborhoods)
                    if dropoff_neighborhood!=-1 and dropoff_neighborhood in gentrified:
                        print '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (neighborhoods[dropoff_neighborhood][0], values[3],values[4],values[5],values[6],values[7],values[8],values[9],values[10],values[11],values[15],values[17])
                else:
                    pass
            elif day == 4 or day == 5:
                if hr >= 0 and hr <= 3:
                    dropoff_neighborhood = findNeighborhood(dropoff_location, index, neighborhoods)
                    if dropoff_neighborhood!=-1 and dropoff_neighborhood in gentrified:
                        print '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (neighborhoods[dropoff_neighborhood][0],values[3],values[4],values[5],values[6],values[7],values[8],values[9],values[10],values[11],values[15],values[17])
                elif hr >= 20:
                    dropoff_neighborhood = findNeighborhood(dropoff_location, index, neighborhoods)
                    if dropoff_neighborhood!=-1 and dropoff_neighborhood in gentrified:
                        print '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (neighborhoods[dropoff_neighborhood][0], values[3],values[4],values[5],values[6],values[7],values[8],values[9],values[10],values[11],values[15],values[17]) 
                else:
                    pass
            elif day == 6:
                if hr >= 0 and hr <= 3:
                    dropoff_neighborhood = findNeighborhood(dropoff_location, index, neighborhoods)
                    if dropoff_neighborhood!=-1 and dropoff_neighborhood in gentrified:
                        print '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (neighborhoods[dropoff_neighborhood][0],values[3],values[4],values[5],values[6],values[7],values[8],values[9],values[10],values[11],values[15],values[17])
                else:
                    pass
            else:
                pass

if __name__=='__main__':
    mapper()
