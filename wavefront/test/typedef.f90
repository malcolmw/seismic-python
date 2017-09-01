MODULE typedefn
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  INTEGER, PARAMETER     :: sp = SELECTED_REAL_KIND(6,37)
  INTEGER, PARAMETER     :: dp = SELECTED_REAL_KIND(15,307)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  TYPE Tbackpointer
! Three integer numbers that uniquely identify each node for regular
! grid nodes these are the grid coordinates in r,lat and long for
! interface nodes i1=0, i2= id of interface, i3 = number of node in
! list of interface nodes.
    INTEGER :: i1
    INTEGER :: i2
    INTEGER :: i3
  END TYPE Tbackpointer
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  TYPE Tgrid_identifier
    INTEGER   :: igrid,&
               & vtype
  END TYPE Tgrid_identifier
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  TYPE Tinteger_coordinates
    INTEGER :: ir,&
             & ilat,&
             & ilong
  END TYPE Tinteger_coordinates
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  TYPE Tinterface
! This type defines the position of an interface
! Note: type Tinterface defines of the position of the interface (used
! as input by the cubic spline interpolation).
! Type Tintersection contains the actual nodes of the interface and
! everything related to them.

! Grid definitions.
! # of points in lat,long.
    INTEGER                                 :: nlat,&
                                             & nlong,&
                                             & id
! Size of intervals.
    REAL(KIND=dp)                           :: dlat0,&
                                             & dlong0
! Position of grid origin.
    REAL(KIND=dp)                           :: lat0,&
                                             & long0
! True if the interface touches another.
    LOGICAL                                 :: pinched
! Parametrs of the inversion.
! # of parameters describing the interface position.
    INTEGER                                 :: nnode
! Start index of the interface parameters in the global parametr list.
    INTEGER                                 :: start_index
! Is the position of this interface is to be inverted for?
    LOGICAL                                 :: to_be_inverted
    REAL(KIND=dp), DIMENSION (:), POINTER   :: lat
    REAL(KIND=dp), DIMENSION (:), POINTER   :: long
! The actual radius values for the interface at the nodes.
    REAL(KIND=dp), DIMENSION (:,:), POINTER :: r
  END TYPE Tinterface
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
TYPE Tintersection
! This type contains information about where an interface intersects
! with a grid
! Note: type Tinterface defines of the position of the interface (used
! as input by the cubic spline interpolation) type Tintersection
! contains the actual nodes of the interface and everything related to
! them.
! # of intersection nodes, # of grid cells cut by the interface.
    INTEGER                                             :: nnode,n_ccells
! Intersection id.
    INTEGER                                             :: id
! Corresponding interface id.
    INTEGER                                             :: iface_id
! Pointer to the grid on which the intersection is defined.
    TYPE(Tpropagation_grid), POINTER                    :: grid
! Flags
! True if the the intersection touches another.
    LOGICAL                                             :: pinched
! Positions of the intersection nodes.
    REAL(KIND=dp), DIMENSION (:), POINTER               :: r
    REAL(KIND=dp), DIMENSION (:), POINTER               :: lat
    REAL(KIND=dp), DIMENSION (:), POINTER               :: long
    REAL(KIND=dp), DIMENSION (:), POINTER               :: coslat
! Vector giving the normal of the interface at every intersection node.
    REAL(KIND=dp), DIMENSION (:,:), POINTER             :: normal
! Velocities on both side of the interface.
    REAL(KIND=dp), DIMENSION (:,:), POINTER             :: vel_top
    REAL(KIND=dp), DIMENSION (:,:), POINTER             :: vel_bot
! Time a front arrives at an intersection node.
    REAL(KIND=dp), DIMENSION (:), POINTER               :: arrivaltime
! Time a front starts from an intersection node.
    REAL(KIND=dp), DIMENSION (:), POINTER               :: starttime
! Time gradient at an interface node. The time gradient is normal to
! the wave front and has size 1/velocity.
    REAL(KIND=dp), DIMENSION (:,:), POINTER             :: time_gradient
! Type of inode (0:on grid,1,2,3 on r,lat long connection)
    INTEGER, DIMENSION(:), POINTER                      :: intype
