!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!SUBROUTINE clean_ray(recID, rayID)
!  USE globals
!  USE typedefn
!  INTEGER              :: recID,&
!                        & rayID
!  TYPE(Tray), POINTER  :: ray
!  IF (receiver(recID)%ray(rayID)%is_multiray) THEN
!    DO isubray=1, receiver(recID)%ray(rayID)%n_subrays
!      ray => receiver(recID)%ray(rayID)%subray(isubray)
!      IF (ASSOCIATED(ray%pdev)) THEN
!        DEALLOCATE(ray%pdev)
!      ENDIF
!      IF (ASSOCIATED(ray%pdev_indx)) THEN
!        DEALLOCATE(ray%pdev_indx)
!      ENDIF
!      DO isec=1, ray%nsections
!        IF (ASSOCIATED(ray%section(isec)%point)) THEN
!          DEALLOCATE(ray%section(isec)%point)
!        ENDIF
!      ENDDO
!    ENDDO
!  ELSE
!    ray => receiver(recID)%ray(rayID)
!    IF (ASSOCIATED(ray%pdev)) THEN
!      DEALLOCATE(ray%pdev)
!    ENDIF
!    IF (ASSOCIATED(ray%pdev_indx)) THEN
!      DEALLOCATE(ray%pdev_indx)
!    ENDIF
!    DO isec=1, ray%nsections
!      IF (ASSOCIATED(ray%section(isec)%point)) THEN
!        DEALLOCATE(ray%section(isec)%point)
!      ENDIF
!    ENDDO
!  ENDIF
!END SUBROUTINE clean_ray
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!SUBROUTINE initialize_source_regions(src)
!!  USE globals
!!  USE typedefn
!!! The source with its properties on the main grid and the secondary
!!! source with its properties on the refined grid.
!!  TYPE(Tsource)                 :: src,&
!!                                 & ssrc
!!! Top and bottom intersections of refined grid and top and bottom
!!! intersection of main grid.
!!  TYPE(Tintersection), POINTER  :: itop,&
!!                                 & ibot,&
!!                                 & itopc,&
!!                                 & ibotc
!!! The source region in the main grid and the refined source region.
!!  TYPE(Tregion), POINTER        :: reg,&
!!                                 & sreg
!!! Construct the refined grid around the source.
!!  ALLOCATE(sgrid)
!!  CALL pgrid_defaults(sgrid)
!!  sgrid%is_source_grid = .TRUE.
!!! Limits of the volume of main grid to be refined, taking main
!!! boundaries into account.
!!  ir       = NINT((src%r - pgrid%r0) / pgrid%dr0 + 1)
!!  ilat     = NINT((src%lat - pgrid%lat0) / pgrid%dlat0 + 1)
!!  ilon     = NINT((src%long - pgrid%long0) / pgrid%dlong0 + 1)
!!  nrmax    = MIN(pgrid%nr, ir + ncell_to_be_refined)
!!  nrmin    = MAX(1, ir - ncell_to_be_refined)
!!  nlatmax  = MIN(pgrid%nlat, ilat + ncell_to_be_refined)
!!  nlatmin  = MAX(1, ilat - ncell_to_be_refined)
!!  nlongmax = MIN(pgrid%nlong, ilon + ncell_to_be_refined)
!!  nlongmin = MAX(1, ilon - ncell_to_be_refined)
!!! Origin of the refined source grid in propagation grid index
!!! coordinates.
!!  sgrid%index_r0    = nrmin
!!  sgrid%index_lat0  = nlatmin
!!  sgrid%index_long0 = nlongmin
!!! Calculate the refined source grid parameters.
!!  sgrid%nr     = (nrmax - nrmin) * refinement_factor + 1
!!  sgrid%nlat   = (nlatmax - nlatmin) * refinement_factor + 1
!!  sgrid%nlong  = (nlongmax - nlongmin) * refinement_factor + 1
!!  sgrid%dr0    = pgrid%dr0 / refinement_factor
!!  sgrid%dlat0  = pgrid%dlat0 / refinement_factor
!!  sgrid%dlong0 = pgrid%dlong0 / refinement_factor
!!  sgrid%r0     = pgrid%r(s%ir) - (s%ir - nrmin) * pgrid%dr0
!!  sgrid%lat0   = pgrid%lat(s%ilat) - (s%ilat - nlatmin) * pgrid%dlat0
!!  sgrid%long0  = pgrid%long(s%ilong) - (s%ilong - nlongmin) * pgrid%dlong0
!!! Initialize the grid coordinates.
!!  ALLOCATE(sgrid%r(sgrid%nr),&
!!         & sgrid%lat(sgrid%nlat),&
!!         & sgrid%long(sgrid%nlong),&
!!         & sgrid%coslat(sgrid%nlat))
!!  DO ir=1, sgrid%nr
!!    sgrid%r(ir) = sgrid%r0 + (ir - 1) * sgrid%dr0
!!  ENDDO
!!  DO ilat=1, sgrid%nlat
!!    sgrid%lat(ilat) = sgrid%lat0 + (ilat - 1) * sgrid%dlat0
!!  ENDDO
!!  DO ilon=1, sgrid%nlong
!!    sgrid%long(ilon) = sgrid%long0 + (ilon - 1) * sgrid%dlong
!!  ENDDO
!!  sgrid%tolerance = refinement_factor * interface_tolerance * sgrid%dr0
!!! Allocate storage for the refined source grid, intersections and
!!! regions.
!!  ALLOCATE(sgrid%rnode_id(sgrid%nr, sgrid%nlat, sgrid%nlong))
!!  sgrid%rnode_id = 0
!!  ALLOCATE(sgrid%node_region(sgrid%nr, sgrid%nlat, sgrid%nlong))
!!  sgrid%node_region = 0
!!  DO ilon=1, sgrid%nlong
!!    DO ilat=1, sgrid%nlat
!!      DO ir=1, sgrid%nr
!!      NULLIFY(sgrid%ccind_from_3dc(ir, ilat, ilon)%p)
!!      ENDDO
!!    ENDDO
!!  ENDDO
!!  ALLOCATE(sgrid%arrivaltime(sgrid%nr, sgrid%nlat, sgrid%nlong))
!!  sgrid%arrival_time = huge_time
!!  n_sinstersections = n_intersections
!!  ALLOCATE(sintersection(n_sintersections))
!!  DO iinter=1, n_sintersections
!!    CALL intersection_defaults(sintersection(iinter))
!!    sintersection(iinter)%id = iinter
!!  ENDDO
!!    n_sregions = n_regions
!!  ALLOCATE(sregion(n_sregions))
!!  DO ireg=1, n_sregions
!!    CALL region_defaults(sregion(ireg))
!!    sregion(ireg)%id = ireg
!!  ENDDO
!!  DO iinter=1, n_sintersections
!!    CALL find_intersection(sintersection(iinter), intrface(iinter), sgrid)
!!    IF (sintersection(iinter)%nnode > 0) THEN
!!      ALLOCATE(sintersection(iinter)%arrivaltime(sintersection(iinter)%nnode))
!!      ALLOCATE(sintersection(iinter)%time_gradient(3, sintersection(iinter)%nnode))
!!    ENDIF
!!  ENDDO
!!! Set a flag at nodes on the grid that are completely regular.
!!! i.e. None of the connected cells has irregular nodes.
!!  CALL tag_regular_ndoes(sgrid)
!!  DO ireg=1, n_sregions
!!    sregion(ireg)%id = ireg
!!! Pointers to the intersections that are the boundaries of the region.
!!    sregion(ireg)%itop   => sintersection(ireg)
!!    sregion(ireg)%ibot   => sintersection(ireg+1)
!!    sregion(ireg)%ivgrid = region(ireg)%ivgrid
!!    IF (sregion(ireg)%itop%nnoe == 0&
!!      & .AND. sregion(ireg)%ibot%nnode == 0&
!!      & .AND. sregion(ireg)%id /= src$region_id) THEN
!!      sregion(ireg)%nnode = 0
!!      CYCLE
!!    ENDIF
!!    CALL define_region(sregion(ireg),&
!!                     & sintersection(ireg),&
!!                     & sintersection(ireg + 1),&
!!                     & sgrid)
!!  ENDDO
!!! Transfer the velocity values to all refined grid nodes
!!  CALL velocities_to_grid(sgrid)
!!  DO iinter=1, n_sintersections
!!    IF (sintersection(iinter)%nnode /= 0) THEN
!!      CALL velocities_to_intersection(sintersection(iinter))
!!    ENDIF
!!  ENDDO
!!  DO ireg=1, n_sregions
!!    IF (sregion(ireg)%nnode > 0) THEN
!!      CALL velocities_to_region(sregion(iinter), sgrid)
!!    ENDIF
!!  ENDDO
!!! Determine the paths up and down from the source region covering the
!!! main regions overlapping with the refined source region. Set default
!!! values for the intialization paths.
!!
!!  DO ii=1, 2
!!    DO ij=1, 2
!!        CALL path_defaults(src%init_path(ii, ij))
!!        src%init_path(ii, ij)%used = .FALSE.
!!    ENDDO
!!  ENDDO
!!! First construct the path up if it exists.
!!  DO vtype=1, n_vtypes
!!    IF (.NOT.(src%on_interface .AND. src%topint_id == 1)) THEN
!!      IF (src%on_interface) THEN
!!        nstart = src%topreg_id - 1
!!      ELSE
!!        nstart = src%region_id - 1
!!      ENDIF
!!      src%init_path(1, vtype)%n_tf = 1
!!! Count the number of timefields up
!!      DO ireg=nstart, 1, -1
!!        IF (sregion(ireg)%nnode > 0) THEN
!!          src%init_path(1, vtype)%n_tf = src%init_path(1, vtype)%n_tf + 1
!!        ENDIF
!!      ENDDO
!!      ALLOCATE(src%init_path(1, vtype)%sequence(2 * src%init_path(1, vtype)%n_tf))
!!      ALLOCATE(src%init_path(1, vtype)%tf_sequence(src%init_path(1, vtype)%n_tf))
!!      src%init_path(1, vtype)%id                = 0
!!      src%init_path(1, vtype)%valid             = .TRUE.
!!      src%init_path(1, vtype)%used              = .TRUE.
!!      src%init_path(1, vtype)%refstep           = 0
!!      src%init_path(1, vtype)%fitting_interface = 0
!!      src%init_path(1, vtype)%sequence(1)       = 0
!!      IF (src%on_interface) THEN
!!        src%init_path(1, vtype)%sequence(2) = region(src%topreg_id)%itop%iface_id
!!      ELSE
!!        src%init_path(1, vtype)%sequence(2) = region(src%region_id)%itop%iface_id
!!      ENDIF
!!! Construct the sequence of the first path.
!!      IF (src%init_path(1, vtype)%n_tf > 1) THEN
!!        DO itf=2, src%init_path(1, vtype)%n_tf
!!          src%init_path(1, vtype)%sequence(2 * itf - 1)&
!!              & = src%init_path(1, vtype)%sequence(2 * itf - 2)
!!          src%init_path(1, vtype)%sequence(2 * itf)&
!!              & = src%init_path(1, vtype)%sequence(2 * itf - 1) - 1
!!        ENDDO
!!      ENDIF
!!    ENDIF
!!! Then construct the path down if it exists.
!!    IF (.NOT.(src%on_interface .AND. src%botint_id == n_interfaces)) THEN
!!      IF (src%on_interface) THEN
!!        nstart = src%botreg_id + 1
!!      ELSE
!!        nstart = s%region_id + 1
!!      ENDIF
!!      src%init_path(2, vtype)%n_tf = 1
!!! Count the number of timefields down
!!      DO ireg=nstart, n_sregions
!!        IF (sregion(ireg)%nnode > 0) THEN
!!          src%init_path(2, vtype)%n_tf = src%init_path(2, vtype)%n_tf + 1
!!        ENDIF
!!      ENDDO
!!      ALLOCATE(src%init_path(2, vtype)%sequence(2 * src%init_path(2, vtype)%n_tf))
!!      ALLOCATE(src%init_path(2, vtype)%sequence(src%init_path(2, vtype)%n_tf))
!!      src%init_path(2, vtype)%id                = 0
!!      src%init_path(2, vtype)%valid             = .TRUE.
!!      src%init_path(2, vtype)%used              = .TRUE.
!!      src%init_path(2, vtype)%refstep           = 0
!!      src%init_path(2, vtype)%fitting_interface = 0
!!      src%init_path(2, vtype)%sequence(1)       = 0
!!      IF (src%on_interface) THEN
!!        src%init_path(2, vtype)%sequence(2) = region(src%botreg_id)%ibot%iface_id
!!      ELSE
!!        src%init_path(2, vtype)%sequence(2) = region(src%region_id)%ibot%iface_id
!!      ENDIF
!!! Construct the sequence of the second path
!!      IF (src%init_path(2, vtype)%n_tf > 1) THEN
!!        DO itf=2, src%init_path(2, vtype)%n_tf
!!          src%init_path(2, vtype)%sequence(2 * itf - 1)&
!!              & = src%init_path(2, vtype)%sequence(2 * itf - 2)
!!          src%init_path(2, vtype)%sequence(2 * itf)&
!!              & = src%init_path(2, vtype)%sequence(2 * itf - 1) + 1
!!        ENDDO
!!      ENDIF
!!    ENDIF
!!  ENDDO
!!
!!END SUBROUTINE initialize_source_regions
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!FUNCTION interpolate_interface(lat, long, iface)
!  USE globals
!  USE typedefn
!  REAL(KIND=dp)               :: lat, long
!  TYPE(Tinterface)            :: iface
!  INTEGER                     :: i, j, ilat, ilong
!  REAL(KIND=dp)               :: u, v, bu(4), bv(4)
!  REAL(KIND=dp)               :: interpolate_interface, valu
!  ilat  = FLOOR((lat  - iface%lat0 ) / iface%dlat0)  + 1
!  ilong = FLOOR((long - iface%long0) / iface%dlong0) + 1
!  IF (ilong < 2 .OR. ilong > (iface%nlong - 2)) THEN
!    PRINT *,"ERROR:: interpolation outside longitude domain"
!  ENDIF
!  IF (ilat < 2 .or. ilat > (iface%nlat - 2)) THEN
!    PRINT *,"ERROR:: interpolation outside latitude domain"
!  ENDIF
!  u = (lat  - iface%lat(ilat)  ) / iface%dlat0
!  v = (long - iface%long(ilong)) / iface%dlong0
!  bu(1) = (1.0_dp - u) ** 3 / 6.0_dp
!  bu(2) = (4.0_dp - 6.0_dp * u ** 2 + 3.0_dp * u ** 3) / 6.0_dp
!  bu(3) = (1.0_dp + 3.0 * u + 3.0_dp * u ** 2 - 3.0_dp * u ** 3) / 6.0_dp
!  bu(4) = u ** 3 / 6.0_dp
!  bv(1) = (1.0_dp - v) ** 3 / 6.0_dp
!  bv(2) = (4.0_dp - 6.0_dp * v ** 2 + 3.0_dp * v ** 3) / 6.0_dp
!  bv(3) = (1.0_dp + 3.0 * v + 3.0_dp * v ** 2 - 3.0_dp * v ** 3) / 6.0_dp
!  bv(4) = v ** 3 / 6.0_dp
!  valu  = 0.0_dp
!  DO j=1, 4
!    DO i=1, 4
!        valu = valu + bu(i) * bv(j) * iface%r(ilat + i - 2, ilong + j - 2)
!    ENDDO
!  ENDDO
!  interpolate_interface = valu
!END FUNCTION interpolate_interface
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
MODULE core
  use globals
  use typedefn
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  CONTAINS
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE march
      INTEGER                      :: isrc,&
                                    & ipath,&
                                    & itf,&
                                    & istep,&
                                    & prev_tf,&
                                    & ctype,&
                                    & vtype,&
                                    & pathID,&
                                    & direction
      TYPE(Tsource), POINTER       :: src
      TYPE(Tpath), POINTER         :: path
      TYPE(Tintersection), POINTER :: istart,&
                                    & inext
      TYPE(Tregion), POINTER       :: reg
      TYPE(Tray), POINTER          :: ray
      global_source_counter = 0
      DO isrc=1, n_sources_ppinc
        src => source(isrc)
