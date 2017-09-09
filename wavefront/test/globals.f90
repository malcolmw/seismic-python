MODULE globals
  USE typedefn
! Global parameters.
! Intersection nodes snap to regular grid if closer than this fraction
! of radial grid cell size (to avoid tiny triangles).
    REAL(KIND=dp), PARAMETER   :: interface_tolerance = 0.005_dp
! Default value for a time that is larger than any realistic value.
    REAL(KIND=dp), PARAMETER   :: huge_time = 1.0e20_dp
    REAL(KIND=dp), PARAMETER   :: earth_radius = 6371.0_dp
    REAL(KIND=dp), PARAMETER   :: deg_to_rad=acos(-1.0_dp)/180._dp
! Reduction in size for refined source grid.
    INTEGER   :: refinement_factor
! Extent of refined grid around the source in main grid cells
! refinement parameters are overwritten by values in propgrid.in.
    INTEGER   :: ncell_to_be_refined
    INTEGER   :: global_source_counter
    INTEGER   :: raypoint_counter
    LOGICAL   :: file_mode
    LOGICAL   :: no_pp_mode
    LOGICAL   :: parallel_mode
    LOGICAL   :: display_mode
    LOGICAL   :: save_rays_mode
    LOGICAL   :: save_timefields_mode
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! Below the definition of variables that will be accessible to every
! subprogram this array of type Tinterface defines  the location of the
! interfaces on the propagation grids by B-spline interpolation.
    INTEGER                                             :: n_interfaces
    TYPE(Tinterface), DIMENSION(:), POINTER             :: intrface
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! These are the velocity grids used to define the velocity on the
! propagation grids by B-spline interpolation.
    INTEGER                                             :: n_vgrids
    INTEGER                                             :: n_vtypes
    TYPE(Tvelocity_grid), DIMENSION(:,:), POINTER       :: vgrid
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! The main propagation grid.
    TYPE(Tpropagation_grid), POINTER                    :: pgrid
! These are the intersections associated with the main propgation grid.
    INTEGER                                             :: n_intersections
    TYPE(Tintersection), DIMENSION(:), POINTER          :: intersection
! These are the regions of the main propagation grid.
    INTEGER                                             :: n_regions
    TYPE(Tregion), DIMENSION(:), POINTER                :: region
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! The fine grid around the source.
    TYPE(Tpropagation_grid), POINTER                    :: sgrid
! These are the intersections associated with the refined source grid.
    INTEGER                                             :: n_sintersections
    TYPE(Tintersection), DIMENSION(:), POINTER          :: sintersection
! These are the regions of the refined source grid.
    INTEGER                                             :: n_sregions
    TYPE(Tregion), DIMENSION(:), POINTER                :: sregion
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! The receivers.
    INTEGER                                             :: n_receivers
    TYPE(Treceiver), DIMENSION(:), POINTER              :: receiver
! The sources.
! The number of sources defined in the input.
    INTEGER                                             :: n_sources
! n_sources + # of virtual sources at receiver.
    INTEGER                                             :: n_sources_ppinc
! Positions required for reflection matching.
    TYPE(Tsource), DIMENSION(:), POINTER                :: source
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! Parameters of the inversion.
! Total # of inversion parameters.
    INTEGER                                             :: n_inv_parms
! Total # of active inversion parameters.
    INTEGER                                             :: n_inv_active
! # of velocity grids to be solved for.
    INTEGER                                             :: n_inv_vgrid
! List of velocity grids to be solved for.
    TYPE(Tgrid_identifier) , DIMENSION(:), POINTER      :: vgrids_to_be_inv
! # of interfaces to be solved for.
    INTEGER                                             :: n_inv_iface
! List of interfaces to be solved for.
    INTEGER, DIMENSION(:), POINTER                      :: ifaces_to_be_inv
! Solve for source position and time or not.
    LOGICAL                                             :: locate_source
! # of sources to be solved for.
    INTEGER                                             :: n_inv_source
! List of sources to be solved for.
    INTEGER, DIMENSION(:), POINTER                      :: sources_to_be_inv
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
CONTAINS
  SUBROUTINE display()
    INTEGER                   :: rxID,&
                               & rayID,&
                               & srcID,&
                               & pathID
    TYPE(Treceiver), POINTER  :: rx
    TYPE(Tray), POINTER       :: ray
    TYPE(Tsource), POINTER    :: src
    TYPE(Tpath), POINTER      :: path
    DO rxID=1,n_receivers
      rx => receiver(rxID)
      print *,"RECEIVER:",rx%id,rx%lat,rx%long,rx%r,rx%n_rays
      DO rayID=1,rx%n_rays
        ray => rx%ray(rayID)
        print *,"    RAY:",ray%source_id,ray%raypath_id
      ENDDO
    ENDDO
    DO srcID=1,n_sources
      src => source(srcID)
      print *,"SOURCE:",src%id,src%lat,src%long,src%r,src%n_paths
      DO pathID=1,src%n_paths
        path => src%path(pathID)
        print *,"    PATH:",path%id
        print *,"        :",path%sequence
        print *,"        :",path%vtype_sequence
      ENDDO
    ENDDO
  END SUBROUTINE display
END MODULE globals
