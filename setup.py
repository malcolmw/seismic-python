import setuptools
# Initialize the setup kwargs that are independent of Antelope.
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
          "py_modules": ["seispy.constants",
                         "seispy.fm3d",
                         "seispy.geometry",
                         "seispy.sqlschemas",
                         "seispy.topography",
                         "seispy.ttgrid",
                         "seispy.velocity"]}

kwargs["packages"] = ["seispy"]

setuptools.setup(**kwargs)
