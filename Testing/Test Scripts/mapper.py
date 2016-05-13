#!/usr/bin/env python
import sys
sys.path.append('.')
import matplotlib
matplotlib.use('Agg')
from matplotlib.path import Path
from rtree import index as rtree
import numpy, shapefile, time

def findNeighborhood(location, index, neighborhoods):
    match = index.intersection((location[0], location[1], location[0], location[1]))
    for a in match:
        if any(map(lambda x: x.contains_point(location), neighborhoods[a][1])):
            return a
    return -1

def readNeighborhood(shapeFilename, index, neighborhoods):
    sf = shapefile.Reader(shapeFilename)
    for sr in sf.shapeRecords():
        if sr.record[1] not in ['New York', 'Kings', 'Queens', 'Bronx']: continue
        paths = map(Path, numpy.split(sr.shape.points, sr.shape.parts[1:]))
        bbox = paths[0].get_extents()
        map(bbox.update_from_path, paths[1:])
        index.insert(len(neighborhoods), list(bbox.get_points()[0])+list(bbox.get_points()[1]))
        neighborhoods.append((sr.record[3], paths))
    neighborhoods.append(('UNKNOWN', None))

def parseInput():
    for line in sys.stdin:
        line = line.strip('\n')
        values = line.split(',')
        if len(values)>1 and values[0]!='VendorID': 
            yield values

def mapper():
    index = rtree.Index()
    neighborhoods = []
    readNeighborhood('ZillowNeighborhoods-NY.shp', index, neighborhoods)
    agg = {}
    for values in parseInput():
        try:
            pickup_location = (float(values[9]), float(values[10]))
            p2 = float(values[9])
            p3 = float(values[10])
            loc = []    
            loc.append(p2)
            loc.append(p3)  
            dropoff = values[2]
            dt = datetime.strptime(dropoff, '%Y-%m-%d %H:%M:%S')
            year = dt.year
            month = dt.month
            day = dt.weekday()
            hr = dt.hour

        except:
            pass


        if p2 == 0 and p3 == 0:
            pass
        else:
            if day == 3:
                if hr >= 20:
                    pickup_neighborhood = findNeighborhood(pickup_location, index, neighborhoods)
                    if pickup_neighborhood!=-1:
                        agg[pickup_neighborhood] = agg.get(pickup_neighborhood, 0) + 1
                else:
                    pass
            elif day == 4 or day == 5:
                if hr >= 0 and hr <= 3:
                    pickup_neighborhood = findNeighborhood(pickup_location, index, neighborhoods)
                    if pickup_neighborhood!=-1:
                        agg[pickup_neighborhood] = agg.get(pickup_neighborhood, 0) + 1
                elif hr >= 20:
                    pickup_neighborhood = findNeighborhood(pickup_location, index, neighborhoods)
                    if pickup_neighborhood!=-1:
                        agg[pickup_neighborhood] = agg.get(pickup_neighborhood, 0) + 1
                else:
                    pass
            elif day == 6:
                if hr >= 0 and hr <= 3:
                    pickup_neighborhood = findNeighborhood(pickup_location, index, neighborhoods)
                    if pickup_neighborhood!=-1:
                        agg[pickup_neighborhood] = agg.get(pickup_neighborhood, 0) + 1
                else:
                    pass
            else:
                pass

    for item in agg.iteritems():
        print '%s\t%s' % (neighborhoods[item[0]][0], item[1])

if __name__=='__main__':
    mapper()
