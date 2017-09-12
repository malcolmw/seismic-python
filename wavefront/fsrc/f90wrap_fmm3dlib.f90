! Module core defined in file fmm3dlib.f90

subroutine f90wrap_march
    use core, only: march
    implicit none
    
    call march()
end subroutine f90wrap_march

subroutine f90wrap_get_nsources(ret_get_nsources)
    use core, only: get_nsources
    implicit none
    
    integer, intent(out) :: ret_get_nsources
    ret_get_nsources = get_nsources()
end subroutine f90wrap_get_nsources

subroutine f90wrap_get_nrays(ret_get_nrays, recid)
    use core, only: get_nrays
    implicit none
    
    integer, intent(out) :: ret_get_nrays
    integer :: recid
    ret_get_nrays = get_nrays(recID=recid)
end subroutine f90wrap_get_nrays

subroutine f90wrap_get_nreceivers(ret_get_nreceivers)
    use core, only: get_nreceivers
    implicit none
    
    integer, intent(out) :: ret_get_nreceivers
    ret_get_nreceivers = get_nreceivers()
end subroutine f90wrap_get_nreceivers

subroutine f90wrap_get_nsections(recid, ret_get_nsections, rayid)
    use core, only: get_nsections
    implicit none
    
    integer :: recid
    integer, intent(out) :: ret_get_nsections
    integer :: rayid
    ret_get_nsections = get_nsections(recID=recid, rayID=rayid)
end subroutine f90wrap_get_nsections

subroutine f90wrap_get_npoints(recid, rayid, ret_get_npoints, secid)
    use core, only: get_npoints
    implicit none
    
    integer :: recid
    integer :: rayid
    integer, intent(out) :: ret_get_npoints
    integer :: secid
    ret_get_npoints = get_npoints(recID=recid, rayID=rayid, secID=secid)
end subroutine f90wrap_get_npoints

subroutine f90wrap_get_ray_section(recid, rayid, secid, ret_get_ray_section, &
    npts, n0)
    use core, only: get_ray_section
    implicit none
    
    integer :: recid
    integer :: rayid
    integer :: secid
    real, intent(out), dimension(3,n0) :: ret_get_ray_section
    integer :: npts
    integer :: n0
    ret_get_ray_section = get_ray_section(recID=recid, rayID=rayid, secID=secid, &
        npts=npts)
end subroutine f90wrap_get_ray_section

subroutine f90wrap_get_ray_arrival_time(recid, ret_get_ray_arrival_time, rayid)
    use core, only: get_ray_arrival_time
    implicit none
    
    integer :: recid
    real, intent(out) :: ret_get_ray_arrival_time
    integer :: rayid
    ret_get_ray_arrival_time = get_ray_arrival_time(recID=recid, rayID=rayid)
end subroutine f90wrap_get_ray_arrival_time

! End of module core defined in file fmm3dlib.f90

! Module fmm3dlib defined in file fmm3dlib.f90

! End of module fmm3dlib defined in file fmm3dlib.f90

! Module fmm3dlib_noint defined in file fmm3dlib.f90

! End of module fmm3dlib_noint defined in file fmm3dlib.f90