! The variables below allow us to identify the grid cells that an
! intersection node is part of and the inverse, the intersection nodes
! that are part of a given grid cell.
    TYPE(Tinteger_coordinates), DIMENSION (:), POINTER  :: ccells
! List of cells cut by this interface.
    INTEGER, DIMENSION(:), POINTER                      :: n_inodes
! Actual inodes in cut cell.
    INTEGER, DIMENSION(:,:), POINTER                    :: inodes
! Pointer from inode to cut cells it is in.
    INTEGER, DIMENSION (:,:), POINTER                   :: ccell_from_inode
! These variables connect the intersection with the regions (abov and
! below) that is is part of.
! The region above the intersection.
    TYPE(Tregion), POINTER                              :: regabo
! The region above the intersection.
    TYPE(Tregion), POINTER                              :: regbel
! Index of each intersection node in the node list of the region above
! the intersection.
    INTEGER, DIMENSION (:), POINTER                     :: rabo_node_id
! Index of each intersection node in the node list of the region below
! the intersection.
    INTEGER, DIMENSION (:), POINTER                     :: rbel_node_id
! First regular grid node above the interface at (j,k).
    INTEGER, DIMENSION (:,:), POINTER                   :: irg_abo
! First regular grid node below the interface at (j,k).
    INTEGER, DIMENSION (:,:), POINTER                   :: irg_bel
  END TYPE Tintersection
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  TYPE Tpointer_to_integer_array
    INTEGER, DIMENSION(:), POINTER   :: p
  END TYPE Tpointer_to_integer_array
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  TYPE Tpath
! Contains information about the sequence of interface interactions
! defining a path in multi-stage fast marching.

! Index of path in user-defined list.
    INTEGER                            :: id
! # of time fields on each path.
    INTEGER                            :: n_tf
! The sequence of interfaces on each path.
    INTEGER, DIMENSION(:), POINTER     :: sequence
! The sequence of time fields on each path. Number refers to index in
! time_field array in source
    INTEGER, DIMENSION(:), POINTER     :: tf_sequence
! The sequence of velocity types on each path.
    INTEGER, DIMENSION(:), POINTER     :: vtype_sequence
! Flag for valid path, required sequence may not exist.
    LOGICAL                            :: valid
! Flag set if path is actually used.
    LOGICAL                            :: used
! Flag set if a grid of arrival times is to be saved for this path.
    LOGICAL                            :: gridsave
    INTEGER                            :: first_tf_to_save
! =0 if no late reflections, step indicating refl otherwise.
    INTEGER                            :: refstep
! Interface at which fitting is performed.
    INTEGER                            :: fitting_interface
  END TYPE Tpath
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  TYPE Tpropagation_grid
! A regular grid used for wave front propagation with fast marching.
! # of grid cells in each direction.
    INTEGER       :: nr,&
                   & nlong,&
                   & nlat
! Grid step sizes.
    REAL(KIND=dp) :: dr0,&
                   & dlat0,&
                   & dlong0
! Position of grid origin.
    REAL(KIND=dp) :: r0,&
                   & lat0,&
                   & long0
! Position of grid corner opposite origin.
    REAL(KIND=dp) :: rmax,&
                   & latmax,&
                   & longmax
! Tolerance for deciding if a position coincides exactly with the grid
! or not.
    REAL(KIND=dp) :: tolerance
    LOGICAL       :: is_main_grid
    LOGICAL       :: is_source_grid
! Total # of nodes.
    INTEGER       :: nnode
! Indices of the origin of a refined source grid in the main grid.
    INTEGER       :: index_r0,&
                   & index_lat0,&
                   & index_long0
    REAL(KIND=dp), DIMENSION (:), POINTER :: r
    REAL(KIND=dp), DIMENSION (:), POINTER :: lat
    REAL(KIND=dp), DIMENSION (:), POINTER :: long
    REAL(KIND=dp), DIMENSION (:), POINTER :: coslat
    REAL(KIND=dp), DIMENSION (:,:,:,:), POINTER   :: velocity
    REAL(KIND=dp), DIMENSION (:,:,:), POINTER     :: arrivaltime
    REAL(KIND=dp), DIMENSION (:,:,:,:), POINTER   :: time_gradient
