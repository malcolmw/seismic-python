from distutils.core import setup

setup(name='seispy',
      version='0.0alpha',
      author='Malcolm White',
      author_email='malcolcw@usc.edu',
      maintainer='Malcolm White',
      maintainer_email='malcolcw@usc.edu',
      url='http://malcolmw.github.io/SeismicPython/',
      description='Seismic data analysis tools',
      download_url='https://github.com/malcolmw/SeisPy',
      platforms=['linux'],
      requires=['obspy'],
      packages=['seispy', 'gazelle'],
      package_dir={'seispy': 'seispy'},
      package_data={'seispy': ['data/schemas/*',
                               'data/dbdemo/*']
                   },
      py_modules=['seispy.core',
                  'seispy.geoid',
                  'seispy.geometry',
                  'seispy.util',
                  'seispy.velocity'],
      scripts=['scripts/fm3d_ttimes/fm3d_ttimes']
      )
