MODULE initialize
  USE fmm3dlib
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  CONTAINS
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE allocate_receivers(n)
      INTEGER, INTENT(IN)   :: n
      INTEGER               :: rxID
      ALLOCATE(receiver(n))
      n_receivers = n
      DO rxID=1,n_receivers
        CALL receiver_defaults(receiver(rxID))
        receiver(rxID)%id = rxID
      END DO
    END SUBROUTINE allocate_receivers
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE allocate_sources(n)
      INTEGER, INTENT(IN)     :: n
      INTEGER                 :: srcID
      TYPE(Tsource), POINTER  :: src
      ALLOCATE(source(n + n_receivers))
      n_sources = n
      DO srcID = 1, n_sources + n_receivers
        CALL source_defaults(source(srcID))
        source(srcID)%id = srcID
      ENDDO
! Will contain the number of sources including receivers of pp phases.
      n_sources_ppinc = n_sources
! Will contain the number of teleseismic sources.
      n_teleseismic = 0
    END SUBROUTINE allocate_sources
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  SUBROUTINE allocate_vgrids(nvgrids,&
                           & nvtypes)
    INTEGER, INTENT(IN)  :: nvgrids,&
                          & nvtypes
    n_vgrids = nvgrids
    n_vtypes = nvtypes
! Allocate storage for the velocity grids.
    ALLOCATE(vgrid(n_vgrids, n_vtypes))
    DO ivtype=1, n_vtypes
      DO igrid=1, n_vgrids
        CALL vgrid_defaults(vgrid(igrid, ivtype))
      ENDDO
    ENDDO
  END SUBROUTINE allocate_vgrids
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SUBROUTINE define_interfaces(intrfaces,&
                               & ninter,&
                               & nlat, nlon,&
                               & lat0, lon0,&
                               & dlat, dlon)
      INTEGER, INTENT(IN)         :: ninter,&
                                   & nlat,&
                                   & nlon
      REAL, INTENT(IN)            :: intrfaces(ninter, nlat, nlon),&
                                   & lat0, lon0,&
                                   & dlat, dlon
      INTEGER                     :: iinter, i, j
      REAL(KIND=dp)               :: h, hb
      TYPE(Tinterface), POINTER   :: intr
      n_interfaces = ninter
! Allocate space for these interfaces (and the associated intersections
! and regions for future use).
      ALLOCATE(intrface(n_interfaces))
      DO iinter=1, n_interfaces
        CALL interface_defaults(intrface(iinter))
        intrface(iinter)%id = iinter
      ENDDO
! Read the grid properties and radius values to be interpolated for the
! internal interfaces.
      ! grid parameters
      DO iinter=1, n_interfaces
        intr => intrface(iinter)
        intr%lat0   = lat0 * deg_to_rad
        intr%long0  = lon0 * deg_to_rad
        intr%nlat   = nlat
        intr%nlong  = nlon
        intr%dlat0  = dlat * deg_to_rad
        intr%dlong0 = dlon * deg_to_rad
! Initialize the grid.
        ALLOCATE(intr%lat(intr%nlat), intr%long(intr%nlong))
        DO ilat=1, intr%nlat
            intr%lat(ilat) = intr%lat0 + (ilat - 1) * intr%dlat0
        ENDDO
        DO ilon=1, intr%nlong
            intr%long(ilon) = intr%long0 + (ilon - 1) * intr%dlong0
        ENDDO
! Read in the radius values on the interpolation grid.
        ALLOCATE(intr%r(intr%nlat, intr%nlong))
        DO ilat=1, intr%nlat
          DO ilon=1, intr%nlong
            !intr%r(ilat, ilon) = intrfaces(iinter, ilat, ilon)
            intr%r(ilon, ilat) = intrfaces(iinter, ilon, ilat)
          ENDDO
        ENDDO
        intr%nnode = intr%nlat * intr%nlong
      ENDDO
! Correct for intersecting interfaces, higher takes priority.
      DO iinter=2, n_interfaces
          intr => intrface(iinter)
        DO ilon=1, intr%nlong
          DO ilat=1, intr%nlat