! Identifies region of which this node is part.
    INTEGER, DIMENSION (:,:,:), POINTER :: node_region
! Index of this node in the regional node list of the region to which
! it belongs.
    INTEGER, DIMENSION (:,:,:), POINTER :: rnode_id
! Is node surrounded by regular cells only.
    LOGICAL, DIMENSION(:,:,:),  POINTER :: fully_regular
! Here it gets complicated: ccind_from_3dc stands for cut cell index
! from 3D coordinates. If a cell i,j,k of the grid is cut by an
! interface, and therefore has intersection nodes, the pointer
! ccind_from_3dc(i,j,k) is allocated, and points to an integer array
! ccind_from_3dc(i,j,k)%p of length n_intersections. If the cell is cut
! by intersection n, ccind_from_3dc(i,j,k)%p(n) contains the index of
! the cut cell i,j,k in the cut cell list of intersection n. For an
! intersection m that does not cut the cell  ccind_from_3dc(i,j,k)%p(m)
! is zero. In this way we can identify the intersection nodes that are
! part of a cell from its position in the grid.
    TYPE(Tpointer_to_integer_array), DIMENSION (:,:,:), POINTER :: ccind_from_3dc
  END TYPE Tpropagation_grid
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  TYPE Treceiver
! Identifies the receiver.
    INTEGER                                    :: id
! Position.
    REAL(KIND=dp)                              :: r,&
                                                & lat,&
                                                & long,&
                                                & coslat
! The arrival time at the receiver (not used).
    REAL(KIND=dp), DIMENSION(:), POINTER       :: arrivaltime
! Number of paths ending at this receiver.
    INTEGER                                    :: n_rays
! Rays of the paths ending at this receiver.
    TYPE(Tray), DIMENSION(:), POINTER          :: ray
! The variables below are only used if the path contains a reflection
! fit they identify the sequence of time fields from the receiver to
! the intermediate fitting interface.
! Index in source list of this receiver.
    INTEGER                                    :: source_equivalent
! Corresponding path in the source_equivalent
    INTEGER, DIMENSION(:), POINTER             :: path_equivalent
  END TYPE Treceiver
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  TYPE Tray_section
! A ray section is the part of a ray between two interfaces, except the
! first one which starts at source, and the last one which ends at a
! receiver.
! The ray that this section is part of
    TYPE(Tray), POINTER                        :: ray
! The region in which the ray section lies
    TYPE(Tregion), POINTER                     :: reg
! The intersection at which the integration to find the ray starts.
! Note that the rays are found integrating backward in time!
    TYPE(Tintersection), POINTER               :: istart
! The intersection at which the ray integration ends.
    TYPE(Tintersection), POINTER               :: iend
! The time field used for finding the ray.
    TYPE(Ttime_field), POINTER                 :: tf
! The source of the ray.
    TYPE(Tsource), POINTER                     :: source
! # of points on this ray section.
    INTEGER                                    :: npoints
! The actual positions of the points on the ray section.
    REAL(KIND=dp), DIMENSION(:,:), POINTER     :: point
! The position of the section in collection of ray sections defining
! the ray.
    INTEGER                                    :: place_in_sequence
    LOGICAL                                    :: diffracted
    LOGICAL                                    :: headwave
  END TYPE Tray_section
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  TYPE Tray
  ! A ray is a collection of ray sections that define a given
  ! ray/path/phase.
! # of sections on the ray.
    INTEGER                                      :: nsections
! The actual ray sections.
    TYPE(Tray_section), DIMENSION(:), POINTER    :: section
! The source of this ray.
    TYPE(Tsource), POINTER                       :: source
! Number of ray in list of rays from this source.
    INTEGER                                      :: raypath_id
    INTEGER                                      :: source_id
! Time the ray arrives at the receiver.
    REAL(KIND=dp)                                :: receiver_time
! Time gradient (direction) of ray at the receiver.
    REAL(KIND=dp), DIMENSION(3)                  :: receiver_time_gradient
    LOGICAL                                      :: diffracted
    LOGICAL                                      :: headwave
! True if reflection fit is required.
    LOGICAL                                      :: is_multiray
! # of reflections found in fit.
    INTEGER                                      :: n_subrays
