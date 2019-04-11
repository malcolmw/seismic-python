import numpy as np
import os
import subprocess
import tempfile
from . import constants as _constants
from . import coords as _coords

FM3D_BIN = '/home/malcolmw/src/fmtomo/fm3d'


class Ray(object):
    def __init__(self, path, travel_time, phase=None, stacode=None, src_id=None, arrival_id=None):
        self.path = path
        self.travel_time = travel_time
        self.stacode = stacode
        self.src_id = src_id
        self.arrival_id = arrival_id
        self._phase = phase
        self._toa = None
        self._az = None


    @property
    def az(self):
        if self._az == None:
            drho, dtheta, dphi   = self.path[1] - self.path[0]
            self._az  = np.degrees(np.arctan2(dphi, -dtheta))
        return (self._az)


    @az.setter
    def az(self, value):
        raise (NotImplementedError('sorry, az is an immutable attribute'))


    @property
    def phase(self):
        return (None if self._phase is None else self._phase.upper())


    @phase.setter
    def phase(self, value):
        self._phase = value


    @property
    def toa(self):
        if self._toa == None:
            drho, dtheta, dphi   = self.path[1] - self.path[0]
            xyz      = self.path[:2].to_cartesian()
            dtotal   = np.sqrt(np.sum(np.square(xyz[1] - xyz[0])))
            self._toa = np.degrees(np.arccos(drho / dtotal))
        return (self._toa)


    @toa.setter
    def toa(self, value):
        raise (NotImplementedError('sorry, toa is an immutable attribute'))


def format_frechet():
    return (
        '0\n'
    )


def format_interfaces(vm):
    blob = '2\n' # Number of interfaces; always 2
    blob += f'{vm.nlambda:<4d} {vm.nphi:<4d}\n'
    blob += f'{vm.dlambda:.4f} {vm.dphi:.4f}\n'
    blob += f'{vm.lambda0:.4f} {vm.phi0:.4f}\n'
    n = vm.nlambda * vm.nphi
    i1 = vm.rho0 + (vm.nrho - 3) * vm.drho
    i2 = vm.rho0 + 2 * vm.drho
    blob += '\n'.join((str(i1) for i in range(n)))
    blob += '\n'
    blob += '\n'.join((str(i2) for i in range(n)))
    blob += '\n'
    return (blob)


def format_mode_set():
    return (
        'F\nT\nF\nF\nT\nF'
    )



def format_pgrid(vm,
                 refinement_factor=5,
                 n_refined_propgrid_cells=10):
    blob  = f'{vm.ndepth-3:9d} {vm.nlambda-4:9d} {vm.nphi-4:9d}\n'
    blob += f'{vm.ddepth:9.4f} {vm.dlat:9.4f} {vm.dlon:9.4f}\n'
    blob += f'{-(vm.depth0+1.5*vm.ddepth):9.4f} {vm.lat0+1.5*vm.dlat:9.4f} {vm.lon0+1.5*vm.dlon:9.4f}\n'
    blob += f'{refinement_factor:9d} {n_refined_propgrid_cells:9d}\n'
    return (blob)


def format_receivers(receivers):
    blob = f'{len(receivers)}\n' # Number of receivers
    for rx in receivers:
        blob += f'{-rx[2]:.4f} {rx[0]:.4f} {rx[1]:.4f}\n'
        blob += '1\n' # Number of paths to receiver; always 1
        blob += '1\n' # The source of the path; always 1
        blob += '1\n' # Number of the path in source-path list; always 1
    return (blob)


def format_source(latitude, longitude, depth):
    blob = '1\n' # Number of sources; always 1
    blob += '0\n' # Teleseism flag; always 0
    blob += f'{depth:.4f} {latitude:.4f} {longitude:.4f}\n'
    blob += '1\n' # Number of paths; always 1
    blob += '1\n' # Number of path-sections; always 1
    blob += '0 1\n' # Section definition; always direct from source to receiver
    blob += '1\n' # vtype; always 1 for P-wave
    return (blob)


def format_vgrid(vm, phase='p'):
    blob = '1 1\n' # Number of grids and vtypes; always 1
    blob += f'{vm.nrho:<4d} {vm.nlambda:<4d} {vm.nphi:<4d}\n'
    blob += f'{vm.drho:<.4f} {vm.dlambda:<.4f} {vm.dphi:.4f}\n'
    blob += f'{vm.rho0:<.4f} {vm.lambda0:<.4f} {vm.phi0:.4f}\n'
    if phase.upper() in ('P', 'VP'):
        data = vm._vp
    elif phase.upper() in ('S', 'VS'):
        data = vm._vs
    else:
        raise (ValueError(f'sorry, I didn\'t recognize phase type {phase}'))
    data = np.flip(data, axis=1)
    blob += '\n'.join(np.round(data.flatten(), 3).astype(str))
    return (blob)