! Higher has priority, EXCEPT bottom interface.
            IF (iinter < n_interfaces) THEN
              hb = intrface(n_interfaces)%r(ilat,ilon)
              IF (intr%r(ilat, ilon) < hb) THEN
                intr%r(ilat, ilon) = hb
                intr%pinched = .TRUE.
                intrface(n_interfaces)%pinched = .TRUE.
              ENDIF
            ENDIF
! Check if interface above is crossed.
            h=intrface(iinter-1)%r(ilat, ilon)
            IF (intr%r(ilat, ilon) > h) THEN
              intr%r(ilat, ilon) = h
              intr%pinched = .TRUE.
              intrface(iinter-1)%pinched = .TRUE.
            ENDIF
          ENDDO
        ENDDO
      ENDDO
  END SUBROUTINE define_interfaces
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  SUBROUTINE define_propagation_grid(lat0, lon0, depth0,&
                                   & nlat, nlon, ndepth,&
                                   & dlat, dlon, ddepth)
    INTEGER, INTENT(IN)           :: nlat,&
                                   & nlon,&
                                   & ndepth
    REAL, INTENT(IN)              :: lat0,&
                                   & lon0,&
                                   & depth0,&
                                   & dlat,&
                                   & dlon,&
                                   & ddepth
    ALLOCATE(pgrid)
    CALL pgrid_defaults(pgrid)

! Grid parameters.
    pgrid%nr        = ndepth
    pgrid%nlat      = nlat
    pgrid%nlong     = nlon
    pgrid%dr0       = ddepth
    pgrid%dlat0     = dlat
    pgrid%dlong0    = dlon
    pgrid%lat0      = lat0
    pgrid%long0     = lon0
    pgrid%r0        = earth_radius - depth0 - dble(pgrid%nr - 1) * pgrid%dr0
    pgrid%dlat0     = pgrid%dlat0  * deg_to_rad
    pgrid%dlong0    = pgrid%dlong0 * deg_to_rad
    pgrid%lat0      = pgrid%lat0   * deg_to_rad
    pgrid%long0     = pgrid%long0  * deg_to_rad
    pgrid%tolerance = interface_tolerance * pgrid%dr0
    pgrid%rmax      = pgrid%r0    + (pgrid%nr    - 1) * pgrid%dr0
    pgrid%latmax    = pgrid%lat0  + (pgrid%nlat  - 1) * pgrid%dlat0
    pgrid%longmax   = pgrid%long0 + (pgrid%nlong - 1) * pgrid%dlong0
    refinement_factor   = 5
    ncell_to_be_refined = 10
! Initialize the grid.
    ALLOCATE(pgrid%r(pgrid%nr),&
           & pgrid%lat(pgrid%nlat),&
           & pgrid%coslat(pgrid%nlat),&
           & pgrid%long(pgrid%nlong))
    DO ir=1, pgrid%nr
      pgrid%r(ir) = pgrid%r0 + (ir - 1) * pgrid%dr0
    ENDDO
    DO ilat=1, pgrid%nlat
      pgrid%lat(ilat) = pgrid%lat0 + (ilat - 1) * pgrid%dlat0
    ENDDO
    DO ilon=1, pgrid%nlat
      pgrid%coslat(ilon) = cos(pgrid%lat(ilon))
    ENDDO
    DO ilon=1, pgrid%nlong
      pgrid%long(ilon) = pgrid%long0 + (ilon - 1) * pgrid%dlong0
    ENDDO
    ALLOCATE(pgrid%rnode_id(pgrid%nr, pgrid%nlat, pgrid%nlong))
    ALLOCATE(pgrid%node_region(pgrid%nr, pgrid%nlat, pgrid%nlong))
    pgrid%node_region = 0
    ALLOCATE(pgrid%ccind_from_3dc(pgrid%nr, pgrid%nlat, pgrid%nlong))
    DO ilon=1, pgrid%nlong
      DO ilat=1, pgrid%nlat
        DO ir=1, pgrid%nr
          NULLIFY(pgrid%ccind_from_3dc(ir, ilat, ilon)%p)
        ENDDO
      ENDDO
    ENDDO

    pgrid%is_main_grid = .TRUE.
  END SUBROUTINE define_propagation_grid
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  SUBROUTINE define_receiver(rxID,&
                           & lat,&
                           & lon,&
                           & depth,&
                           & n_rays,&
                           & source_ids,&
                           & path_ids)
      INTEGER, INTENT(IN)       :: rxID,&
                                 & n_rays,&
                                 & source_ids(n_rays),&
                                 & path_ids(n_rays)
      REAL, INTENT(IN)          :: lat,&
                                 & lon,&
                                 & depth
      INTEGER                   :: rayID
      TYPE(Treceiver), POINTER  :: rx
