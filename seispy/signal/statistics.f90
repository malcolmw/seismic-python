!Statistical signal processing routines

! ----------------------------------------
subroutine cov_filter(Z, N, E, r, phi, npts, wlen)
    ! Recursive sliding covariance matrix calculation
    implicit none

    ! Argument declarations
    double precision, intent(in) :: Z(npts), E(npts), N(npts)
    double precision, intent(out) :: r(npts), phi(npts)
    double precision :: C(3,3), W(3), work(8)
    double precision :: CNN(npts), CEE(npts), CZZ(npts)
    double precision :: CNE(npts), CNZ(npts), CZE(npts)
    integer :: npts, info, i, wlen, lwork

    ! Initialize variables & matrices
    r(1:npts) = 0
    phi(1:npts) = 1
    lwork = 8

    r(1:wlen) = 0
    phi(1:wlen) = 0

    call moving_cov(N, N, CNN, npts, wlen)
    call moving_cov(E, E, CEE, npts, wlen)
    call moving_cov(Z, Z, CZZ, npts, wlen)
    call moving_cov(N, Z, CNZ, npts, wlen)
    call moving_cov(N, E, CNE, npts, wlen)
    call moving_cov(Z, E, CZE, npts, wlen)

    do i = wlen+1, npts
        ! Store result in matrix for given time index
        C(1,1) = CEE(i)
        C(2,2) = CNN(i)
        C(3,3) = CZZ(i)
        C(1,2) = CNE(i)
        C(1,3) = CZE(i)
        C(2,3) = CNZ(i)
        C(3,2) = C(2,3)
        C(3,1) = C(1,3)
        C(2,1) = C(1,2)

        ! Calculate eigenvectors
        call DSYEV('V', 'U', 3, C, 3, W, work, lwork, info)

        ! Store polarization quantities
        r(i) = 1 - (W(1)+W(2))/(2*W(3))
        phi(i) = abs(C(3,3))
    end do

end subroutine cov_filter

! ----------------------------------------
subroutine moving_cov(X, Y, C, npts, wlen)
    implicit none
    double precision, intent(in) :: X(npts), Y(npts)
    double precision, intent(out) :: C(npts)
    double precision :: xm, ym, xm_old, ym_old, cov
    integer, intent(in) :: wlen
    integer :: npts, den, i

    xm = sum(X(1:wlen))
    ym = sum(Y(1:wlen))
    cov = dot_product(X(1:wlen)-xm/wlen, Y(1:wlen)-ym/wlen)
    den = npts*npts
    C(1:wlen) = 0
    do i = wlen+1, npts
        xm_old = xm
        ym_old = ym
        xm = xm + X(i) - X(i-wlen)
        ym = ym + Y(i) - Y(i-wlen)
        cov = cov + X(i)*Y(i) - X(i-wlen)*Y(i-wlen) !+ npts*(xm_old*ym_old/den -xm*ym/den) 
        C(i) = cov
    end do

end subroutine moving_cov

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
subroutine snr(trace, cft, nsta, nlta, npts, on, off)

    ! recursive mean calculation
    implicit none

    ! Argument declarations
    integer :: npts
    double precision, intent(in) :: trace(npts), on, off
    integer, intent(in) :: nsta, nlta
    double precision, intent(out) :: cft(npts)

    ! Variable declarations
    double precision :: sta, lta, X(nsta), Y(nlta)
    integer :: state, i
    state = 0
    cft(1:nlta) = 0
    do i = nlta, npts
        X = trace(i-nsta+1:i)
        Y = trace(i-nlta+1:i)
        sta = sum(X**2)/nsta
        if (state == 0) then
            lta = sum(Y**2)/nlta
            cft(i) = sta/lta
            if (cft(i) >= on) then
                state = 1
            end if
        else
            cft(i) = sta/lta
            if (cft(i) < off) then
                state = 0
            end if
        end if
    end do

end subroutine snr

! ----------------------------------------
subroutine stalta(trace, cft, nsta, nlta, npts)

    ! recursive mean calculation
    implicit none

    ! Argument declarations
    integer :: npts
    double precision, intent(in) :: trace(npts), nsta, nlta
    double precision, intent(out) :: cft(npts)

    ! Variable declarations
    double precision :: alpha, beta, inv_alpha, inv_beta, square
    double precision :: sta, lta
    integer :: i

    alpha = 1/nsta
    beta = 1/nlta
    inv_alpha = 1 - alpha
    inv_beta = 1 - beta
    sta = 0
    lta = 1e-30

    do i = 2, npts
        square = trace(i)**2
        sta = alpha*square + inv_alpha*sta
        lta = beta*square + inv_beta*lta
        cft(i) = sta/lta
        if (i <= nlta) then
            cft(i) = 0
        end if
    end do

end subroutine stalta

! ----------------------------------------
subroutine trigger(x, t_on, t_off, N, ntrig, on, off)
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

end subroutine trigger