def read_arrivals(filename):
    with open(filename, 'r') as infile:
        data = infile.read().split('\n')[:-1]
    arrivals = [float(line.split()[4]) for line in data]
    arrivals = list(filter(lambda arrival: arrival != -1, arrivals))
    return (arrivals)


def read_outputs(outdir):
    arrivals = read_arrivals(os.path.join(outdir, 'arrivals.dat'))
    raypaths = read_rays(os.path.join(outdir, 'rays.dat'))
    if len(arrivals) != len(raypaths):
        raise (ValueError('sorry, I don\'t understand these data files'))
    rays = [Ray(raypaths[idx], arrivals[idx]) for idx in range(len(arrivals))]
    return (rays if len(rays) > 0 else None)


def read_rays(filename):
    rays = []
    with open(filename, 'r') as infile:
        data = infile.read().split('\n')
    while len(data) > 1:
        nsec = int(data[0].split()[4])
        if nsec == 0:
            data = data[1:]
            continue
        npts = int(data[1].split()[0])
        data = data[2:]
        try:
            ray = _coords.as_left_spherical(
                list(
                    map(
                        lambda point: np.fromstring(point, sep=' '),
                        data[:npts]
                    )
                )
            ).to_spherical()
        except ValueError:
            print(ray)
            raise
        data = data[npts:]
        rays.append(ray)
    return (rays)


def pad_vm(vm):
    vm.pad(nrho=-2, ntheta=-2, nphi=-2)
    vm.pad(nrho=3, ntheta=2, nphi=2)


def in_propgrid(vm, points):
    points    = _coords.as_geographic(points)
    if points.shape == (3,):
        points = [points]
    # The depth is constrained by the interfaces.
    # An extra 0.1*vm.drho is shaved off here to remove
    # points that lie "exactly" on the interface
    depth_min = _constants.EARTH_RADIUS - (vm.rho0 + (vm.nrho - 3.1) * vm.drho)
    depth_max = _constants.EARTH_RADIUS - (vm.rho0 + 2.1 * vm.drho)
    # The latitude and longitude are constrained by the propagation grid.
    lat_min = vm.lat0 + 1.5 * vm.dlat
    lat_max = lat_min + (vm.nlat - 5) * vm.dlat
    lon_min = vm.lon0 + 1.5 * vm.dlon
    lon_max = lon_min + (vm.nlon - 5) * vm.dlon
    return (
        np.array(
            [
                 (lat_min < lat0 < lat_max)
                &(lon_min < lon0 < lon_max)
                &(depth_min < depth0 < depth_max)
                for lat0, lon0, depth0 in points
            ]
        )
    )


def write_fm3d_inputs(vm, origin, receivers, outdir, phase='p'):
    if not in_propgrid(vm, origin):
        raise (ValueError(f'sorry, origin {origin} lies outside of propagation region'))
    rx_in_propgrid = in_propgrid(vm, receivers)
    if not np.all(rx_in_propgrid):
        raise (ValueError(f'sorry, receiver(s) lies outside of propagation region\n'
                          f'{receivers[~rx_in_propgrid]}'))
    with open(os.path.join(outdir, 'frechet.in'), 'w') as outfile:
        outfile.write(format_frechet())
    with open(os.path.join(outdir, 'interfaces.in'), 'w') as outfile:
        outfile.write(format_interfaces(vm))
    with open(os.path.join(outdir, 'mode_set.in'), 'w') as outfile:
        outfile.write(format_mode_set())
    with open(os.path.join(outdir, 'propgrid.in'), 'w') as outfile:
        outfile.write(format_pgrid(vm))
    with open(os.path.join(outdir, 'receivers.in'), 'w') as outfile:
        outfile.write(format_receivers(receivers))
    with open(os.path.join(outdir, 'sources.in'), 'w') as outfile:
        outfile.write(format_source(*origin))
    with open(os.path.join(outdir, 'vgrids.in'), 'w') as outfile:
        outfile.write(format_vgrid(vm, phase=phase))


def trace_rays(vm, origin, receivers, phase):
    print(f'Tracing {phase.upper()}-wave rays for origin at '
          f'({origin[0]:.3f}, {origin[1]:.3f}, {origin[2]:6.3f})')
    cwd = os.getcwd()
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            write_fm3d_inputs(vm, origin, receivers, temp_dir, phase=phase)
            os.chdir(temp_dir)
            output = subprocess.run([FM3D_BIN], capture_output=True)
            rays = read_outputs(temp_dir)
    finally:
        os.chdir(cwd)
    return (rays)
