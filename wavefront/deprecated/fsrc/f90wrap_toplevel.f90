subroutine f90wrap_run(sources, nsources, receivers, nreceivers, outrays, &
    outtts, n0, n1, n2, n3, n4, n5)
    implicit none
    external run
    
    real, intent(in), dimension(n0,3) :: sources
    integer, intent(in) :: nsources
    real, intent(in), dimension(n1,3) :: receivers
    integer, intent(in) :: nreceivers
    real, intent(inout), dimension(n2,n3,2,10000,3) :: outrays
    real, intent(inout), dimension(n4,n5,2) :: outtts
    integer :: n0
    !f2py intent(hide), depend(sources) :: n0 = shape(sources,0)
    integer :: n1
    !f2py intent(hide), depend(receivers) :: n1 = shape(receivers,0)
    integer :: n2
    !f2py intent(hide), depend(outrays) :: n2 = shape(outrays,0)
    integer :: n3
    !f2py intent(hide), depend(outrays) :: n3 = shape(outrays,1)
    integer :: n4
    !f2py intent(hide), depend(outtts) :: n4 = shape(outtts,0)
    integer :: n5
    !f2py intent(hide), depend(outtts) :: n5 = shape(outtts,1)
    call run(sources, nsources, receivers, nreceivers, outrays, outtts)
end subroutine f90wrap_run

subroutine f90wrap_initialize_velocity_grids(vgrids, ngrids, ntypes, nr, &
    nlambda, nphi, r0, lambda0, phi0, dr, dlambda, dphi, n0, n1, n2, n3, n4)
    implicit none
    external initialize_velocity_grids
    
    real, intent(in), dimension(n0,n1,n2,n3,n4) :: vgrids
    integer, intent(in) :: ngrids
    integer, intent(in) :: ntypes
    integer, intent(in) :: nr
    integer, intent(in) :: nlambda
    integer, intent(in) :: nphi
    real, intent(in) :: r0
    real, intent(in) :: lambda0
    real, intent(in) :: phi0
    real, intent(in) :: dr
    real, intent(in) :: dlambda
    real, intent(in) :: dphi
    integer :: n0
    !f2py intent(hide), depend(vgrids) :: n0 = shape(vgrids,0)
    integer :: n1
    !f2py intent(hide), depend(vgrids) :: n1 = shape(vgrids,1)
    integer :: n2
    !f2py intent(hide), depend(vgrids) :: n2 = shape(vgrids,2)
    integer :: n3
    !f2py intent(hide), depend(vgrids) :: n3 = shape(vgrids,3)
    integer :: n4
    !f2py intent(hide), depend(vgrids) :: n4 = shape(vgrids,4)
    call initialize_velocity_grids(vgrids, ngrids, ntypes, nr, nlambda, nphi, r0, &
        lambda0, phi0, dr, dlambda, dphi)
end subroutine f90wrap_initialize_velocity_grids

subroutine f90wrap_initialize_propagation_grid(nr, nlat, nlon, dr, dlat, dlon, &
    h0, lat0, lon0)
    implicit none
    external initialize_propagation_grid
    
    integer, intent(in) :: nr
    integer, intent(in) :: nlat
    integer, intent(in) :: nlon
    real, intent(in) :: dr
    real, intent(in) :: dlat
    real, intent(in) :: dlon
    real, intent(in) :: h0
    real, intent(in) :: lat0
    real, intent(in) :: lon0
    call initialize_propagation_grid(nr, nlat, nlon, dr, dlat, dlon, h0, lat0, lon0)
end subroutine f90wrap_initialize_propagation_grid

subroutine f90wrap_initialize_interfaces(lambda0, phi0, nlambda, nphi, dlambda, &
    dphi)
    implicit none
    external initialize_interfaces
    
    real, intent(in) :: lambda0
    real, intent(in) :: phi0
    integer, intent(in) :: nlambda
    integer, intent(in) :: nphi
    real, intent(in) :: dlambda
    real, intent(in) :: dphi
    call initialize_interfaces(lambda0, phi0, nlambda, nphi, dlambda, dphi)
end subroutine f90wrap_initialize_interfaces

