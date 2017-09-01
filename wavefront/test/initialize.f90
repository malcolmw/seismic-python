MODULE initialize
  USE globals
  USE typedefn
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
    SUBROUTINE initialize_receiver(rxID,&
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
! Check that the receiver is within the latitude and longitude limits
! of the propagation grid here.
! Check also that the receiver lies in the region between the bounding
! surfaces.
! Allocate memory for the ray paths and initialize rays with default
! values.
    ALLOCATE(receiver(rxID)%ray(n_rays))
    DO rayID=1,n_rays
      CALL ray_defaults(rx%ray(rayID))
      rx%ray(rayID)%source_id = source_ids(rayID)
      rx%ray(rayID)%raypath_id = path_ids(rayID)
      rx%ray(rayID)%source => source(source_ids(rayID))
! Verify that ray path references are valid here.
    END DO
    END SUBROUTINE initialize_receiver
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
END MODULE initialize
