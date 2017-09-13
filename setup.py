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
                           "wavefront.fmm3d",
                           "wavefront.fmm3dlib"],
            "package_data": {"wavefront": ["_fmm3dlib.*.so"]},
            "include_package_data": True}
    return(kwargs)

def compile_fmm3d():
    sources = ["typedefn.f90",
               "globals.f90",
               "legacy/interface_definitions.f90",
               "fmm3dlib.f90",
               "legacy/3dfmlib.f90",
               "legacy/ellip.f",
               "legacy/frechet.f90",
               "legacy/libsun.f",
               "legacy/libtau.f",
               "legacy/matchref.f90",
               "legacy/nn_subsf.f",
               "legacy/propagate.f90",
               "legacy/rays.f90",
               "legacy/sphdist.f",
               "legacy/stack.f90",
               "legacy/svdlib.f90",
               "legacy/teleseismic.f90",
               "initialize.f90",
               "util.f90"]
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
    for src in sources:
        print(gtext("Compiling Fortran source %s" % src))
        src = "%s/%s" % (fortran_src_dir, src)
        try:
            cmd = ["gfortran", "-c", src]
            print("\t%s" % gtext(" ".join(cmd)))
            subprocess.run(cmd)
        except Exception as err:
            print(rtext("Failed to compile Fortran source %s.%s" % src))
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
        print(gtext("Creating Fortran extension module: _fmm3dlib"))
        cmd = ["f2py", "-c", "-m", "_fmm3dlib", "-I%s" % comp_dir]
        cmd += ["%s/f90wrap_fmm3dlib.f90" % fortran_src_dir]
        cmd += ["%s/f90wrap_initialize.f90" % fortran_src_dir]
        for src in sources:
            src = os.path.splitext(os.path.split(src)[1])[0]
            cmd += ["%s/%s.o" % (comp_dir, src)]
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
