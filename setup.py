import glob
import numpy.distutils.misc_util
import os
import shutil
import subprocess
import setuptools

gtext = numpy.distutils.misc_util.green_text
ytext = numpy.distutils.misc_util.yellow_text
rtext = numpy.distutils.misc_util.red_text

def configure():
# Initialize the setup kwargs
    kwargs = {"name": "seismic-python",
            "version": "1.0a0",
            "author": "Malcolm White",
            "author_email": "malcolcw@usc.edu",
            "maintainer": "Malcolm White",
            "maintainer_email": "malcolcw@usc.edu",
            "url": "http://malcolmw.github.io/seismic-python",
            "description": "Seismic data analysis tools",
            "download_url": "https://github.com/malcolmw/seismic-python.git",
            "platforms": ["linux", "osx"],
            "requires": ["obspy", "sqlite3"],
            "packages": ["seispy", "wavefront"],
            "package_dir": {"wavefront": "wavefront/compile"},
            "py_modules": ["seispy.constants",
                           "seispy.coords",
                           "seispy.faults",
                           "seispy.fmm3dio",
                           "seispy.geogrid",
                           "seispy.geometry",
                           "seispy.mapping",
                           "seispy.sqlschemas",
                           "seispy.surface",
                           "seispy.topography",
                           "seispy.ttgrid",
                           "seispy.velocity",
                           "wavefront.fmm3d"],
            "package_data": {"wavefront": ["_fmm3d.*.so"]}}
    return(kwargs)

def compile_fmm3d():
    fsrcs = ["libsun", "libtau", "ellip", "sphdist", "nn_subsf"]
    f90srcs = ["mod_3dfm", "3dfmlib", "propagate", "rays",
            "frechet", "matchref", "teleseismic",
            "3dfm_main", "stack", "svdlib", "visual"]
    srcs = f90srcs + fsrcs

    root_dir = os.path.split(os.path.abspath(__file__))[0]
    comp_dir = "%s/wavefront/compile" % root_dir
    fortran_src_dir = "%s/wavefront/fsrc" % root_dir
    py_src_dir = "%s/wavefront/pysrc" % root_dir
    if os.path.isdir(comp_dir):
        try:
            print(gtext("Removing existing compile directory: %s" % comp_dir))
            shutil.rmtree(comp_dir)
        except Exception as err:
            print(rtext("Failed to remove compile directory"))
            print(rtext(err))
            exit()

    try:
        print(gtext("Creating compile directory: %s" % comp_dir))
        os.mkdir(comp_dir)
    except Exception as err:
        print(rtext("Failed to created compile directory"))
        print(rtext(err))
        exit()
    try:
        print(gtext("Changing directory to: %s" % comp_dir))
        os.chdir(comp_dir)
    except Exception as err:
        print(rtext("Failed to change directory"))
        print(rtext(err))
        exit()
    for src, ext in list(zip(["%s/%s" % (fortran_src_dir, src) for src in f90srcs],
                            ["f90"]*len(f90srcs))) +\
                    list(zip(["%s/%s" % (fortran_src_dir, src) for src in fsrcs],
                            ["f"]*len(fsrcs))):
        print(gtext("Compiling Fortran source %s.%s" % (src, ext)))
        try:
            cmd = ["gfortran", "-c", "%s.%s" % (src, ext)]
            print("\t%s" % gtext(" ".join(cmd)))
            subprocess.run(cmd)
        except Exception as err:
            print(rtext("Failed to compile Fortran source %s.%s" % (src, ext)))
            print(rtext(err))
            exit()

    try:
        print(gtext("Copying package contents to: %s" % comp_dir))
        for f in glob.glob("%s/*" % py_src_dir):
            shutil.copyfile(f, "%s/%s" % (comp_dir, os.path.split(f)[1]))
    except Exception as err:
        print(rtext("Failed to copy file: %s" % f))
        print(rtext(err))
        exit()

    try:
        print(gtext("Creating Fortran extension module: _fmm3d"))
        cmd = ["f2py", "-c", "-m", "_fmm3d", "-I%s" % comp_dir]
        cmd += glob.glob("%s/f90wrap_*.f90" % fortran_src_dir)
        cmd += ["%s/%s.o" % (comp_dir, src) for src in srcs]
        print("\t%s" % gtext(" ".join(cmd)))
        subprocess.run(cmd)
    except Exception as err:
        print(rtext(err))

    try:
        print(gtext("Changing directory to: %s" % root_dir))
        os.chdir(root_dir)
    except Exception as err:
        print(rtext("Failed to change directory"))
        print(rtext(err))
        exit()

if __name__ == "__main__":
    compile_fmm3d()
    kwargs = configure()
    setuptools.setup(**kwargs)
