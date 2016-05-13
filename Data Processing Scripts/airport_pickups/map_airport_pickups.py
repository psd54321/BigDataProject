#!/usr/bin/env python
import sys, csv
sys.path.append('.')
import matplotlib
matplotlib.use('Agg')
from matplotlib.path import Path
from rtree import index as rtree
import numpy, shapefile, time
from datetime import datetime


class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Polygon:
    def __init__(self,points):
        self.points = points
        self.nvert = len(points)

        minx = maxx = points[0].x
        miny = maxy = points[0].y
        for i in xrange(1,self.nvert):
            minx = min(minx,points[i].x)
            miny = min(miny,points[i].y)
            maxx = max(maxx,points[i].x)
            maxy = max(maxy,points[i].y)

        self.bound = (minx,miny,maxx,maxy)

    def contains(self,pt):
        firstX = self.points[0].x
        firstY = self.points[0].y
        testx = pt.x
        testy = pt.y
        c = False
        j = 0
        i = 1
        nvert = self.nvert

        while (i < nvert) :
            vi = self.points[i]
            vj = self.points[j]
            
            if(((vi.y > testy) != (vj.y > testy)) and (testx < (vj.x - vi.x) * (testy - vi.y) / (vj.y - vi.y) + vi.x)):
                c = not(c)

            if(vi.x == firstX and vi.y == firstY):
                i = i + 1
                if (i < nvert):
                    vi = self.points[i];
                    firstX = vi.x;
                    firstY = vi.y;
            j = i
            i = i + 1
        return c

    def bounds(self):
        return self.bound


polyJFK = Polygon([Point(-73.7712,40.6188),Point(-73.7674,40.6233),Point(-73.7681,40.6248),Point(-73.7657,40.6281),Point(-73.7472,40.6356),Point(-73.7468,40.6422),Point(-73.7534,40.6469),Point(-73.7544,40.6460),Point(-73.7745,40.6589),Point(-73.7858,40.6628),Point(-73.7891,40.6634),Point(-73.7903,40.6655),Point(-73.8021,40.6658),Point(-73.8146,40.6632),Point(-73.8210,40.6638),Point(-73.8244,40.6621),Point(-73.8248,40.6546),Point(-73.8212,40.6469),Point(-73.7848,40.6302),Point(-73.7899,40.6223),Point(-73.7831,40.6203),Point(-73.7782,40.6274),Point(-73.7731,40.6235),Point(-73.7738,40.6193),Point(-73.7712,40.6188)])


#LaGuardia Polygon
polyLG = lpoly = Polygon([Point(-73.8888,40.7662),Point(-73.8898,40.7736),Point(-73.8843,40.7751),Point(-73.8852,40.7808),Point(-73.8795,40.7812),Point(-73.8788,40.7842),Point(-73.8751,40.7827),Point(-73.8711,40.7864),Point(-73.8673,40.788),Point(-73.868,40.7832),Point(-73.8716,40.7808),Point(-73.8534,40.773),Point(-73.8557,40.7697),Point(-73.8505,40.7673),Point(-73.85,40.7645),Point(-73.8529,40.7637),Point(-73.856,40.7676),Point(-73.8594,40.7659),Point(-73.8625,40.7654),Point(-73.8672,40.7693),Point(-73.8732,40.7714),Point(-73.8871,40.7697),Point(-73.8866,40.7665),Point(-73.8888,40.7662)])

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
        values = line.split(',')
        if len(values)>1 and (values[0]!='VendorID' or values[0]!='vendor_id'): 
            yield values


def mapper():
    index = rtree.Index()
    neighborhoods = []
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

        except:
            continue

        if p2 == 0 or p3 == 0 or dt is None or d2 == 0 or d3 == 0:
            pass
        else:
            pt = Point(p2, p3)
            if polyJFK.contains(pt):
                dropoff_neighborhood = findNeighborhood(dropoff_location, index, neighborhoods)
                if dropoff_neighborhood!=-1:
                    agg[dropoff_neighborhood] = agg.get(dropoff_neighborhood, 0) + 1
                else:
                    pass
            elif polyLG.contains(pt):
                dropoff_neighborhood = findNeighborhood(dropoff_location, index, neighborhoods)
                if dropoff_neighborhood!=-1:
                    agg[dropoff_neighborhood] = agg.get(dropoff_neighborhood, 0) + 1
                else:
                    pass
            else:
                pass
    for item in agg.iteritems():
        print '%s\t%s' % (neighborhoods[item[0]][0], item[1])

if __name__=='__main__':
    mapper()
