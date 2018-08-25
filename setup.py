import setuptools

def configure():
# Initialize the setup kwargs
    kwargs = {
            "name": "seismic-python",
            "version": "0.0a0",
            "author": "Malcolm White",
            "author_email": "malcolcw@usc.edu",
            "maintainer": "Malcolm White",
            "maintainer_email": "malcolcw@usc.edu",
            "url": "http://malcolmw.github.io/seismic-python",
            "description": "Seismic data analysis tools",
            "download_url": "https://github.com/malcolmw/seismic-python.git",
            "platforms": ["linux", "osx"],
            "requires": ["obspy", "sqlite3", "numpy", "scipy", "basemap"],
            "packages": ["seispy"],
            "package_data": {"seispy": ["data/ca_scitex.flt"],
                             "seispy.pandas": ["data/schemas/*.pkl"]}
            }
    return(kwargs)

if __name__ == "__main__":
    kwargs = configure()
    setuptools.setup(**kwargs)