! First evaluate the initial time fields of the sequences starting at
! the source.
        IF (src%is_local) THEN
! Do the first sweep from the source through the regions overlapping
! source grid. This is a big subroutine that does the entire grid
! refinement procedure around the source. The call to this subroutine
! takes a significant part of the computation time.
          CALL initialize_source_regions(src)
        ELSE
          CALL initialize_teleseismic_source(src)
        ENDIF
        PRINT *, '# time fields from initialization',src%n_time_fields
        PATHLOOP: DO ipath=1, src%n_paths
          path => src%path(ipath)
          vtype = path%vtype_sequence(1)
! Identify the first time field of the path, created during
! initialization above.
          IF (src%is_local) THEN
            IF (src%on_interface) THEN
              IF (path%sequence(2) == src%topint_id - 1) THEN
                prev_tf = src%first_tf_up(vtype)
              ENDIF
              IF (path%sequence(2) == src%botint_id + 1) THEN
                prev_tf = src%first_tf_down(vtype)
              ENDIF
            ELSE
              prev_tf = src%first_tf_up(vtype)
            ENDIF
          ENDIF
          IF (src%is_teleseismic) THEN
            prev_tf = src%first_tf_up(vtype)
          ENDIF
          path%tf_sequence(1) = prev_tf
          print '(a5,i4,a35,i4)', &
            'path',path%id,' leg  1  using source time field',prev_tf
