# SeismicPython
**SeismicPython** provides convenience classes and functions, as well as extensions to and interfaces between seismic data processing tools including [ObsPy](https://github.com/obspy/obspy/wiki "ObsPy Wiki"), the [Antelope](http://www.brtt.com/home.html "BRTT.com") Python API. Because SeismicPython is built as an extension to existing codes, a number of dependencies are required for full functionality.

## Dependencies
- scipy >= 0.18.1
- numpy >= 1.11.2
- matplotlib >= 1.5.3
- obspy >= 1.0.2
- basemap >= 1.0.7

### Non-essential Dependencies (Commercial)
- Antelope Python API [(BRTT)](http://www.brtt.com/home.html "BRTT.com")

# Installation
```bash
bash>$ git clone https://github.com/malcolmw/SeismicPython.git
bash>$ cd SeismicPython
bash>$ python setup.py install --user
```
