import numpy as np
import os
from . import constants as _constants


class Ray(object):
    def __init__(self, path, stacode=None, src_id=None, arrival_id=None):
        self.path = path
        self.stacode = stacode
        self.src_id = src_id
        self.arrival_id = arrival_id
        self._init_toa_and_az()


    def _init_toa_and_az(self):
        drho, dtheta, dphi   = self.path[1] - self.path[0]
        xyz      = self.path[:2].to_cartesian()
        dtotal   = np.sqrt(np.sum(np.square(xyz[1] - xyz[0])))
        self.toa = np.degrees(np.arccos(drho / dtotal))
        self.az  = np.degrees(np.arctan2(dphi, -dtheta))


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
    blob  = f'{vm.ndepth-4:9d} {vm.nlambda-4:9d} {vm.nphi-4:9d}\n'
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


#def read_raypaths(filename, arrivals):
#    rays = []
#    with open(filename, 'r') as infile:
#        for i in range(len(arrivals)):
#            infile.readline()
#            npts = int(infile.readline().split()[0])
#            path = seispy.coords.as_left_spherical(
#                [[float(v) for v in infile.readline().split()] for i in range(npts)]
#            ).to_spherical()
#            rays.append(
#                Ray(
#                    path,
#                    stacode=arrivals[i].stacode,
#                    arrival_id=arrivals[i].arrival_id
#                )
#            )
#    return (rays)
#
#
def pad_vm(vm):
    vm.pad(nrho=-2, ntheta=-2, nphi=-2)
    vm.pad(nrho=3, ntheta=2, nphi=2)


def write_fm3d_inputs(vm, origin, receivers, outdir):
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
        outfile.write(format_vgrid(vm))

##########################################################
# This code is for checking grid fitting...
#%matplotlib ipympl
#import matplotlib.pyplot as plt
#import numpy as np
#import seispy
#vm = seispy.velocity.VelocityModel('/home/malcolmw/proj/shared/velocity/White_et_al_2019a/White_et_al_2019a.regular.npz',
#                              fmt='npz')
#vm.pad(nrho=3, ntheta=2, nphi=2)
#vm.pad(nrho=-2, ntheta=-2, nphi=-2)
#vg = np.meshgrid(
#    np.linspace(float(vm.theta0), float(vm.theta0 + (vm.ntheta-1) * vm.dtheta), vm.ntheta),
#    np.linspace(float(vm.rho0), float(vm.rho0 + (vm.nrho-1) * vm.drho), vm.nrho)
#)
#pg = np.meshgrid(
#    np.linspace(float(vm.theta0+1.5*vm.dtheta), float(vm.theta0+1.5*vm.dtheta + (vm.ntheta-4) * vm.dtheta), 
#                vm.ntheta-3),
#    np.linspace(seispy.constants.EARTH_RADIUS-float(vm.depth0+1.5*vm.ddepth), 
#                seispy.constants.EARTH_RADIUS-float(vm.depth0+1.5*vm.ddepth + (vm.ndepth-4) * vm.ddepth),
#                vm.ndepth-3)
#)
#i1 = vm.rho0 + (vm.nrho - 3) * vm.drho
#i2 = vm.rho0 + 2 * vm.drho
#plt.close('all')
#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
#ax.scatter(vg[0].flatten(), vg[1].flatten(), 
#    s=10,
#    marker='o'
#)
#ax.scatter(pg[0].flatten(), pg[1].flatten(), 
#    s=10,
#    marker='x'
#)
#ax.axhline(i1, color='r', linestyle='--')
#ax.axhline(i2, color='r', linestyle='--')
##########################################################