! Initialize receiver coordinates
      rx => receiver(rxID)
      rx%r = earth_radius - depth
      rx%lat = lat*deg_to_rad
      rx%long = lon*deg_to_rad
      rx%n_rays = n_rays
! Check that the receiver is within the latitude and longitude limits
! of the propagation grid here.
! Check also that the receiver lies in the region between the bounding
! surfaces.
! Allocate memory for the ray paths and initialize rays with default
! values.
    ALLOCATE(rx%ray(n_rays))
    DO rayID=1,n_rays
      CALL ray_defaults(rx%ray(rayID))
      rx%ray(rayID)%source_id = source_ids(rayID)
      rx%ray(rayID)%raypath_id = path_ids(rayID)
      rx%ray(rayID)%source => source(source_ids(rayID))
! Verify that ray path references are valid here.
    ENDDO
  END SUBROUTINE define_receiver
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  SUBROUTINE define_source(srcID,&
                             & is_tele,&
                             & lat,&
                             & lon,&
                             & depth,&
                             & n_paths)
    INTEGER, INTENT(IN)           :: srcID,&
                                   & n_paths
    REAL, INTENT(IN)              :: lat,&
                                   & lon,&
                                   & depth
    LOGICAL, INTENT(IN)           :: is_tele
    INTEGER                       :: pathID
    !CHARACTER(LEN=8), INTENT(IN)  :: tele_phase
    TYPE(Tsource), POINTER        :: src
    PRINT *, "define_source()", srcID
    src => source(srcID)
    src%is_teleseismic = is_tele
    IF (src%is_teleseismic) THEN
      n_teleseismic = n_teleseismic + 1
      !src%teleseismic_phase = phase
    ELSE
      src%is_local = .TRUE.
      src%r = earth_radius - depth
      src%lat = lat * deg_to_rad
      src%long = lon * deg_to_rad
      src%coslat = cos(src%lat)
! Determines where the source is located wrt grid/intersections.
      CALL initialize_source(src, pgrid)
    ENDIF
    src%n_paths = n_paths
! Allocate the array containing path information for this source.
    ALLOCATE(src%path(n_paths))
    DO pathID=1,n_paths
      CALL path_defaults(src%path(pathID))
    ENDDO
    DO pathID=1,n_paths
      src%path(pathID)%id = pathID
    ENDDO
  END SUBROUTINE define_source
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  SUBROUTINE define_path(srcID,&
                       & pathID,&
                       & n_steps,&
                       & steps,&
                       & vtypes)
    INTEGER, INTENT(IN)           :: srcID,&
                                   & pathID,&
                                   & n_steps,&
                                   & steps(n_steps, 2),&
                                   & vtypes(n_steps)
    INTEGER                       :: istep
    TYPE(Tpath), POINTER          :: path
! TODO: There are a number of consistency checks done in the original
! code to validate the paths that I have left out. I will probably do
! these on the Python end.
    path => source(srcID)%path(pathID)
    path%n_tf = n_steps
    ALLOCATE(path%sequence(2 * n_steps))
    ALLOCATE(path%tf_sequence(n_steps))
    ALLOCATE(path%vtype_sequence(n_steps))
    DO istep=1,n_steps
      path%sequence(istep*2 - 1) = steps(istep, 1)
      path%sequence(istep*2) = steps(istep, 2)
      path%vtype_sequence(istep) = vtypes(istep)
