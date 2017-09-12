from . import _fmm3dlib
import f90wrap.runtime
import logging

class Core(f90wrap.runtime.FortranModule):
    """
    Module core
    
    
    Defined at fmm3dlib.f90 lines 296-653
    
    """
    @staticmethod
    def march():
        """
        march()
        
        
        Defined at fmm3dlib.f90 lines 302-586
        
        
        """
        _fmm3dlib.f90wrap_march()
    
    @staticmethod
    def get_nsources():
        """
        get_nsources = get_nsources()
        
        
        Defined at fmm3dlib.f90 lines 592-594
        
        
        Returns
        -------
        get_nsources : int
        
        """
        get_nsources = _fmm3dlib.f90wrap_get_nsources()
        return get_nsources
    
    @staticmethod
    def get_nrays(recid):
        """
        get_nrays = get_nrays(recid)
        
        
        Defined at fmm3dlib.f90 lines 599-602
        
        Parameters
        ----------
        recid : int
        
        Returns
        -------
        get_nrays : int
        
        """
        get_nrays = _fmm3dlib.f90wrap_get_nrays(recid=recid)
        return get_nrays
    
    @staticmethod
    def get_nreceivers():
        """
        get_nreceivers = get_nreceivers()
        
        
        Defined at fmm3dlib.f90 lines 607-609
        
        
        Returns
        -------
        get_nreceivers : int
        
        """
        get_nreceivers = _fmm3dlib.f90wrap_get_nreceivers()
        return get_nreceivers
    
    @staticmethod
    def get_nsections(recid, rayid):
        """
        get_nsections = get_nsections(recid, rayid)
        
        
        Defined at fmm3dlib.f90 lines 615-619
        
        Parameters
        ----------
        recid : int
        rayid : int
        
        Returns
        -------
        get_nsections : int
        
        """
        get_nsections = _fmm3dlib.f90wrap_get_nsections(recid=recid, rayid=rayid)
        return get_nsections
    
    @staticmethod
    def get_npoints(recid, rayid, secid):
        """
        get_npoints = get_npoints(recid, rayid, secid)
        
        
        Defined at fmm3dlib.f90 lines 624-629
        
        Parameters
        ----------
        recid : int
        rayid : int
        secid : int
        
        Returns
        -------
        get_npoints : int
        
        """
        get_npoints = _fmm3dlib.f90wrap_get_npoints(recid=recid, rayid=rayid, \
            secid=secid)
        return get_npoints
    
    @staticmethod
    def get_ray_section(recid, rayid, secid, npts):
        """
        get_ray_section = get_ray_section(recid, rayid, secid, npts)
        
        
        Defined at fmm3dlib.f90 lines 634-640
        
        Parameters
        ----------
        recid : int
        rayid : int
        secid : int
        npts : int
        
        Returns
        -------
        get_ray_section : float array
        
        """
        get_ray_section = _fmm3dlib.f90wrap_get_ray_section(recid=recid, rayid=rayid, \
            secid=secid, npts=npts, n0=npts)
        return get_ray_section
    
    @staticmethod
    def get_ray_arrival_time(recid, rayid):
        """
        get_ray_arrival_time = get_ray_arrival_time(recid, rayid)
        
        
        Defined at fmm3dlib.f90 lines 645-649
        
        Parameters
        ----------
        recid : int
        rayid : int
        
        Returns
        -------
        get_ray_arrival_time : float
        
        """
        get_ray_arrival_time = _fmm3dlib.f90wrap_get_ray_arrival_time(recid=recid, \
            rayid=rayid)
        return get_ray_arrival_time
    
    _dt_array_initialisers = []
    

core = Core()

class Fmm3Dlib(f90wrap.runtime.FortranModule):
    """
    Module fmm3dlib
    
    
    Defined at fmm3dlib.f90 lines 659-664
    
    """
    pass
    _dt_array_initialisers = []
    

fmm3dlib = Fmm3Dlib()

class Fmm3Dlib_Noint(f90wrap.runtime.FortranModule):
    """
    Module fmm3dlib_noint
    
    
    Defined at fmm3dlib.f90 lines 670-674
    
    """
    pass
    _dt_array_initialisers = []
    

fmm3dlib_noint = Fmm3Dlib_Noint()

