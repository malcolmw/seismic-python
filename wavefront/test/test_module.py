import numpy as np
import seispy
import test

π = np.pi
root = "/Users/malcolcw/Projects/Wavefront/examples/example1"
def main():
    v_typegrids = seispy.read_vgrids("%s/vgrids.in" % root)
    print("allocate_vgrids()")
    test.initialize.allocate_vgrids(v_typegrids["n_vgrids"],
                                    v_typegrids["n_vtypes"])
    for (ivt, ivg) in [(ivt, ivg) for ivt in range(1, v_typegrids["n_vtypes"] + 1)\
                                  for ivg in range(1, v_typegrids["n_vgrids"] + 1)]:
        vg = v_typegrids[ivt][ivg]
        grid = vg["grid"]
        test.initialize.define_vgrid(ivt, ivg,
                                     np.fliplr(vg["data"]),
                                     grid.ρ0, grid.λ0, grid.φ0,
                                     grid.nρ, grid.nλ, grid.nφ,
                                     grid.dρ, grid.dλ, grid.dφ)
    print("define_propagation_grid()")
    test.initialize.define_propagation_grid(0, 0, 0,
                                            41, 41, 21,
                                            0.5, 0.5, 50.0)
    interfaces = seispy.read_interfaces("%s/interfaces.in" % root)
    grid = interfaces[0].grid
    interfaces = np.array([np.flipud(intr.coordinates[...,0]) for intr in interfaces])
    print("define_interfaces()")
    test.initialize.define_interfaces(interfaces,
                                      *interfaces.shape,
                                      grid.lat0, grid.lon0,
                                      grid.dlat, grid.dlon)
    print("allocate_sources()")
    test.initialize.allocate_sources(1)
    print("define_source()")
    test.initialize.define_source(1, False,
                                  2.0, 2.0, 0.0,
                                  4)
    print("define_path()")
    test.initialize.define_path(1, 1, 6,
                                [[0, 2], [2, 3], [3, 4], [4, 3], [3, 2], [2, 1]],
                                [1, 1, 1, 1, 1, 1])
    print("define_path()")
    test.initialize.define_path(1, 2, 6,
                                [[0, 2], [2, 3], [3, 4], [4, 3], [3, 2], [2, 1]],
                                [1, 1, 2, 2, 1, 1])
    print("define_path()")
    test.initialize.define_path(1, 3, 6,
                                [[0, 2], [2, 3], [3, 4], [4, 3], [3, 2], [2, 1]],
                                [2, 2, 2, 1, 1, 1])
    print("define_path()")
    test.initialize.define_path(1, 4, 6,
                                [[0, 2], [2, 3], [3, 4], [4, 3], [3, 2], [2, 1]],
                                [2, 2, 1, 1, 1, 1])
    print("allocate_receivers()")
    test.initialize.allocate_receivers(1)
    print("define_receiver()")
    test.initialize.define_receiver(1,
                                    18.0, 18.0, 0.0,
                                    4,
                                    [1, 1, 1, 1],
                                    [1, 2, 3, 4])
    print("finalize_definitions()")
    test.initialize.finalize_definitions()
    print("march()")
    test.core.march()
if __name__ == "__main__":
    main()
