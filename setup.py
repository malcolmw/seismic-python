from numpy.distutils.core import setup, Extension
from numpy.distutils.system_info import get_info
from numpy import get_include as np_get_include
import os
import sys

# Use the g++ compiler to compile C++ and Fortran90 code.
os.environ['CXX'] = "g++"

# Initialize the setup kwargs that are independent of Antelope.
kwargs = {'name': 'seispy',
          'version': '0.0alpha',
          'author': 'Malcolm White',
          'author_email': 'malcolcw@usc.edu',
          'maintainer': 'Malcolm White',
          'maintainer_email': 'malcolcw@usc.edu',
          'url': 'http://malcolmw.github.io/SeismicPython/',
          'description': 'Seismic data analysis tools',
          'download_url': 'https://github.com/malcolmw/SeismicPython',
          'platforms': ['linux'],
          'requires': ['obspy', 'basemap'],
          'py_modules': ['seispy.event',
                         'seispy.gather',
                         'seispy.geoid',
                         'seispy.geometry',
                         'seispy.locate',
                         'seispy.network',
                         'seispy.station',
                         'seispy.trace',
                         'seispy.util',
                         'seispy.velocity'],
          'scripts': ['scripts/fetch_data.py',
                      'scripts/fm3d_ttimes.py',
                      'scripts/mt3dloc.py',
                      'scripts/mtsynth.py',
                      'scripts/synthetics2db.py']}

# Get some information about BLAS and LAPACK libraries.
blas_opt = get_info('blas', notfound_action=2)
lapack_opt = get_info('lapack', notfound_action=2)

# Compile resource information needed by seispy.signal.statistics module.
config_path = "%s/lib/python%d.%d/config" % (sys.prefix,
                                             sys.version_info.major,
                                             sys.version_info.minor)
libs = [blas_opt['libraries'][0],
        lapack_opt['libraries'][0]]
lib_dirs = [blas_opt['library_dirs'][0],
            lapack_opt['library_dirs'][0],
            config_path]
# Compile resource information needed by seispy.signal.detect module
eigen_path = os.getcwd() + "/seispy/signal/src"
# Add statistics and detect extension modules from the seispy.signal
# sub-module.
kwargs['ext_modules'] = [Extension('seispy.signal.statistics',
                                   ['seispy/signal/statistics.f90'],
                                   libraries=libs,
                                   library_dirs=lib_dirs,
                                   extra_link_args=['-llapack', '-lblas']),
                         Extension('seispy.signal.detect',
                                   sources=['seispy/signal/src/detect.cc',
                                            'seispy/signal/src/picker.cc'],
                                   include_dirs=[np_get_include(),
                                                 eigen_path],
                                   extra_compile_args=['-O3']),
                         Extension('seispy.hypocenter.accelerate',
                                   sources=['seispy/hypocenter/accelerate.cc'])]
kwargs['packages'] = ['seispy', 'seispy.signal', 'seispy.hypocenter']
kwargs['package_dir'] = {'seispy': 'seispy'}
# If $ANTELOPE environment variable is not initialized, install only the
# portions of the distribution that will operate independently of
# Antelope.
try:
    antelope_dir = os.environ['ANTELOPE']
except KeyError:
    print "INFO:: $ANTELOPE environment variable not detected."
    print "INFO:: Installing Antelope independent components only."
    setup(**kwargs)
    exit()

# If $ANTELOPE environment variable is initialized, install the portions
# the distribution that depend on Antelope.
print "INFO:: $ANTELOPE environment variable detected (%s)" % antelope_dir
print "INFO:: Installing all components."
kwargs['packages'] += ['gazelle']
kwargs['package_dir']['gazelle'] = 'gazelle'
kwargs['ext_modules'] += [Extension("gazelle.response",
                                    ["gazelle/responsemodule/"
                                     "responsemodule.c"],
                                    include_dirs=["%s/include" % antelope_dir],
                                    libraries=['coords',
                                               'alk',
                                               'stock',
                                               'deviants',
                                               'brttpool',
                                               'response'],
                                    library_dirs=['%s/lib' % antelope_dir])]
setup(**kwargs)
