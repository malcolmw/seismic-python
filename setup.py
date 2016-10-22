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
          'requires': ['obspy'],
          'py_modules': ['seispy.core',
                         'seispy.geoid',
                         'seispy.geometry',
                         'seispy.locate',
                         'seispy.util',
                         'seispy.velocity'],
          'scripts': ['scripts/fetch/fetch_event_data',
                      'scripts/fm3d_ttimes/fm3d_ttimes',
                      'scripts/locate/mt3dloc',
                      'scripts/synthetics/mtsynth',
                      'scripts/synthetics/synthetics2db']}

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
                                   extra_compile_args=['-O3'])]

# If $ANTELOPE environment variable is not initialized, install only the
# portions of the distribution that will operate independently of
# Antelope.
try:
    antelope_dir = os.environ['ANTELOPE']
except KeyError:
    print "INFO:: $ANTELOPE environment variable not detected."
    print "INFO:: Installing Antelope independent components only."
    kwargs['packages'] = ['seispy', 'seispy.signal']
    kwargs['package_dir'] = {'seispy': 'seispy'}
    setup(**kwargs)
    exit()

# If $ANTELOPE environment variable is initialized, install the portions
# the distribution that depend on Antelope.
print "INFO:: $ANTELOPE environment variable detected (%s)" % antelope_dir
print "INFO:: Installing all components."
kwargs['packages'] = ['seispy', 'seispy.signal', 'gazelle']
kwargs['package_dir'] = {'seispy': 'seispy',
                         'gazelle': 'gazelle'}
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
