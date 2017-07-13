import numpy as np

class FaultCollection(object):
    def __init__(self, infile):
        inf = open(infile)
        self.data = np.array([
                                np.array([[float(coord) for coord in pair.split()]
                                 for pair in chunk.strip().split("\n")
                                ])
                             for chunk in inf.read().split(">")
                             ])
        inf.close()

    def subset(self, latmin, latmax, lonmin, lonmax):
        cond1 = lambda coords: latmin <= coords[1] <= latmax and\
                               lonmin <= coords[0] <= lonmax
        cond2 = lambda segment: np.any([cond1(coords) for coords in segment])
        return(np.asarray(list(filter(cond2, self.data))))
