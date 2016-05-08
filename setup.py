from distutils.core import setup

setup(name='seispy',
      version='1.0',
      description='Seismic data analysis tool',
      author='Malcolm White',
      author_email='white.m88@gmail.com',
      download_url='https://github.com/malcolmw/SeisPy',
      packages=['seispy.core',
                'seispy.util'],
      py_modules=['seispy.core.arrival',
                  'seispy.core.origin',
                  'seispy.util.mtp'],
      scripts=['scripts/tests/test_arrival',
               'scripts/tests/test_origin']
      )
