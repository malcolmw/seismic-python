!Statistical signal processing routines

! ----------------------------------------
subroutine pai_s(trace, output, M, npts)
  ! PAI-S Skewness function defined by Saragiotis et al. (2002)
  implicit none

  ! Argument declarations
  integer :: npts, M
  double precision, intent(in) :: trace(npts)
  double precision, intent(out) :: output(npts)

  ! Variable declarations
  double precision :: numer, denom, X(M), mean, diff(M) 
  integer :: i

  output = 0
  mean = sum(trace(1:M))
  do i = M, npts 
    X = trace(i-M+1:i)
    mean = mean - trace(i-M+1) + trace(i+1)
    diff = (X-mean/M)
    numer = sum(diff**3)/M
    denom = (sum(diff**2)/(M-1))**(3./2.)
    output(i) = numer/denom
  end do

end subroutine PAI_S

! ----------------------------------------
subroutine pai_k(trace, output, M, npts)
  ! PAI-K Kurtosis subroutine defined by Saragiotis et al. (2002)
  implicit none

  ! Argument declarations
  integer :: npts, M
  double precision, intent(in) :: trace(npts)
  double precision, intent(out) :: output(npts)

  ! Variable declarations
  double precision :: numer, denom, X(M), mean, diff(M)
  integer :: i

  output = 0
  mean = sum(trace(1:M))
  do i = M, npts
    X = trace(i-M+1:i)
    mean = mean - trace(i-M+1) + trace(i+1)
    diff = (X-mean/M)**2
    denom = (sum(diff)/M)**2
    numer = sum(diff**2)/M
    output(i) = numer/denom - 3.0
    if (isnan(output(i))) output(i) = 0
  end do

end subroutine PAI_K

! ----------------------------------------
subroutine f90trigger(x, t_on, t_off, N, ntrig, on, off)
  implicit none
  double precision, intent(in) :: x(N), on, off
  integer, intent(out) :: t_on(N), t_off(N), ntrig 
  integer, intent(in) :: N
  integer :: i, mode

  mode = 0
  ntrig = 1

  do i = 1, N
    if (mode == 0) then
      if (x(i) >= on) then
        t_on(ntrig) = i - 1
        mode = 1
      end if
    else
      if (x(i) <= off) then
        t_off(ntrig) = i - 1
        ntrig = ntrig + 1
        mode = 0
      end if
    end if
  end do
  if (mode == 1) then
    t_off(ntrig) = N - 1
  end if

end subroutine f90trigger
