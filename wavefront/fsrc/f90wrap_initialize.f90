! Module initialize defined in file initialize.f90

subroutine f90wrap_allocate_receivers(n)
    use initialize, only: allocate_receivers
    implicit none
    
    integer, intent(in) :: n
    call allocate_receivers(n=n)
end subroutine f90wrap_allocate_receivers

subroutine f90wrap_allocate_sources(n)
    use initialize, only: allocate_sources
    implicit none
    
    integer, intent(in) :: n
    call allocate_sources(n=n)
end subroutine f90wrap_allocate_sources

subroutine f90wrap_allocate_vgrids(nvgrids, nvtypes)
    use initialize, only: allocate_vgrids
    implicit none
    
    integer, intent(in) :: nvgrids
    integer, intent(in) :: nvtypes
    call allocate_vgrids(nvgrids=nvgrids, nvtypes=nvtypes)
end subroutine f90wrap_allocate_vgrids

subroutine f90wrap_define_interfaces(intrfaces, ninter, nlat, nlon, lat0, lon0, &
    dlat, dlon, n0, n1, n2)
    use initialize, only: define_interfaces
    implicit none
    
    real, intent(in), dimension(n0,n1,n2) :: intrfaces
    integer, intent(in) :: ninter
    integer, intent(in) :: nlat
    integer, intent(in) :: nlon
    real, intent(in) :: lat0
    real, intent(in) :: lon0
    real, intent(in) :: dlat
    real, intent(in) :: dlon
    integer :: n0
    !f2py intent(hide), depend(intrfaces) :: n0 = shape(intrfaces,0)
    integer :: n1
    !f2py intent(hide), depend(intrfaces) :: n1 = shape(intrfaces,1)
    integer :: n2
    !f2py intent(hide), depend(intrfaces) :: n2 = shape(intrfaces,2)
    call define_interfaces(intrfaces=intrfaces, ninter=ninter, nlat=nlat, nlon=nlon, &
        lat0=lat0, lon0=lon0, dlat=dlat, dlon=dlon)
end subroutine f90wrap_define_interfaces

subroutine f90wrap_define_propagation_grid(lat0, lon0, depth0, nlat, nlon, &
    ndepth, dlat, dlon, ddepth)
    use initialize, only: define_propagation_grid
    implicit none
    
    real, intent(in) :: lat0
    real, intent(in) :: lon0
    real, intent(in) :: depth0
    integer, intent(in) :: nlat
    integer, intent(in) :: nlon
    integer, intent(in) :: ndepth
    real, intent(in) :: dlat
    real, intent(in) :: dlon
    real, intent(in) :: ddepth
    call define_propagation_grid(lat0=lat0, lon0=lon0, depth0=depth0, nlat=nlat, &
        nlon=nlon, ndepth=ndepth, dlat=dlat, dlon=dlon, ddepth=ddepth)
end subroutine f90wrap_define_propagation_grid

subroutine f90wrap_define_receiver(rxid, lat, lon, depth, n_rays, source_ids, &
    path_ids, n0, n1)
    use initialize, only: define_receiver
    implicit none
    
    integer, intent(in) :: rxid
    real, intent(in) :: lat
    real, intent(in) :: lon
    real, intent(in) :: depth
    integer, intent(in) :: n_rays
    integer, intent(in), dimension(n0) :: source_ids
    integer, intent(in), dimension(n1) :: path_ids
    integer :: n0
    !f2py intent(hide), depend(source_ids) :: n0 = shape(source_ids,0)
    integer :: n1
    !f2py intent(hide), depend(path_ids) :: n1 = shape(path_ids,0)
    call define_receiver(rxID=rxid, lat=lat, lon=lon, depth=depth, n_rays=n_rays, &
        source_ids=source_ids, path_ids=path_ids)
end subroutine f90wrap_define_receiver

subroutine f90wrap_define_source(srcid, is_tele, lat, lon, depth, n_paths)
    use initialize, only: define_source
    implicit none
    
    integer, intent(in) :: srcid
    logical, intent(in) :: is_tele
    real, intent(in) :: lat
    real, intent(in) :: lon
    real, intent(in) :: depth
    integer, intent(in) :: n_paths
    call define_source(srcID=srcid, is_tele=is_tele, lat=lat, lon=lon, depth=depth, &
        n_paths=n_paths)
end subroutine f90wrap_define_source

subroutine f90wrap_define_path(srcid, pathid, n_steps, steps, vtypes, n0, n1, &
    n2)
    use initialize, only: define_path
    implicit none
    
    integer, intent(in) :: srcid
    integer, intent(in) :: pathid
    integer, intent(in) :: n_steps
    integer, intent(in), dimension(n0,n1) :: steps
    integer, intent(in), dimension(n2) :: vtypes
    integer :: n0
    !f2py intent(hide), depend(steps) :: n0 = shape(steps,0)
    integer :: n1
    !f2py intent(hide), depend(steps) :: n1 = shape(steps,1)
    integer :: n2
    !f2py intent(hide), depend(vtypes) :: n2 = shape(vtypes,0)
    call define_path(srcID=srcid, pathID=pathid, n_steps=n_steps, steps=steps, &
        vtypes=vtypes)
end subroutine f90wrap_define_path

subroutine f90wrap_define_vgrid(vtypeid, gridid, values, r0, lambda0, phi0, nr, &
    nlambda, nphi, dr, dlambda, dphi, n0, n1, n2)
    use initialize, only: define_vgrid
    implicit none
    
    integer, intent(in) :: vtypeid
    integer, intent(in) :: gridid
    real, intent(in), dimension(n0,n1,n2) :: values
    real, intent(in) :: r0
    real, intent(in) :: lambda0
    real, intent(in) :: phi0
    integer, intent(in) :: nr
    integer, intent(in) :: nlambda
    integer, intent(in) :: nphi
    real, intent(in) :: dr
    real, intent(in) :: dlambda
    real, intent(in) :: dphi
    integer :: n0
    !f2py intent(hide), depend(values) :: n0 = shape(values,0)
    integer :: n1
    !f2py intent(hide), depend(values) :: n1 = shape(values,1)
    integer :: n2
    !f2py intent(hide), depend(values) :: n2 = shape(values,2)
    call define_vgrid(vtypeID=vtypeid, gridID=gridid, values=values, r0=r0, &
        lambda0=lambda0, phi0=phi0, nr=nr, nlambda=nlambda, nphi=nphi, dr=dr, &
        dlambda=dlambda, dphi=dphi)
end subroutine f90wrap_define_vgrid

subroutine f90wrap_finalize_definitions
    use initialize, only: finalize_definitions
    implicit none
    
    call finalize_definitions()
end subroutine f90wrap_finalize_definitions

! End of module initialize defined in file initialize.f90

