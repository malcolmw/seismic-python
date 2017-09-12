!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
module interface_definitions
! explicit interfaces for subroutines that have pointer/target arguments

interface
   subroutine propagate(regin,vtype)
     USE typedefn
     USE globals
     type(Tregion),target    :: regin
     integer                 :: vtype
   end subroutine
end interface

interface
   subroutine trace_ray_from_receiver(rec,s,ray)
     USE typedefn
     USE globals
     type(Tsource),target          :: s         
     type(Treceiver)               :: rec       
     type(Tray),target             :: ray       
   end subroutine
end interface

interface
   subroutine find_intersection(isec,iface,grid)
     USE typedefn
     USE globals
     type(Tintersection)               :: isec
     type(Tinterface)                  :: iface
     type(Tpropagation_grid),target    :: grid
   end subroutine
end interface

interface
   subroutine define_region(reg,itop,ibot,grid)
     USE typedefn
     USE globals
     type(Tregion),target     :: reg
     type(Tintersection)      :: itop,ibot
     type(Tpropagation_grid),target :: grid
   end subroutine
end interface

interface
   subroutine sweep_region_from_interface(reg,istart_in,vtype,s)
     USE typedefn
     USE globals
     type(Tregion)                          :: reg
     type(Tintersection),target             :: istart_in
     integer                                :: vtype
     type(Tsource)                          :: s
   end subroutine
end interface

interface
   subroutine sweep_sregion_from_interface(reg,istart_in,vtype)
     USE typedefn
     USE globals
     type(Tregion)                          :: reg
     type(Tintersection),target             :: istart_in
     integer                                :: vtype
   end subroutine
end interface

interface
   subroutine initialize_refined_source(s,sc,grid,reg,itop,ibot)
     USE typedefn
     USE globals
     type(Tsource) :: s
     type(Tsource) :: sc
     type(Tpropagation_grid) :: grid
     type(Tregion)         :: reg
     type(Tintersection),target   :: itop,ibot
   end subroutine
end interface


interface
   subroutine initialize_refined_source2(s,sc,grid,reg,itop,ibot)
     USE typedefn
     USE globals
     type(Tsource) :: s
     type(Tsource) :: sc
     type(Tpropagation_grid) :: grid
     type(Tregion)         :: reg
     type(Tintersection),target   :: itop,ibot
   end subroutine
end interface

end module interface_definitions
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
