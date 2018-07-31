# coding=utf-8
import mpl_toolkits.basemap as bm

class Basemap(bm.Basemap):
    def __init__(self, latmin, latmax, lonmin, lonmax,
                 resolution="i", **kwargs):
        import warnings
        warnings.filterwarnings("ignore")
        kwargs["llcrnrlat"] = latmin
        kwargs["llcrnrlon"] = lonmin
        kwargs["urcrnrlat"] = latmax
        kwargs["urcrnrlon"] = lonmax
        kwargs["resolution"] = resolution
        super(self.__class__, self).__init__(**kwargs)
        self.drawmapboundary(fill_color="aqua")
        self.fillcontinents(color="coral", lake_color="aqua")
        self.drawcoastlines()
