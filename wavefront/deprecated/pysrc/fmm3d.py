from . import _fmm3d
import f90wrap.runtime
import logging

def run(sources, nsources, receivers, nreceivers, outrays, outtts):
    """
    run(sources, nsources, receivers, nreceivers, outrays, outtts)
    
    
    Defined at 3dfm_main.f90 lines 14-1230
    
    Parameters
    ----------
    sources : float array
    nsources : int
    receivers : float array
    nreceivers : int
    outrays : float array
    outtts : float array
    
    \
        ---------------------------------------------------------------------------------------------------
     initialize intersections (interface grid + navigation pointers) and regions \
         (collection of grid
     points between two interfaces, including the bounding intersections ). The fast \
         marching
     solution is evaluated region by region.
    ---------
      calculate the intersection points, i.e. where the surfaces cut through the \
          regular propagation grid
    """
    _fmm3d.f90wrap_run(sources=sources, nsources=nsources, receivers=receivers, \
        nreceivers=nreceivers, outrays=outrays, outtts=outtts)

def initialize_velocity_grids(vgrids, ngrids, ntypes, nr, nlambda, nphi, r0, \
    lambda0, phi0, dr, dlambda, dphi):
    """
    initialize_velocity_grids(vgrids, ngrids, ntypes, nr, nlambda, nphi, r0, \
        lambda0, phi0, dr, dlambda, dphi)
    
    
    Defined at 3dfmlib.f90 lines 7-99
    
    Parameters
    ----------
    vgrids : float array
    ngrids : int
    ntypes : int
    nr : int
    nlambda : int
    nphi : int
    r0 : float
    lambda0 : float
    phi0 : float
    dr : float
    dlambda : float
    dphi : float
    
    """
    _fmm3d.f90wrap_initialize_velocity_grids(vgrids=vgrids, ngrids=ngrids, \
        ntypes=ntypes, nr=nr, nlambda=nlambda, nphi=nphi, r0=r0, lambda0=lambda0, \
        phi0=phi0, dr=dr, dlambda=dlambda, dphi=dphi)

def initialize_propagation_grid(nr, nlat, nlon, dr, dlat, dlon, h0, lat0, lon0):
    """
    initialize_propagation_grid(nr, nlat, nlon, dr, dlat, dlon, h0, lat0, lon0)
    
    
    Defined at 3dfmlib.f90 lines 104-187
    
    Parameters
    ----------
    nr : int
    nlat : int
    nlon : int
    dr : float
    dlat : float
    dlon : float
    h0 : float
    lat0 : float
    lon0 : float
    
    """
    _fmm3d.f90wrap_initialize_propagation_grid(nr=nr, nlat=nlat, nlon=nlon, dr=dr, \
        dlat=dlat, dlon=dlon, h0=h0, lat0=lat0, lon0=lon0)

def initialize_interfaces(lambda0, phi0, nlambda, nphi, dlambda, dphi):
    """
    initialize_interfaces(lambda0, phi0, nlambda, nphi, dlambda, dphi)
    
    
    Defined at 3dfmlib.f90 lines 194-292
    
    Parameters
    ----------
    lambda0 : float
    phi0 : float
    nlambda : int
    nphi : int
    dlambda : float
    dphi : float
    
    """
    _fmm3d.f90wrap_initialize_interfaces(lambda0=lambda0, phi0=phi0, \
        nlambda=nlambda, nphi=nphi, dlambda=dlambda, dphi=dphi)

