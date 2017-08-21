import glob
import numpy.distutils
import numpy.distutils.core
import numpy.distutils.misc_util
import numpy.f2py.f2py2e as f2py
import os
import setuptools
import shutil
import subprocess
gtext = numpy.distutils.misc_util.green_text
ytext = numpy.distutils.misc_util.yellow_text
rtext = numpy.distutils.misc_util.red_text
Extension = numpy.distutils.core.Extension

fsrcs = ["libsun", "libtau", "ellip", "sphdist", "nn_subsf"]
f90srcs = ["mod_3dfm", "3dfmlib", "propagate", "rays",
           "frechet", "matchref", "teleseismic",
           "3dfm_main", "stack", "svdlib", "visual"]
srcs = f90srcs + fsrcs

root_dir = os.path.split(os.path.abspath(__file__))[0]
build_dir = "%s/build-tmp" % root_dir
src_dir = "%s/src" % root_dir
pkg_dir = "%s/pkg" % root_dir

if os.path.isdir(build_dir):
    try:
        print(gtext("Removing existing build directory: %s" % build_dir))
        shutil.rmtree(build_dir)
    except Exception as err:
        print(rtext("Failed to remove build directory"))
        print(ytext(err))
        exit()

for path in glob.glob("pkg/_fm3d*"):
    try:
        print(gtext("Removing stale build file: %s" % path))
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
    except Exception as err:
        print(rtext("Failed to remove stale build file"))
        print(ytext(err))
        exit()

try:
    print(gtext("Creating build directory: %s" % build_dir))
    os.mkdir(build_dir)
except Exception as err:
    print(rtext("Failed to created build directory"))
    print(ytext(err))
    exit()
try:
    print(gtext("Changing directory to: %s" % build_dir))
    os.chdir(build_dir)
except Exception as err:
    print(rtext("Failed to change directory"))
    print(ytext(err))
    exit()
for src, ext in list(zip(["%s/%s" % (src_dir, src) for src in f90srcs],
                         ["f90"]*len(f90srcs))) +\
                list(zip(["%s/%s" % (src_dir, src) for src in fsrcs],
                         ["f"]*len(fsrcs))):
    print(gtext("Compiling Fortran source %s.%s" % (src, ext)))
    try:
        cmd = ["gfortran", "-c", "%s.%s" % (src, ext)]
        print("\t%s" % gtext(" ".join(cmd)))
        subprocess.run(cmd)
    except Exception as err:
        print(rtext("Failed to compile Fortran source %s.%s" % (src, ext)))
        print(ytext(err))
        exit()

try:
    print(gtext("Changing directory to: %s" % pkg_dir))
    os.chdir(pkg_dir)
except Exception as err:
    print(rtext("Failed to change directory"))
    print(ytext(err))
    exit()

try:
    print(gtext("Creating Fortran extension module: _fm3d"))
    cmd = ["f2py", "-c", "-m", "_fm3d", "-I%s" % build_dir]
    cmd += glob.glob("%s/f90wrap_*.f90" % src_dir)
    cmd += ["%s/%s.o" % (build_dir, src) for src in srcs]
    print("\t%s" % gtext(" ".join(cmd)))
    subprocess.run(cmd)
except Exception as err:
    print(rtext(err))

try:
    print(gtext("Changing directory to: %s" % root_dir))
    os.chdir(root_dir)
except Exception as err:
    print(rtext("Failed to change directory"))
    print(ytext(err))
    exit()

setuptools.setup(name="wavefront",
                 version=0.0,
                 packages=["wavefront"],
                 package_dir={"wavefront": pkg_dir},
                 package_data={"wavefront": glob.glob("%s/_fm3d*.so" % pkg_dir)},
                 py_modules=["wavefront.fm3d"])