! Check whether the path contains a reflection fit step. Store the
! number of the step if so.
      IF (path%sequence(istep*2 - 1) == path%sequence(istep * 2)) THEN
        path%refstep = istep
        path%fitting_interface = path%sequence(istep * 2)
      ENDIF
    ENDDO
  END SUBROUTINE define_path
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  SUBROUTINE define_vgrid(vtypeID,&
                        & gridID,&
                        & values,&
                        & r0,&
                        & lambda0,&
                        & phi0,&
                        & nr,&
                        & nlambda,&
                        & nphi,&
                        & dr,&
                        & dlambda,&
                        & dphi)
    INTEGER, INTENT(IN)            :: vtypeID,&
                                    & gridID,&
                                    & nlambda,&
                                    & nphi,&
                                    & nr
    REAL, INTENT(IN)               :: values(nr, nlambda, nphi),&
                                    & lambda0,&
                                    & phi0,&
                                    & r0,&
                                    & dlambda,&
                                    & dphi,&
                                    & dr
    INTEGER                        :: ir,&
                                    & ilambda,&
                                    & iphi
    TYPE(Tvelocity_grid), POINTER  :: vg
    vg => vgrid(gridID, vtypeID)
    vg%lat0   = lambda0
    vg%long0  = phi0
    vg%r0     = r0
    vg%nlat   = nlambda
    vg%nlong  = nphi
    vg%nr     = nr
    vg%dr0    = dr
    vg%dlat0  = dlambda
    vg%dlong0 = dphi
! Allocate storage for grid coordinates.
    ALLOCATE(vg%r(vg%nr), vg%lat(vg%nlat), vg%long(vg%nlong))
! Initialize grid coordinates.
    DO ir=1, vg%nr
      vg%r(ir) = vg%r0 + (ir - 1) * vg%dr0
    ENDDO
    DO ilambda=1, vg%nlat
      vg%lat(ilambda) = vg%lat0 + (ilambda - 1) * vg%dlat0
    ENDDO
    DO iphi=1, vg%nlong
      vg%long(iphi) = vg%long0 + (iphi - 1) * vg%dlong0
    ENDDO
! Allocate storage for velocity values
    ALLOCATE(vg%velocity(vg%nr, vg%nlat, vg%nlong))
! Initialize velocity values.
    DO ir=1, vg%nr
      DO ilambda=1, vg%nlat
        DO iphi=1, vg%nlong
          vg%velocity(ir, ilambda, iphi) = values(ir, ilambda, iphi)
        ENDDO
      ENDDO
    ENDDO
    vg%nnode = vg%nr * vg%nlat * vg%nlong
! Allocate storage for the activity flag
    ALLOCATE(vg%active(vg%nr, vg%nlat, vg%nlong))
! Initialize activity flags.
    vg%active = .FALSE.
  END SUBROUTINE define_vgrid
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  SUBROUTINE finalize_definitions
! This subroutine is intended to perform any validation/consistency
! checks that have been left out so far.
! Verify that path references are valid.
    INTEGER                               :: rxID,&
                                           & rayID,&
                                           & pathID,&
                                           & recpathID,&
                                           & nsteps,&
                                           & irx, iray, ipath, isrc,&
                                           & istep, jstep,&
                                           & i1, i2,&
                                           & top_id, bot_id,&
                                           & max_n_tf, itf
    INTEGER, DIMENSION(:), ALLOCATABLE    :: npp_receiver,&
                                           & ipp_receiver
    TYPE(Tpath), POINTER                  :: path,&
                                           & pathpp
    TYPE(Tray), POINTER                   :: ray
    TYPE(Treceiver), POINTER              :: rx
    TYPE(Tsource), POINTER                :: src,&
                                           & srcpp
    REAL(KIND=dp)                         :: interpolate_interface
