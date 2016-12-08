import numpy as np

from seispy.hypocenter import accelerate
from seispy.event import Origin
from seispy.geometry import sph2geo


class Locator:
    def __init__(self, ttgrid, cfg):
        self.ttgrid = ttgrid
        self.cfg = cfg

    def locate(self, origin, P_only=False):
        # print "locating event #%d" % origin.evid
        arrivals = origin.arrivals
        if P_only:
            arrivals = tuple([arr for arr in arrivals if arr.phase == 'P'])
        if not self._check_nobs(arrivals,
                                self.cfg["min_nsta"],
                                self.cfg["min_nobs"]):
            return None
        r0, theta0, phi0, t0 = self._grid_search(arrivals)
        arrivals = self._remove_outliers(r0, theta0, phi0, t0, arrivals)
        if not self._quality_control(r0, theta0, phi0, arrivals):
            return None
        soln = self._subgrid_inversion(r0, theta0, phi0, t0, arrivals)
        if soln is None:
            return None
        else:
            r0, theta0, phi0, t0, sdobs0, arrivals0 = soln
        lat0, lon0, z0 = sph2geo(r0, theta0, phi0)
        return Origin(lat0, lon0, z0, t0,
                      arrivals=arrivals0,
                      evid=origin.evid,
                      sdobs=sdobs0,
                      author="seispy.locate")

    def _check_nobs(self, arrivals, min_nsta, min_nobs):
        stations = []
        for arrival in arrivals:
            if arrival.station.name not in stations:
                stations += [arrival.station.name]
        if len(stations) < min_nsta:
            return False
        if len(arrivals) < min_nobs:
            return False
        return True

    def _grid_search(self, arrivals):
        print "GETTING GRIDDY WITH IT NA NA NA NA NA NA NA"
        ir0, itheta0, iphi0, t0 = accelerate.grid_search(self.ttgrid, arrivals)
        print ir0, itheta0, iphi0, t0
        return self.ttgrid.nodes['r'][ir0, itheta0, iphi0],\
            self.ttgrid.nodes['theta'][ir0, itheta0, iphi0],\
            self.ttgrid.nodes['phi'][ir0, itheta0, iphi0],\
            t0

    def _subgrid_inversion(self, r, theta, phi, t, arrivals, itern=0):
        print "SUBGRID"
        r0, theta0, phi0, t0, arrivals0 = r, theta, phi, t, arrivals
        T = np.asarray([self.ttgrid.get_ttgradient(arrival.station.name,
                                                   arrival.phase,
                                                   r,
                                                   theta,
                                                   phi) + (1, )
                        for arrival in arrivals])
        residuals = np.asarray([arrival.time.timestamp -
                                (t + self.ttgrid.get_tt(arrival.station.name,
                                                        arrival.phase,
                                                        r,
                                                        theta,
                                                        phi))
                                for arrival in arrivals])
        rms0 = np.sqrt(np.mean(np.square(residuals)))
        delU = np.linalg.lstsq(T, residuals)[0]
        U = np.asarray([r, theta, phi, t])
        ds = np.asarray([self.ttgrid.dr,
                         self.ttgrid.dtheta,
                         self.ttgrid.dphi,
                         1])
        r, theta, phi, t = U + delU * ds
        if not self._quality_control(r, theta, phi, arrivals):
            return None
        arrivals = self._remove_outliers(r, theta, phi, t, arrivals)
        if not self._quality_control(r, theta, phi, arrivals):
            return None
        residuals = np.asarray([arrival.time.timestamp -
                                (t + self.ttgrid.get_tt(arrival.station.name,
                                                        arrival.phase,
                                                        r,
                                                        theta,
                                                        phi))
                                for arrival in arrivals])
        rms = np.sqrt(np.mean(np.square(residuals)))
        if itern >= self.cfg['max_iterations']:
            return r, theta, phi, t, rms, arrivals
        if rms > rms0:
            return r0, theta0, phi0, t0, rms0, arrivals0
        if abs(rms0 - rms) > self.cfg['convergance_threshold']:
            self._subgrid_inversion(r, theta, phi, t,
                                    arrivals,
                                    itern=itern + 1)
        return r, theta, phi, t, rms, arrivals

    def _quality_control(self, r, theta, phi, arrivals):
        if not self.ttgrid.contains(r, theta, phi):
            return False
        if not self._check_nobs(arrivals,
                                self.cfg["min_nsta"],
                                self.cfg["min_nobs"]):
            return False
        return True

    def _remove_outliers(self, r, theta, phi, t, arrivals):
        res = np.array([arrival.time.timestamp -
                        (t + self.ttgrid.get_tt(arrival.station.name,
                                                arrival.phase,
                                                r,
                                                theta,
                                                phi))
                        for arrival in arrivals])
        new_arrivals = []
        for i in range(len(arrivals)):
            arrival = arrivals[i]
            r = res[i]
            tol = self.cfg["P_residual_tolerance"]\
                if arrival.phase == 'P'\
                else self.cfg["S_residual_tolerance"]
            if abs(r) < tol:
                new_arrivals += [arrival]
        return new_arrivals


def test():
    import gazelle as gz
    import seispy as sp
    cfg = {"min_nsta": 5,
           "min_nobs": 5,
           "P_residual_tolerance": 1.0,
           "S_residual_tolerance": 2.0,
           "max_iterations": 40,
           "convergance_threshold": 0.1}
    ttgrid = sp.ttgrid.TTGrid("/home/shake/malcolcw/data/fm3d_ttimes")
    locator = Locator(ttgrid, cfg)
    db = gz.datascope.Database("/home/shake/malcolcw/sandbox/test_mt3dloc/"
                               "2013/SJFZ_2013")
    outfile = open("/home/shake/malcolcw/sandbox/test_mt3dloc/drms.out",
                   "w",
                   0)
    outfile.write("1D\t3D\n")
    for origin in db.iterate_origins():
        r, theta, phi = sp.geometry.geo2sph(origin.lat,
                                            origin.lon,
                                            origin.depth)
        if not locator.ttgrid.contains(r, theta, phi):
            continue
#        T = np.asarray([locator.ttgrid.get_ttgradient(arrival.station.name,
#                                                      arrival.phase,
#                                                      r,
#                                                      theta,
#                                                      phi) + (1, )
#                        for arrival in origin.arrivals])
        new = locator.locate(origin)
#        if new is None:
#            origin.plot(filter=(("highpass",), {"freq": 3.0}),
#                        ttgrid=ttgrid,
#                        show=False,
#                        save="/home/shake/malcolcw/sandbox/event_plots/"
#                        "nonconvergent/%03d-1D.png" % origin.evid)
#        else:
#            outfile.write("%.4f\t%.4f\n" % (origin.get_rms(ttgrid),
#                                           new.get_rms(ttgrid)))
#            origin.plot(filter=(("highpass",), {"freq": 3.0}),
#                        ttgrid=ttgrid,
#                        show=False,
#                        save="/home/shake/malcolcw/sandbox/event_plots/"
#                        "convergent/%03d-1D.png" % origin.evid)
#            new.plot(filter=(("highpass",), {"freq": 3.0}),
#                     ttgrid=ttgrid,
#                     show=False,
#                     save="/home/shake/malcolcw/sandbox/event_plots/"
#                     "convergent/%03d-3D.png" % origin.evid)
    outfile.close()

if __name__ == "__main__":
    test()
