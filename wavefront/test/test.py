import _test
import f90wrap.runtime
import logging

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
        _test.f90wrap_allocate_receivers(n=n)
    
    @staticmethod
    def allocate_sources(n):
        """
        allocate_sources(n)
        
        
        Defined at initialize.f90 lines 21-34
        
        Parameters
        ----------
        n : int
        
        """
        _test.f90wrap_allocate_sources(n=n)
    
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
        _test.f90wrap_allocate_vgrids(nvgrids=nvgrids, nvtypes=nvtypes)
    
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
        _test.f90wrap_define_interfaces(intrfaces=intrfaces, ninter=ninter, nlat=nlat, \
            nlon=nlon, lat0=lat0, lon0=lon0, dlat=dlat, dlon=dlon)
    
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
        _test.f90wrap_define_propagation_grid(lat0=lat0, lon0=lon0, depth0=depth0, \
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
        _test.f90wrap_define_receiver(rxid=rxid, lat=lat, lon=lon, depth=depth, \
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
        _test.f90wrap_define_source(srcid=srcid, is_tele=is_tele, lat=lat, lon=lon, \
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
        _test.f90wrap_define_path(srcid=srcid, pathid=pathid, n_steps=n_steps, \
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
        _test.f90wrap_define_vgrid(vtypeid=vtypeid, gridid=gridid, values=values, r0=r0, \
            lambda0=lambda0, phi0=phi0, nr=nr, nlambda=nlambda, nphi=nphi, dr=dr, \
            dlambda=dlambda, dphi=dphi)
    
    @staticmethod
    def finalize_definitions():
        """
        finalize_definitions()
        
        
        Defined at initialize.f90 lines 391-659
        
        
        """
        _test.f90wrap_finalize_definitions()
    
    _dt_array_initialisers = []
    

initialize = Initialize()

class Core(f90wrap.runtime.FortranModule):
    """
    Module core
    
    
    Defined at fmm3dlib.f90 lines 296-586
    
    """
    @staticmethod
    def march():
        """
        march()
        
        
        Defined at fmm3dlib.f90 lines 302-584
        
        
        """
        _test.f90wrap_march()
    
    _dt_array_initialisers = []
    

core = Core()

class Fmm3Dlib(f90wrap.runtime.FortranModule):
    """
    Module fmm3dlib
    
    
    Defined at fmm3dlib.f90 lines 591-596
    
    """
    pass
    _dt_array_initialisers = []
    

fmm3dlib = Fmm3Dlib()

class Fmm3Dlib_Noint(f90wrap.runtime.FortranModule):
    """
    Module fmm3dlib_noint
    
    
    Defined at fmm3dlib.f90 lines 601-605
    
    """
    pass
    _dt_array_initialisers = []
    

fmm3dlib_noint = Fmm3Dlib_Noint()