! Now go throught the specified seuqnce of the path.
          DO itf=3, 2*path%n_tf, 2
            istep = (itf + 1) / 2
            vtype = path%vtype_sequence(istep)
! Intersection at which the sweep starts
            istart => intersection(path%sequence(itf))
! Intersection at which the sweep ends
            inext => intersection(path%sequence(itf + 1))
            IF (istart%id > inext%id) THEN
              reg => istart%regabo
            ELSE
              reg => istart%regbel
            ENDIF
            print '(a5,i4,a5,i4,a16,i4,a5,i4,a16,i4)', 'path',path%id, &
              ' leg',istep,' from interface',istart%id,'to',inext%id,'through region',reg%id
! Set the child type of the next time field (up, down, turning,
! non-turning)
! If the previous time field is not a source time field
            IF (istep > 2) THEN
              PRINT *, "Previous time field is not a source time field"
              IF (istart%id == src%time_field(prev_tf)%inonstart%id) THEN
                IF (istart%id > inext%id) THEN
                  PRINT *, vtype, 1 + (vtype-1)*4
                  ctype = 1 + (vtype - 1) * 4
                ENDIF
                IF (istart%id < inext%id) THEN
                  PRINT *, vtype, 2 + (vtype-1)*4
                  ctype = 2 + (vtype - 1) * 4
                ENDIF
              ELSE