! Contains the rays in case of a the reflection fit.
    TYPE(Tray), DIMENSION(:), POINTER            :: subray
! Variables relating to the inversion process
! # of non-zero partial derivatives based on this ray.
    INTEGER                                      :: n_pdev
! List of inversion parameters for which the
! partial derivative of the arrival time is non-zero.
    INTEGER, DIMENSION(:), POINTER               :: pdev_indx
! Partial derivative of the arrival time with respect to the
! corresponding inversion parameter in the array pdev_indx.
    REAL(KIND=dp), DIMENSION(:), POINTER         :: pdev
! Set to false if this ray does not exist.
    LOGICAL                                      :: valid

  END TYPE Tray
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  TYPE Tregion
! This type contains a region of the propagation grid between
! interfaces the region is a volume of space between two interfaces,
! and contains nodes of the regular grid and both bounding
! intersections. Fast marching proceeds on a region by region basis.
! Region identification.
    INTEGER                                     :: id
! Velocity definition grid associated with this region.
    INTEGER                                     :: ivgrid
! Intersections at the top and bottom of this region.
    TYPE(Tintersection), POINTER                :: itop,&
                                                 & ibot
! Pointer to the grid on which the region is defined.
    TYPE(Tpropagation_grid), POINTER            :: grid
! Number of propagation grid nodes in this region.
    INTEGER                                     :: ngnode
! Arrays below define a 1-D list of regular + intersection nodes
! constituting this region this 1-D array is used for the fast
! marching.
! Total number of nodes in this region including boundary nodes.
    INTEGER                                     :: nnode
! Points back from 1-D list of nodes in the.
    TYPE(Tbackpointer), DIMENSION(:), POINTER   :: node
! Fast marching status.
    INTEGER, DIMENSION(:), POINTER              :: node_status
    REAL(KIND=dp), DIMENSION(:), POINTER        :: arrivaltime
    REAL(KIND=dp), DIMENSION(:,:), POINTER      :: time_gradient
    REAL(KIND=dp), DIMENSION(:,:), POINTER      :: velocity
    REAL(KIND=dp), DIMENSION(:), POINTER        :: r
    REAL(KIND=dp), DIMENSION(:), POINTER        :: lat
    REAL(KIND=dp), DIMENSION(:), POINTER        :: long
    REAL(KIND=dp), DIMENSION(:), POINTER        :: coslat
! Nodes that have been initialized from a teleseismic source.
! Number of initialized nodes.
    INTEGER                                     :: n_init
! The list of initialized nodes.
    INTEGER, DIMENSION(:), POINTER              :: init_id
! The list of initialized nodes.
    INTEGER, DIMENSION(:), POINTER              :: init_type
! Arrival time of the init nodes.
    REAL(KIND=dp), DIMENSION(:), POINTER        :: init_arrivaltime
! Incoming gradient at the init node.
    REAL(KIND=dp), DIMENSION(:,:), POINTER      :: init_time_gradient
  END TYPE Tregion
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
TYPE Tsource
! Id # of source.
    INTEGER                                   :: id
! Position.
    REAL(KIND=dp)                             :: r,&
                                               & lat,&
                                               & long,&
                                               & coslat
! Main grid cell containing source.
    INTEGER                                   :: ir,&
                                               & ilat,&
                                               & ilong
! Nodes connected to the source.
    TYPE(Tbackpointer)                        :: cnode(100)
! # of nodes connected to the source.
    INTEGER                                   :: n_cnode
    LOGICAL                                   :: on_grid,&
                                               & on_interface,&
                                               & on_pinched_interface
    INTEGER                                   :: region_id,&
                                               & interface_id
    INTEGER                                   :: topreg_id,&
                                               & botreg_id,&
                                               & topint_id,&
                                               & botint_id
    LOGICAL                                   :: is_local,&
                                               & is_teleseismic
    INTEGER                                   :: teleseismic_id
    character(LEN=8)                          :: teleseismic_phase
    INTEGER                                   :: nfile
! # of timefields in which source lies (1/2). 1 if in a region, 2 if on
! an interface that is not top or bottom.
    INTEGER                                   :: n_tf_init