! Initialize intersections (interface grid + navigation pointers) and
! regions (collection of grid points between two interfaces, including
! the bounding intersections). The fast marching solution is evaluated
! region by region.
! Calculate intersection points, i.e. where the surfaces cut through
! the regular propagation grid.
    n_intersections = n_interfaces
    ALLOCATE(intersection(n_intersections))
    DO iinter=1, n_intersections
      CALL intersection_defaults(intersection(iinter))
      intersection(iinter)%id = iinter
    ENDDO
    DO iinter=1, n_intersections
      CALL find_intersection(intersection(iinter), intrface(iinter), pgrid)
    ENDDO
! Set up the 3D regions that lie between the interfaces.
    n_regions = n_interfaces - 1
    ALLOCATE(region(n_regions))
    DO ireg=1, n_regions
      CALL region_defaults(region(ireg))
      region(ireg)%id = ireg
! Pointers to the intersections that are the boundaries of the region.
      region(ireg)%itop => intersection(ireg)
      region(ireg)%ibot => intersection(ireg + 1)
      IF (region(ireg)%itop%nnode == 0) THEN
        PRINT *,"region",ireg,"does not exist"
        region(ireg)%nnode = 0
        CYCLE
      ENDIF
      CALL define_region(region(ireg),&
                       & region(ireg)%itop,&
                       & region(ireg)%ibot,&
                       & pgrid)
    ENDDO
    PRINT *, "main grid regions intialized"
! Set a flag at each node of the main grid that has only regular
! connected cells. This is used later to speed up calculations.
! Intersections have to be initialized to do this.
    CALL tag_regular_nodes(pgrid)
    PRINT *, "regular nodes tagged"
! Calculate the velocities on the regular grid and intersection grid
! points and transfer them to the corresponding regional nodes.
    CALL velocities_to_grid(pgrid)
    PRINT *, "velocities on regular grid calculated"
    DO iinter=1, n_intersections
      CALL velocities_to_intersection(intersection(iinter))
    ENDDO
    PRINT *, "velocities on intersections calculated"
    DO ireg=1, n_regions
      CALL velocities_to_region(region(ireg), pgrid)
    ENDDO
    PRINT *, "velocities on main grid, its intersections and regions evaluated."
    DO rxID=1,n_receivers
      rx => receiver(rxID)
      DO rayID=1,rx%n_rays
        ray => rx%ray(rayID)
        IF (ray%raypath_id > ray%source%n_paths) THEN
          PRINT *,"ERROR:: undefined path"
          PRINT *,"     :: receiver", rx%id
          PRINT *,"     :: raypath", ray%raypath_id
          PRINT *,"     :: source", ray%source%id
        ENDIF
        src => ray%source
        IF (src%is_teleseismic) CYCLE
        pathID = ray%raypath_id
        nsteps = src%path(pathID)%n_tf
        IF (nsteps > 1) THEN
          i1 = src%path(pathID)%sequence(2 * nsteps)
          i2 = src%path(pathID)%sequence(2 * nsteps - 1)
          top_id = MIN(i1, i2)
          bot_id = MAX(i1, i2)
          IF ((rx%r > interpolate_interface(rx%lat,&
                                          & rx%long,&
                                          & intrface(top_id))&
                    & + pgrid%tolerance) .OR.&
             &(rx%r < interpolate_interface(rx%lat,&
                                          & rx%long,&
                                          & intrface(bot_id))&
                    & - pgrid%tolerance)) THEN
            PRINT *,"ERROR:: receiver error"
            PRINT *,"     :: receiver does not lie in final time field"
            PRINT *,"     :: receiver", rx%id
          ENDIF
        ELSE
          IF (src%on_interface) THEN
            top_id = max(1, src%topint_id - 1)
            bot_id = min(n_interfaces, src%botint_id + 1)
            IF ((rx%r > interpolate_interface(rx%lat,&
                                           & rx%long,&
                                           & intrface(top_id))&
                     & + pgrid%tolerance) .OR. &
                (rx%r < interpolate_interface(rx%lat,&
                                            & rx%long,&
                                            & intrface(bot_id))&
                     & - pgrid%tolerance)) THEN
              PRINT *,"ERROR:: receiver error"
              PRINT *,"     :: receiver does not lie in final time field"
              PRINT *,"     :: receiver", rx%id
            ENDIF
          ELSE
            top_id = src%region_id
            bot_id = src%region_id
            IF ((rx%r > interpolate_interface(rx%lat,&
                                           & rx%long,&
                                           & intrface(top_id))&
                     & + pgrid%tolerance) .OR. &
                (rx%r < interpolate_interface(rx%lat,&
                                            & rx%long,&
                                            & intrface(bot_id))&
                     & - pgrid%tolerance)) THEN
              PRINT *,"ERROR:: receiver error"
              PRINT *,"    :: receiver does not lie in final time field"
              PRINT *,"    :: receiver", rx%id
            ENDIF
          ENDIF
        ENDIF
      ENDDO
    ENDDO
