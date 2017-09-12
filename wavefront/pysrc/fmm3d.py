from . import fmm3dlib

core = fmm3dlib.core
init = fmm3dlib.initialize

class RaySection(object):
    def __init__(self, recID, srcID, rayID, secID, npts, points):
        self.recID = recID
        self.srcID = srcID
        self.rayID = rayID
        self.secID = secID
        self.npts = npts
        self.points = points

class Ray(object):
    def __init__(self, recID, srcID, rayID, nsec):
        self.recID = recID
        self.srcID = srcID
        self.rayID = rayID
        self.nsec = nsec
        self.sections = []

    def add_section(self, secID, points):
        self.sections.append(RaySection(self.recID,
                                        self.srcID,
                                        self.rayID,
                                        secID,
                                        points.shape[1],
                                        points))

    def __str__(self):
        print(self.sections[0].points.shape)
        s = "%d %d %d 0 %d\n" % (self.recID,
                               self.srcID,
                               self.rayID,
                               self.nsec)
        for isec in range(self.nsec):
            s += "%d %d F F\n" % (self.sections[isec].npts, 0)
            for ipt in range(self.sections[isec].npts):
                s += "%f %f %f\n" % (self.sections[isec].points[0,ipt],
                                     self.sections[isec].points[1,ipt],
                                     self.sections[isec].points[2,ipt])
        return(s)


def get_rays():
    with open("/Users/malcolcw/Desktop/rays.dat", "w") as outf:
        rays = []
        for srcID in range(1, core.get_nsources() + 1):
            #print("source #%d" % srcID)
            for recID in range(1, core.get_nreceivers() + 1):
                nrays = core.get_nrays(recID)
                #print("    treceiver #%d - %d rays" % (recID, nrays))
                for rayID in range(1, nrays + 1):
                    nsec = core.get_nsections(recID, rayID)
                    ray = Ray(recID, srcID, rayID, nsec)
                    print("RAYID %d ray" % rayID)
                    #print("        ray #%d - %d sections" % (rayID, nsec))
                    #print("            travel time: %f" % core.get_ray_arrival_time(recID, rayID))
                    for secID in range(1, nsec + 1):
                        npts = core.get_npoints(recID, rayID, secID)
                        #print("            section #%d - %d points" % (secID, npts))
                        points = core.get_ray_section(recID, rayID, secID, npts)
                        ray.add_section(secID, points)
                        #outf.write(print(str(ray)))
                    rays.append(ray)
    return(rays)