! Indices of source time fields.
    INTEGER, DIMENSION(:), POINTER            :: first_tf_up
! Indices of source time fields.
    INTEGER, DIMENSION(:), POINTER            :: first_tf_down
! These are the paths (sequence of reflections/refractions) originating
! from this source that have to be computed.
! # of paths for this source.
    INTEGER                                   :: n_paths
! The actual paths.
    TYPE(Tpath), DIMENSION(:), POINTER        :: path
    TYPE(Tpath), DIMENSION(2,2)               :: init_path

! These are the time fields containing regional traveltimes for all
! computed paths.
! # of time fields for this source.
    INTEGER                                   :: n_time_fields
! List of time fields.
    TYPE(Ttime_field), DIMENSION(:), POINTER  :: time_field
! Parameters having to do with the calculation of Frechet derivatives
! Location of source parametrs in inversion parameter array.
    INTEGER                                   :: start_index
! Flag showing whether the the source parameters are fixed or free.
    LOGICAL                                   :: to_be_inverted
  END TYPE Tsource
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  TYPE Ttime_field
! The type Ttimefield contains a fast marching solution for the arrival
! times and the time gradients in a region.
! Identifies the time field.
    INTEGER                                     :: id
! The type of velocity used for this tf.
    INTEGER                                     :: vtype
! Number of file in which data will be stored.
    INTEGER                                     :: nfile
! The region this time field refers to.
    TYPE(Tregion), POINTER                      :: reg
! The intersection from which the FMM started.
    TYPE(Tintersection), POINTER                :: istart
! The other intersection of the region.
    TYPE(Tintersection), POINTER                :: inonstart
    REAL(KIND=dp),dimension(:), POINTER         :: arrivaltime
    REAL(KIND=dp),dimension(:,:), POINTER       :: time_gradient
! Indicates if turning rays hit the starting intersection during FMM
    LOGICAL                                     :: turning_rays_present
! If turning rays were present, this array ! indicates which nodes of
! the starting intersection received them.
    LOGICAL, DIMENSION(:), POINTER              :: received_turning_ray
! These pointers allow the time fields to be organised in a tree
! structure that allows for easy re-use of timefields already
! calculated by other path sequences.
! Pointer to the previous time field on the path/ray.
    INTEGER                                     :: prev_tf
! Pointer to the next time fields, possibilities:
!   (1) up from inonstart (vtype = 1)
!   (2) down from inonstart 1
!   (3) up from istart (only possible if turning rays exist) 1
!   (4) down from istart (only possible if turning rays exist) 1
!   (1) up from inonstart (vtype = 2)
!   (2) down from inonstart 2
!   (3) up from istart (only possible if turning rays exist) 2
!   (4) down from istart (only possible if turning rays exist) 2
    INTEGER                                     :: next_tf(8)
  END TYPE Ttime_field
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  TYPE Ttriangulation
! This type contains a 2-dimensional triangulation of a point set.
! Number of points.
    INTEGER                                    :: npoints
! The coordinates of the points.
    REAL(KIND=dp), DIMENSION(:,:), POINTER     :: points
! # of triangles.
    INTEGER                                    :: ntriangles
! The points that are part of a given triangle.
    INTEGER, DIMENSION(:,:), POINTER           :: points_from_triangle
! The triangles that neighbour a triangle.
    INTEGER, DIMENSION(:,:), POINTER           :: triangle_neighbours
! # of triangles connected to a ! given point.
    INTEGER, DIMENSION(:), POINTER             :: n_triangles_from_point
! Indices of triangles connected to a ! given point.
    INTEGER, DIMENSION(:,:), POINTER           :: triangles_from_point
  END TYPE Ttriangulation
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  TYPE Tvelocity_grid
! Regular grid defining the velocity as a function of position
! Note: usually each velocity grid is defined over the entire
! propagation grid, but only some nodes actually influence the
! corresponding region
! # of grid cells in each direction.
    INTEGER       :: nr,&
                   & nlong,&
                   & nlat
! Grid step sizes.
    REAL(KIND=dp) :: dr0,&
                   & dlat0,&
                   & dlong0
! Position of grid origin.
    REAL(KIND=dp) :: r0,&
                   & lat0,&
                   & long0