! Test which paths are actually used, and pre-count the number of
! pp-phases arriving at this receiver.
    ALLOCATE(npp_receiver(n_receivers), ipp_receiver(n_receivers))
! Will contain the number of pp phases arriving at this receiver.
    npp_receiver = 0
! A counter for pp-phases.
    ipp_receiver = 1
    DO irx=1, n_receivers
      rx => receiver(irx)
      DO iray=1,rx%n_rays
        ray => rx%ray(iray)
        src => ray%source
        pathID = ray%raypath_id
        src%path(pathID)%used = .TRUE.
        IF (src%path(pathID)%refstep /= 0) THEN
! We have a pp type phase.
          npp_receiver(n) = npp_receiver(n) + 1
        ENDIF
      ENDDO
    ENDDO
! Add receivers of pp-type phases to the source list, and construct
! their path sequences by inverting the tail end of the original
! pp-type sequence.
  DO irx=1, n_receivers
    rx => receiver(irx)
    IF (npp_receiver(irx) > 0) THEN
      ALLOCATE(rx%path_equivalent(rx%n_rays))
    ENDIF
    DO iray=1,rx%n_rays
      ray => rx%ray(iray)
      src => ray%source
      pathID = ray%raypath_id
      IF (src%path(pathID)%refstep /= 0) THEN
! We have a pp-type phase.
! If the receiver does not yet have a source equivalent,create one and
! point to it.
        IF (rx%source_equivalent == 0) THEN
          n_sources_ppinc = n_sources_ppinc + 1
          rx%source_equivalent = n_source_ppinc
          srcpp => source(rx%source_equivalent)
          srcpp%r = rx%r
          srcpp%lat = rx%lat
          srcpp%long = rx%long
          srcpp%coslat = cos(srcpp%lat)
          srcpp%is_local = .TRUE.
          CALL initialize_source(srcpp, pgrid)
          IF (.NOT. srcpp%on_interface) THEN
            PRINT *,"INFO:: virtual receiver source", n_sources_ppinc
            PRINT *,"    :: located in region", srcpp%region_id
          ELSE
            PRINT *,"INFO:: virtual receiver source", n_sources_ppinc
            PRINT *,"    :: located on interfaces", srcpp%topint_id,&
                                                  & srcpp%botint_id
          ENDIF
          rx%path_equivalent(iray) = 1
! Allocate storage for path info.
          srcpp%n_paths = npp_receiver(irx)
          ALLOCATE(srcpp%path(srcpp%n_paths))
          DO ipath=1, srcpp%n_paths
            CALL path_defaults(srcpp%path(pathID))
          ENDDO
        ELSE
! Point to the already existing source equivalent
          srcpp => source(rx%source_equivalent)
          rx%path_equivalent(iray) = ipp_receiver(irx)
        ENDIF