! If the next required timefield is derived from a turning ray, check
! if turning rays are indeed present
                IF (.NOT. src%time_field(prev_tf)%turning_rays_present) THEN
                  print '(a5,i4,a5,i4,a44)', &
                    'path',ipath,' leg',istep,'no turning rays present, non-existing path'
                  path%valid = .FALSE.
                  CYCLE PATHLOOP
                ENDIF
                IF (istart%id > inext%id) THEN
                  ctype = 3 + (vtype - 1) * 4
                ENDIF
                IF (istart%id < inext%id) THEN
                  ctype = 4 + (vtype - 1) * 4
                ENDIF
              ENDIF
            ELSE
! Only if the previous setp is a source time field.
              PRINT *,'previous step is a source time field'
              IF (istart%id == src%time_field(prev_tf)%reg%itop%id) THEN
                IF (istart%id > inext%id) THEN
! Propagate upwards
                  ctype = 1 + (vtype - 1) * 4
                ENDIF
! Propagate downwards
                IF (istart%id < inext%id) THEN
                  ctype = 2 + (vtype - 1) * 4
                ENDIF
              ELSE
                IF (istart%id > inext%id) THEN
                  ctype = 3 + (vtype - 1) * 4
                ENDIF
                IF (istart%id < inext%id) THEN
                  ctype = 4 + (vtype - 1) * 4
                ENDIF
              ENDIF
            ENDIF
            IF (src%time_field(prev_tf)%next_tf(ctype) == 0) THEN