! Total # of nodes.
    INTEGER       :: nnode

! For use in inversion if the grid is a velocity grid.
    INTEGER       :: start_index
! For use in inversion if the grid is a velocity grid.
    LOGICAL       :: to_be_inverted
    REAL(KIND=dp), DIMENSION (:), POINTER         :: r
    REAL(KIND=dp), DIMENSION (:), POINTER         :: lat
    REAL(KIND=dp), DIMENSION (:), POINTER         :: long
    REAL(KIND=dp), DIMENSION (:,:,:), POINTER     :: velocity
! Set to true for the nodes that actually influence the region to which
! the grid belongs.
    LOGICAL, DIMENSION(:,:,:), POINTER            :: active
  END TYPE Tvelocity_grid
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  CONTAINS
! The subroutines below can be called to give variables inside
! instances of the derived types defined above default values when
! allocated. Initialization inside the derived type definition is a
! Fortran 95 feature, and we had to remove it to ensure fortran 90
! compatibility.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE interface_defaults(iface)
      TYPE(Tinterface)  :: iface
      iface%pinched = .FALSE.
      iface%nnode = 0
      iface%to_be_inverted = .FALSE.
      NULLIFY(iface%lat)
      NULLIFY(iface%long)
      NULLIFY(iface%r)
    END SUBROUTINE interface_defaults
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE intersection_defaults(isec)
      TYPE(Tintersection)  :: isec
      isec%nnode = 0
      isec%n_ccells = 0
      isec%id = 0
      isec%iface_id = 0
      NULLIFY(isec%grid)
      isec%pinched = .FALSE.
      NULLIFY(isec%r)
      NULLIFY(isec%lat)
      NULLIFY(isec%long)
      NULLIFY(isec%coslat)
      NULLIFY(isec%normal)
      NULLIFY(isec%vel_top)
      NULLIFY(isec%vel_bot)
      NULLIFY(isec%arrivaltime)
      NULLIFY(isec%starttime)
      NULLIFY(isec%time_gradient)
      NULLIFY(isec%intype)
      NULLIFY(isec%ccells)
      NULLIFY(isec%n_inodes)
      NULLIFY(isec%inodes)
      NULLIFY(isec%ccell_from_inode)
      NULLIFY(isec%regabo)
      NULLIFY(isec%regbel)
      NULLIFY(isec%rabo_node_id)
      NULLIFY(isec%rbel_node_id)
      NULLIFY(isec%irg_abo)
      NULLIFY(isec%irg_bel)
    END SUBROUTINE intersection_defaults
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE source_defaults(source)
      TYPE(Tsource)  :: source
      source%on_grid = .FALSE.
      source%on_interface = .FALSE.
      source%on_pinched_interface = .FALSE.
      source%region_id = 0
      source%interface_id = 0
      source%topreg_id = 0
      source%botreg_id = 0
      source%topint_id = 0
      source%botint_id = 0
      source%is_local = .FALSE.
      source%is_teleseismic = .FALSE.
      source%teleseismic_id = 0
      source%teleseismic_phase = ' '
      source%n_tf_init = 1
      NULLIFY(source%first_tf_up)
      NULLIFY(source%first_tf_down)
      source%n_paths = 0
      source%to_be_inverted  = .FALSE.
      NULLIFY(source%path)
      source%n_time_fields = 0
      NULLIFY(source%time_field)
    END SUBROUTINE source_defaults
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE path_defaults(path)
      TYPE(Tpath)  :: path
      path%id = 0
      path%n_tf = 0
      NULLIFY(path%sequence)
      NULLIFY(path%tf_sequence)
      NULLIFY(path%vtype_sequence)
      path%valid = .TRUE.
      path%used  = .FALSE.
      path%gridsave  = .FALSE.
      path%refstep = 0
      path%fitting_interface = 0
    END SUBROUTINE path_defaults
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE pgrid_defaults(grid)
      TYPE(Tpropagation_grid)  :: grid
      grid%is_main_grid = .FALSE.
      grid%is_source_grid  = .FALSE.
      grid%nnode = 0
      NULLIFY(grid%r)
      NULLIFY(grid%lat)
      NULLIFY(grid%long)
      NULLIFY(grid%coslat)
      NULLIFY(grid%velocity)
      NULLIFY(grid%arrivaltime)
      NULLIFY(grid%time_gradient)
      NULLIFY(grid%node_region)
      NULLIFY(grid%rnode_id)
      NULLIFY(grid%fully_regular)
      NULLIFY(grid%ccind_from_3dc)
    END SUBROUTINE pgrid_defaults
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE ray_defaults(ray)
      TYPE(Tray)  :: ray
      ray%nsections = 0
      NULLIFY(ray%section)
      NULLIFY(ray%source)
      ray%raypath_id = 0
      ray%source_id = 0
      ray%diffracted = .FALSE.
      ray%headwave = .FALSE.
      ray%is_multiray = .FALSE.
      ray%n_subrays = 0
      NULLIFY(ray%subray)
      ray%n_pdev = 0
      NULLIFY(ray%pdev_indx)
      NULLIFY(ray%pdev)
      ray%valid = .TRUE.
    END SUBROUTINE ray_defaults
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE ray_section_defaults(raysec)
      TYPE(Tray_section) :: raysec
      NULLIFY(raysec%ray)
      NULLIFY(raysec%reg)
      NULLIFY(raysec%istart)
      NULLIFY(raysec%iend)
      NULLIFY(raysec%tf)
      NULLIFY(raysec%source)
      raysec%npoints = 0
      NULLIFY(raysec%point)
      raysec%place_in_sequence = 0
      raysec%diffracted = .FALSE.
      raysec%headwave = .FALSE.
    END SUBROUTINE ray_section_defaults
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE receiver_defaults(rx)
      TYPE(Treceiver) :: rx
      rx%id  = 0
      NULLIFY(rx%arrivaltime)
      rx%n_rays  = 0
      NULLIFY(rx%ray)
      rx%source_equivalent = 0
      NULLIFY(rx%path_equivalent)
    END SUBROUTINE receiver_defaults
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE region_defaults(reg)
      TYPE(Tregion)  :: reg
      reg%id = 0
      reg%ivgrid = 0
      NULLIFY(reg%grid)
      reg%ngnode   = 0
      reg%nnode  = 0
      reg%n_init = 0
      NULLIFY(reg%node)
      NULLIFY(reg%node_status)
      NULLIFY(reg%arrivaltime)
      NULLIFY(reg%time_gradient)
      NULLIFY(reg%velocity)
      NULLIFY(reg%r)
      NULLIFY(reg%lat)
      NULLIFY(reg%long)
      NULLIFY(reg%coslat)
      NULLIFY(reg%init_id)
      NULLIFY(reg%init_arrivaltime)
      NULLIFY(reg%init_time_gradient)
    END SUBROUTINE region_defaults
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE time_field_defaults(tf)
      TYPE(Ttime_field)  :: tf
      tf%id = 0
      tf%vtype = 0
      NULLIFY(tf%reg)
      NULLIFY(tf%istart)
      NULLIFY(tf%inonstart)
      NULLIFY(tf%arrivaltime)
      NULLIFY(tf%time_gradient)
      tf%turning_rays_present = .FALSE.
      NULLIFY(tf%received_turning_ray)
      tf%prev_tf = 0
      tf%next_tf(1:8) = 0
    END SUBROUTINE time_field_defaults
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE triangulation_defaults(tri)
      TYPE(Ttriangulation) :: tri
      tri%npoints = 0
      NULLIFY(tri%points)
      tri%ntriangles = 0
      NULLIFY(tri%points_from_triangle)
      NULLIFY(tri%triangle_neighbours)
      NULLIFY(tri%n_triangles_from_point)
      NULLIFY(tri%triangles_from_point)
    END SUBROUTINE triangulation_defaults
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE vgrid_defaults(grid)
      TYPE(Tvelocity_grid)  :: grid
      grid%to_be_inverted  = .FALSE.
      grid%nnode = 0
      NULLIFY(grid%r)
      NULLIFY(grid%lat)
      NULLIFY(grid%long)
      NULLIFY(grid%velocity)
      NULLIFY(grid%active)
    END SUBROUTINE vgrid_defaults
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
END MODULE typedefn