! Set some attributes of the path
        recpathID = ipp_receiver(irx)
        pathpp => srcpp%path(recpathID)
        path => src%path(pathID)
        pathpp%n_tf = path%n_tf - path%refstep
        pathpp%id = ipp_receiver(irx)
        pathpp%valid = .TRUE.
        pathpp%used = .TRUE.
        pathpp%refstep = pathpp%n_tf + 1
        pathpp%fitting_interface = path%fitting_interface
        ALLOCATE(pathpp%sequence(2*pathpp%n_tf))
        ALLOCATE(pathpp%tf_sequence(pathpp%n_tf))
        ALLOCATE(pathpp%vtype_sequence(pathpp%n_tf))
! Construct the path for the receiver equivalent source by intering the
! original source path.
! Go step by step.
        DO istep=1,2*pathpp%n_tf,2
          pathpp%sequence(istep) = path%sequence(2 * path%n_tf - istep + 1)
          pathpp%sequence(istep + 1) = path%sequence(2 * path%n_tf - i)
          jstep = (istep + 1) / 2
          pathpp%vtype_sequence(jstep) = path%vtype_sequence(path%n_tf - jstep + 1)
! If it is a turning step, exchage the interfaces in this step.
          IF (istep > 1) THEN
            IF (pathpp%sequence(istep + 1) == pathpp%sequence(istep -1)) THEN
              jstep = pathpp%sequence(istep + 1)
              pathpp%sequence(istep + 1) = pathpp%sequence(istep)
              pathpp%sequence(istep) = jstep
            ENDIF
          ENDIF
        ENDDO
        pathpp%sequence(1) = 0
        ipp_receiver(irx) = ipp_receiver(irx) + 1
      ENDIF
    ENDDO
  ENDDO
  DEALLOCATE(npp_receiver, ipp_receiver)
! Now remove the unwated sections from the original pp-type paths from
! the original sources.
  DO isrc=1, n_sources
    src => source(isrc)
    DO ipath=1, src%n_paths
      IF (src%path(ipath)%refstep /= 0) THEN
        src%path(ipath)%n_tf = src%path(ipath)%refstep - 1
      ENDIF
    ENDDO
  ENDDO
! Finished dealing with late reflections.
! Allocate the required timefields for all sources.
  DO isrc=1, n_sources_ppinc
    src => source(isrc)
! Max time fields from initial propagation through regions overlapping
! source grid.
    max_n_tf = n_vtypes * n_regions
    DO ipath=1, src%n_paths
      max_n_tf = max_n_tf + src%path(ipath)%n_tf
    ENDDO
    ALLOCATE(source(isrc)%time_field(max_n_tf))
    DO itf=1, max_n_tf
      CALL time_field_defaults(src%time_field(itf))
      src%time_field(itf)%id = itf
    ENDDO
  ENDDO
  END SUBROUTINE finalize_definitions
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  SUBROUTINE initialize_source(src, grid)
    INTEGER                             :: iinter,&
                                         & ir, ilat, ilon
    TYPE(Tsource)                       :: src
    TYPE(Tpropagation_grid)             :: grid
    REAL(KIND=dp)                       :: dist,&
                                         & dist_below,&
                                         & interpolate_interface,&
                                         & h
    LOGICAL, DIMENSION(:), ALLOCATABLE  :: source_on_interface
! Test for source in grid
    IF (src%lat > pgrid%lat(pgrid%nlat) + pgrid%tolerance / src%r ) THEN
      PRINT *,"ERROR:: source position beyond maximum latitude"
    ENDIF
    IF (src%lat < pgrid%lat(1) - pgrid%tolerance / src%r) THEN
      PRINT *,"ERROR:: source position beyond minimum latitude"
    ENDIF
    IF (src%long > pgrid%long(pgrid%nlong) + pgrid%tolerance / src%r ) THEN
      PRINT *,"ERROR:: source position beyond maximum longitude"
    ENDIF
    IF (src%long < pgrid%long(1) - pgrid%tolerance / src%r ) THEN
      PRINT *,"ERROR:: source position beyond minimum longitude"
    ENDIF
    IF (src%r > interpolate_interface(src%lat,&
                                    & src%long,&
                                    & intrface(1))&
            & + pgrid%tolerance) THEN
      PRINT *,"ERROR:: source above surface"
    ENDIF
    IF (src%r < interpolate_interface(src%lat,&
                                    & src%long,&
                                    & intrface(n_interfaces))&
            & - pgrid%tolerance ) THEN
      PRINT *,"ERROR:: source below lowest interface"
    ENDIF