! If the required time field does not exist, transfer the starting
! times to the starting intersection. Here we use the fact that
! regional (and thus timefield) nodes are always in the same order:
! - regular grid nodes
! - top intersection grid nodes
! - bottom intersection grid nodes
              IF (istart%id == src%time_field(prev_tf)%reg%ibot%id) THEN
                inode = src%time_field(prev_tf)%reg%nnode - istart%nnode + 1
                jnode = src%time_field(prev_tf)%reg%nnode
                istart%arrivaltime =&
                    & src%time_field(prev_tf)%arrivaltime(inode:jnode)
                istart%time_gradient(1,:) =&
                    & src%time_field(prev_tf)%time_gradient(1,inode:jnode)
                istart%time_gradient(2,:) =&
                    & src%time_field(prev_tf)%time_gradient(2,inode:jnode)
                istart%time_gradient(3,:) =&
                    & src%time_field(prev_tf)%time_gradient(3,inode:jnode)
              ELSE
                inode = src%time_field(prev_tf)%reg%ngnode + 1
                jnode = src%time_field(prev_tf)%reg%ngnode + istart%nnode
                istart%arrivaltime =&
                    & src%time_field(prev_tf)%arrivaltime(inode:jnode)
                istart%time_gradient(1,:) =&
                    & src%time_field(prev_tf)%time_gradient(1,inode:jnode)
                istart%time_gradient(2,:) =&
                    & src%time_field(prev_tf)%time_gradient(2,inode:jnode)
                istart%time_gradient(3,:) =&
                    & src%time_field(prev_tf)%time_gradient(3,inode:jnode)
              ENDIF