class Initialize(f90wrap.runtime.FortranModule):
    """
    Module initialize
    
    
    Defined at initialize.f90 lines 1-777
    
    """
    @staticmethod
    def allocate_receivers(n):
        """
        allocate_receivers(n)
        
        
        Defined at initialize.f90 lines 8-16
        
        Parameters
        ----------
        n : int
        
        """
        _fmm3dlib.f90wrap_allocate_receivers(n=n)
    
    @staticmethod
    def allocate_sources(n):
        """
        allocate_sources(n)
        
        
        Defined at initialize.f90 lines 21-34
        
        Parameters
        ----------
        n : int
        
        """
        _fmm3dlib.f90wrap_allocate_sources(n=n)
    
    @staticmethod
    def allocate_vgrids(nvgrids, nvtypes):
        """
        allocate_vgrids(nvgrids, nvtypes)
        
        
        Defined at initialize.f90 lines 40-51
        
        Parameters
        ----------
        nvgrids : int
        nvtypes : int
        
        """
        _fmm3dlib.f90wrap_allocate_vgrids(nvgrids=nvgrids, nvtypes=nvtypes)
    
    @staticmethod
    def define_interfaces(intrfaces, ninter, nlat, nlon, lat0, lon0, dlat, dlon):
        """
        define_interfaces(intrfaces, ninter, nlat, nlon, lat0, lon0, dlat, dlon)
        
        
        Defined at initialize.f90 lines 60-130
        
        Parameters
        ----------
        intrfaces : float array
        ninter : int
        nlat : int
        nlon : int
        lat0 : float
        lon0 : float
        dlat : float
        dlon : float
        
        """
        _fmm3dlib.f90wrap_define_interfaces(intrfaces=intrfaces, ninter=ninter, \
            nlat=nlat, nlon=nlon, lat0=lat0, lon0=lon0, dlat=dlat, dlon=dlon)
    
    @staticmethod
    def define_propagation_grid(lat0, lon0, depth0, nlat, nlon, ndepth, dlat, dlon, \
        ddepth):
        """
        define_propagation_grid(lat0, lon0, depth0, nlat, nlon, ndepth, dlat, dlon, \
            ddepth)
        
        
        Defined at initialize.f90 lines 137-199
        
        Parameters
        ----------
        lat0 : float
        lon0 : float
        depth0 : float
        nlat : int
        nlon : int
        ndepth : int
        dlat : float
        dlon : float
        ddepth : float
        
        """
        _fmm3dlib.f90wrap_define_propagation_grid(lat0=lat0, lon0=lon0, depth0=depth0, \
            nlat=nlat, nlon=nlon, ndepth=ndepth, dlat=dlat, dlon=dlon, ddepth=ddepth)
    
    @staticmethod
    def define_receiver(rxid, lat, lon, depth, n_rays, source_ids, path_ids):
        """
        define_receiver(rxid, lat, lon, depth, n_rays, source_ids, path_ids)
        
        
        Defined at initialize.f90 lines 210-239
        
        Parameters
        ----------
        rxid : int
        lat : float
        lon : float
        depth : float
        n_rays : int
        source_ids : int array
        path_ids : int array
        
        """
        _fmm3dlib.f90wrap_define_receiver(rxid=rxid, lat=lat, lon=lon, depth=depth, \
            n_rays=n_rays, source_ids=source_ids, path_ids=path_ids)
    
    @staticmethod
    def define_source(srcid, is_tele, lat, lon, depth, n_paths):
        """
        define_source(srcid, is_tele, lat, lon, depth, n_paths)
        
        
        Defined at initialize.f90 lines 249-282
        
        Parameters
        ----------
        srcid : int
        is_tele : bool
        lat : float
        lon : float
        depth : float
        n_paths : int
        
        """
        _fmm3dlib.f90wrap_define_source(srcid=srcid, is_tele=is_tele, lat=lat, lon=lon, \
            depth=depth, n_paths=n_paths)
    
    @staticmethod
    def define_path(srcid, pathid, n_steps, steps, vtypes):
        """
        define_path(srcid, pathid, n_steps, steps, vtypes)
        
        
        Defined at initialize.f90 lines 291-317
        
        Parameters
        ----------
        srcid : int
        pathid : int
        n_steps : int
        steps : int array
        vtypes : int array
        
        """
        _fmm3dlib.f90wrap_define_path(srcid=srcid, pathid=pathid, n_steps=n_steps, \
            steps=steps, vtypes=vtypes)
    
    @staticmethod
    def define_vgrid(vtypeid, gridid, values, r0, lambda0, phi0, nr, nlambda, nphi, \
        dr, dlambda, dphi):
        """
        define_vgrid(vtypeid, gridid, values, r0, lambda0, phi0, nr, nlambda, nphi, dr, \
            dlambda, dphi)
        
        
        Defined at initialize.f90 lines 333-386
        
        Parameters
        ----------
        vtypeid : int
        gridid : int
        values : float array
        r0 : float
        lambda0 : float
        phi0 : float
        nr : int
        nlambda : int
        nphi : int
        dr : float
        dlambda : float
        dphi : float
        
        """
        _fmm3dlib.f90wrap_define_vgrid(vtypeid=vtypeid, gridid=gridid, values=values, \
            r0=r0, lambda0=lambda0, phi0=phi0, nr=nr, nlambda=nlambda, nphi=nphi, dr=dr, \
            dlambda=dlambda, dphi=dphi)
    
    @staticmethod
    def finalize_definitions():
        """
        finalize_definitions()
        
        
        Defined at initialize.f90 lines 391-659
        
        
        """
        _fmm3dlib.f90wrap_finalize_definitions()
    
    _dt_array_initialisers = []
    

initialize = Initialize()