! Determine grid cell in which the source is located.
    src%ir           =  FLOOR((src%r    - grid%r0)    / grid%dr0    + 1)
    src%ilat         =  FLOOR((src%lat  - grid%lat0)  / grid%dlat0  + 1)
    src%ilong        =  FLOOR((src%long - grid%long0) / grid%dlong0 + 1)
! Correct if source lies exactly on grid boundary.
    src%ir           = MIN(src%ir,    grid%nr    - 1)
    src%ilat         = MIN(src%ilat,  grid%nlat  - 1)
    src%ilong        = MIN(src%ilong, grid%nlong - 1)
    src%on_grid      = .FALSE.
    src%on_interface = .FALSE.
    src%n_cnode      = 0
! Allocate arrays that will contain the indices of the source time
! fields in the time field array.
    ALLOCATE(src%first_tf_up(n_vtypes), src%first_tf_down(n_vtypes))
! Test where the source lies.
! First test if the source lies exactly on any interface.
    ALLOCATE(source_on_interface(n_interfaces))
    source_on_interface = .FALSE.
    dist_below = 1.0_dp
    DO iinter=n_interfaces, 1, -1
      dist = src%r - interpolate_interface(src%lat, src%long, intrface(iinter))
      source_on_interface(iinter) = ABS(dist) < 2.0_dp * grid%tolerance
      IF (source_on_interface(iinter)) THEN
        PRINT *, "source lies exactly on interface",iinter
      ENDIF
      IF (dist < 0.0_dp .AND. dist_below > 0.0_dp) THEN
        print *,"initialize.f90: ",src%region_id
        src%region_id = iinter
      ENDIF
      dist_below = dist
    ENDDO
    src%on_interface = COUNT(source_on_interface(1:n_interfaces)) > 0
    src%on_pinched_interface = COUNT(source_on_interface(1:n_interfaces)) > 1
    IF (src%on_interface) THEN
      src%topint_id = 0
      src%botint_id = n_interfaces + 1
      DO iinter=1, n_interfaces
          h = interpolate_interface(src%lat, src%long, intrface(iinter))
          IF (h - src%r > pgrid%tolerance) THEN
            src%topint_id = iinter
          ENDIF
      ENDDO
      DO iinter=n_interfaces, 1, -1
          h = interpolate_interface(src%lat, src%long, intrface(iinter))
          IF (src%r - h > pgrid%tolerance) THEN
            src%botint_id = iinter
          ENDIF
      ENDDO
      src%topint_id = src%topint_id + 1
      src%botint_id = src%botint_id - 1
      src%topreg_id = src%topint_id - 1
      src%botreg_id = src%botint_id
      IF (src%topint_id == 1 .OR. src%botint_id == n_interfaces) THEN
          src%n_tf_init = 1
      ELSE
          src%n_tf_init = 2
      ENDIF
    ENDIF
    DEALLOCATE(source_on_interface)
! Test if the source lies exactly on a regular grid node or not.
    IF (.NOT. src%on_interface) THEN
      DO ir=0, 1
        DO ilat=0, 1
          DO ilon=0, 1
            dist = sqrt((src%r    - grid%r(src%ir       + ir  )) ** 2&
                    & + (src%lat  - grid%lat(src%ilat   + ilat)) ** 2&
                    & + (src%long - grid%long(src%ilong + ilon)) ** 2)
            IF (dist < grid%tolerance) THEN
              src%on_grid = .TRUE.
            ENDIF
          ENDDO
        ENDDO
      ENDDO
      src%n_tf_init = 1
    ENDIF
    RETURN
  END SUBROUTINE initialize_source
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
END MODULE initialize