! Modify the time gradients at the interface for the next leg of the
! path.
              IF (reg%id == src%time_field(prev_tf)%reg%id) THEN
! If we go back into the same region as the previous time field, it is
! a reflection. Convert the direction of the gradient and set the
! arrival time at the intersection points where reflection is
! impossible (due to wave-type conversion) to huge_time so that they do
! not act as a source
                CALL reflect_gradient(istart, src%time_field(prev_tf), vtype)
              ELSE
! If the next region is another region, it is a refraction. Convert the
! direction of the gradient and set the arrival time at the
! intersection points where total reflection occurs to huge_time so
! that they do not act as a source.
                direction = src%time_field(prev_tf)%reg%id - reg%id
                CALL refract_gradient(istart,&
                                    & src%time_field(prev_tf)%reg,&
                                    & vtype,&
                                    & direction)
              ENDIF
! We are finally set up, now do the actual fast marching across the
! region, generating a new time field.
              CALL sweep_region_from_interface(reg, istart, vtype, src)
! Attach info to the generated time field.
! Time field preceding the current one.
              src%time_field(src%n_time_fields)%prev_tf = prev_tf
! Identify the current time field as the child of the previous time
! field.
              src%time_field(prev_tf)%next_tf(ctype) = src%n_time_fields
! Store the index of the time field in the sequence of timefields for
! this path.
              path%tf_sequence(istep) = src%n_time_fields
! Pointers to start and non-start interfaces.
              src%time_field(src%n_time_fields)%istart    => istart
              src%time_field(src%n_time_fields)%inonstart => inext
              src%time_field(src%n_time_fields)%reg       => reg
              src%time_field(src%n_time_fields)%vtype     =  vtype
              prev_tf = src%n_time_fields
              print *,'created new time field',src%n_time_fields
            ELSE
! The required time field already exists.
! Step to the next (existing) time field.
              prev_tf = src%time_field(prev_tf)%next_tf(ctype)
              path%tf_sequence(istep) = prev_tf
              print *,'used existing time field',prev_tf
            ENDIF
          ENDDO
        ENDDO PATHLOOP
        DO ipath=1, src%n_paths
          path => src%path(ipath)
          PRINT '(a5,i5,a12,10i5)','path',path%id,' timefields',path%tf_sequence(1:path%n_tf)
        ENDDO
!!!!!
! Save the arrival times on the main grid for this path if requested.
! This is where the original code writes the travel-time grid.
!!!!!
!!!!!
! TODO: This is where ray tracing is performed in no_pp_mode.
!!!!!
! Deallocate source specific variables that are not needed any more.
        DO itf=1, src%n_time_fields
          IF (ASSOCIATED(src%time_field(itf)%received_turning_ray)) THEN
            DEALLOCATE(src%time_field(itf)%received_turning_ray)
          ENDIF
        ENDDO
        IF (src%is_teleseismic) THEN
          DO ireg=1, n_regions
            reg => region(ireg)
            IF (reg%n_init > 0) THEN
              DEALLOCATE(reg%init_id,&
                       & reg%init_type,&
                       & reg%init_arrivaltime,&
                       & reg%init_time_gradient)
            ENDIF
          ENDDO
          reg%n_init = 0
        ENDIF
        IF (no_pp_mode) THEN
          DO itf=1, src%n_time_fields
            DEALLOCATE(src%time_field(itf)%arrivaltime,&
                     & src%time_field(itf)%time_gradient)
          ENDDO
        ENDIF
      ENDDO
! This is the end of the source loop.
! Now do the ray tracing if not in no_pp_mode
      IF (n_receivers > 0 .AND. (.NOT.no_pp_mode)) THEN
! TODO: Initialize inversion here.
        raypoint_counter = 0
        DO irec=1, n_receivers
          DO iray=1, receiver(irec)%n_rays
            ray => receiver(irec)%ray(iray)
            src => ray%source
            pathID = ray%raypath_id
            IF (src%path(pathID)%valid) THEN
! The original path was recognized as valid during the time fields
! calculation.
              IF (src%path(pathID)%refstep == 0) THEN
                CALL trace_ray_from_receiver(receiver(irec), src, ray)
                IF (ray%valid) THEN
! Valid ray path found.
                  k = 0
                  PRINT '(a12,i4,a10,i4,a15,i4,a4,f10.4,2l5)',&
                    & 'traced ray',&
                    & iray,&
                    & 'to source',&
                    & src%id,&
                    & ' from receiver',&
                    & irec,&
                    &'  t=',&
                    & ray%receiver_time,&
                    & ray%diffracted,&
                    & ray%headwave
                ELSE
                  k = 0
                  t_arrival = -1.0_dp
                ENDIF
              ENDIF
              IF (src%path(pathID)%refstep /= 0) THEN
                CALL trace_reflectionfit(irec, iray)
              ENDIF
! TODO: Some frechet derivatives related processing goes here.
            ELSE
! The original path was recognized as invalid during the timefield
! calculations
              ray%valid = .FALSE.
              k = 0
              t_arrival = -1.0_dp
            ENDIF
! IF THE RAY IS CLEANED UP HERE, WE CAN'T RETRIEVE ITS DATA!!!
! IT NEEDS TO BE CLEANED UP ELSEWHERE!
            !CALL clean_ray(irec, iray)
          ENDDO ! loop over rays/paths
        ENDDO ! loop over receivers
      ENDIF
    END SUBROUTINE march
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    FUNCTION get_nsources()
      INTEGER :: get_nsources
      get_nsources = n_sources
    END FUNCTION get_nsources
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    FUNCTION get_nrays(recID)
      INTEGER :: get_nrays,&
               & recID
      get_nrays = receiver(recID)%n_rays
    END FUNCTION get_nrays
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    FUNCTION get_nreceivers()
      INTEGER :: get_nreceivers
      get_nreceivers = n_receivers
    END FUNCTION get_nreceivers
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    FUNCTION get_nsections(recID, rayID)
      INTEGER :: get_nsections,&
               & recID,&
               & rayID
      get_nsections = receiver(recID)%ray(rayID)%nsections
    END FUNCTION get_nsections
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    FUNCTION get_npoints(recID, rayID, secID)
      INTEGER :: get_npoints,&
               & recID,&
               & rayID,&
               & secID
      get_npoints = receiver(recID)%ray(rayID)%section(secID)%npoints
    END FUNCTION get_npoints
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    FUNCTION get_ray_section(recID, rayID, secID, npts)
      INTEGER   :: recID,&
                 & rayID,&
                 & secID,&
                 & npts
      REAL      :: get_ray_section(3,npts)
      get_ray_section = receiver(recID)%ray(rayID)%section(secID)%point(1:3,1:npts)
    END FUNCTION get_ray_section
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    FUNCTION get_ray_arrival_time(recID, rayID)
      INTEGER   :: recID,&
                 & rayID
      REAL      :: get_ray_arrival_time
      get_ray_arrival_time = receiver(recID)%ray(rayID)%receiver_time
    END FUNCTION get_ray_arrival_time
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
END MODULE core
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
MODULE fmm3dlib
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  USE typedefn
  USE globals
  USE interface_definitions
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
END MODULE fmm3dlib
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
MODULE fmm3dlib_noint
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  USE typedefn
  USE globals
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
END MODULE fmm3dlib_noint
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
