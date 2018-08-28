# coding=utf-8
r"""
This is some introductory text describing this module.

.. codeauthor:: Malcolm White

.. autoclass:: Basemap
   :members:

.. autoclass:: FaultCollection
   :members:

.. autoclass:: CaliforniaFaults
   :members:

.. autoclass:: VerticalPlaneProjector
   :members:
"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as bm
import pandas as pd
import pkg_resources

from . import coords as _coords
from . import defaults as _defaults

class Basemap(bm.Basemap):
    r"""A basic map to get started with.
    
    .. todo:: Document this class.
    """
    def __init__(self, **kwargs):
        import warnings
        warnings.filterwarnings("ignore")

        for key in _defaults.DEFAULT_BASEMAP_KWARGS:
            if key not in kwargs:
                kwargs[key] = _defaults.DEFAULT_BASEMAP_KWARGS[key]
        self.kwargs = kwargs
        del(kwargs)

        kwargs = {"llcrnrlat": self.kwargs["latmin"],
                  "llcrnrlon": self.kwargs["lonmin"],
                  "urcrnrlat": self.kwargs["latmax"],
                  "urcrnrlon": self.kwargs["lonmax"],
                  "resolution": self.kwargs["resolution"]}

        if self.kwargs["bgstyle"] == "relief":
            kwargs["projection"] = self.kwargs["projection"]

# Set the current Axes object to the provided handle if one exists.
        if "ax" in self.kwargs:
            plt.sca(self.kwargs["ax"])

        super(self.__class__, self).__init__(**kwargs)

        if self.kwargs["bgstyle"] == "basic":
            self._basic_background()
        elif self.kwargs["bgstyle"] == "relief":
            self._relief_background()
        elif self.kwargs["bgstyle"] == "bluemarble":
            self._bluemarble_background()

        if self.kwargs["meridian_stride"] is not None:
            self.drawmeridians(np.arange(-180,
                                         180,
                                         self.kwargs["meridian_stride"]),
                               labels=self.kwargs["meridian_labels"])
        if self.kwargs["parallel_stride"] is not None:
            self.drawparallels(np.arange(-90,
                                         90,
                                         self.kwargs["parallel_stride"]),
                               labels=self.kwargs["parallel_labels"])

    def _basic_background(self):
        self.drawmapboundary(fill_color=self.kwargs["fill_color"],
                             zorder=0)
        self.fillcontinents(color=self.kwargs["continent_color"],
                            lake_color=self.kwargs["lake_color"],
                            zorder=1)
        self.drawcoastlines(zorder=1)

    def _relief_background(self):
        self.arcgisimage(service="World_Shaded_Relief",
                         xpixels=3000,
                         verbose=True)

    def _bluemarble_background(self):
        self.bluemarble()

    def node_statistic(self, x, y, z, r,
                       func=np.mean,
                       dx=0,
                       dy=0,
                       **kwargs):
        x = np.asarray(x)
        y = np.asarray(y)
        z = np.asarray(z)
        if dx <= 0:
            dx = (x.max() - x.min()) / 9
        if dy <= 0:
            dy = (y.max() - y.min()) / 9
        xnodes = np.arange(x.min(), x.max()+3*dx/2, dx)
        ynodes = np.arange(y.min(), y.max()+3*dy/2, dy)
        XX, YY = np.meshgrid(xnodes, ynodes, indexing="ij")
        ZZ = np.zeros(XX.shape)
        for ix, iy in [(ix, iy) for ix in range(XX.shape[0])
                                for iy in range(XX.shape[1])]:
            dist = np.sqrt(np.square(x-XX[ix, iy]) + np.square(y-YY[ix, iy]))
            idx = dist < r
            ZZ[ix, iy] = func(z[idx]) if np.any(idx) else np.inf
        XX = XX - dx/2
        YY = YY - dy/2
        qmesh = self.pcolormesh(XX, YY, ZZ,
                                zorder=3,
                                **kwargs)
        return(qmesh)

    def overlay_pcolormesh(self, x, y, z, **kwargs):
        df = pd.DataFrame.from_dict({"X": x, "Y": y, "Z": z})
        df = df.sort_values(["X", "Y"])
        x = df["X"].drop_duplicates()
        y = df["Y"].drop_duplicates()
        ZZ = df["Z"].reshape((len(x), len(y)))
        x = np.concatenate([[x.iloc[0] - x.iloc[:2].diff().iloc[1]/2],
                            x.rolling(2).mean().dropna(),
                            [x.iloc[-1] + x.iloc[-2:].diff().iloc[1]/2]])
        y  = np.concatenate([[y.iloc[0] - y.iloc[:2].diff().iloc[1]/2],
                             y.rolling(2).mean().dropna(),
                             [y.iloc[-1] + y.iloc[-2:].diff().iloc[1]/2]])
        XX, YY = np.meshgrid(x, y, indexing="ij")
        qmesh = self.pcolormesh(XX, YY, ZZ,
                                zorder=3,
                                **kwargs)
        return(qmesh)

    def add_faults(self, **kwargs):
        if "color" not in kwargs:
            kwargs["color"] = self.kwargs["fault_color"]
        if "linewidth" not in kwargs:
            kwargs["linewidth"] = self.kwargs["fault_linewidth"]
        faults = CaliforniaFaults()
        return(
            [self.plot(segment[:,0], segment[:,1], **kwargs)
                for segment in faults.subset(self.latmin, self.latmax,
                                            self.lonmin, self.lonmax)]
        )

    def add_rectangle(self, plot_kwargs=None, **kwargs):
        kwargs = {**_defaults.DEFAULT_RECTANGLE_KWARGS, **kwargs}
        if kwargs["width"] == 0:
            geo = _coords.as_ned([[-kwargs["length"], 0, 0],
                                  [kwargs["length"], 0, 0]],
                                 origin=kwargs["origin"]
                                 ).rotate(-np.radians(kwargs["strike"])
                                 ).to_geographic()
        else:
            geo = _coords.as_ned([[-kwargs["length"], -kwargs["width"], 0],
                                  [-kwargs["length"], kwargs["width"], 0],
                                  [kwargs["length"], kwargs["width"], 0],
                                  [kwargs["length"], -kwargs["width"], 0],
                                  [-kwargs["length"], -kwargs["width"], 0]],
                                 origin=kwargs["origin"]
                                 ).rotate(-np.radians(kwargs["strike"])
                                 ).to_geographic()
        if "label" in kwargs and kwargs["width"] == 0:
            text = self.ax.text(geo[0,1], geo[0,0], kwargs["label"],
                                color="w",
                                ha="right",
                                va="bottom")
            text.set_path_effects([path_effects.Stroke(linewidth=3, foreground="black"),
                                   path_effects.Normal()])
            text = self.ax.text(geo[1,1], geo[1,0], kwargs["label"] + "'",
                                color="w",
                                ha="left",
                                va="top")
            text.set_path_effects([path_effects.Stroke(linewidth=3, foreground="black"),
                                   path_effects.Normal()])
        plot_kwargs = {} if plot_kwargs is None else plot_kwargs
        return(self.plot(geo[:,1], geo[:,0], **plot_kwargs))

class FaultCollection(object):
    r"""
    A collection of faults.
    """
    def __init__(self, infile):
        inf = open(infile)
        self.data = np.array([
                                np.array([[float(coord) for coord in pair.split()]
                                 for pair in chunk.strip().split("\n")
                                ])
                             for chunk in inf.read().split(">")
                             ])
        inf.close()

    def subset(self, latmin, latmax, lonmin, lonmax):
        cond1 = lambda coords: latmin <= coords[1] <= latmax and\
                               lonmin <= coords[0] <= lonmax
        cond2 = lambda segment: np.any([cond1(coords) for coords in segment])
        return(np.asarray(list(filter(cond2, self.data))))

class CaliforniaFaults(FaultCollection):
    r"""
    Faults in California.
    """
    def __init__(self):
        fname = pkg_resources.resource_filename("seispy",
                                                "data/ca_scitex.flt")
        super(self.__class__, self).__init__(fname)


class VerticalPlaneProjector(object):
    r"""
    This is the VerticalPlaneProjector docstring.
    
    :param list lat: Event latitude coordinates.
    :param list lon: Event longitude coordinates.
    :param list depth: Event depth coordinates.
    :param list aux_data: Auxiliary data.
    """
    def __init__(self, lat, lon, depth, aux_data=None):
        #: Doc comment for instance attribute _rdata
        self._rdata = _coords.GeographicCoordinates(len(lat))
        self._rdata[:,0], self._rdata[:,1], self._rdata[:,2] = lat, lon, depth
        self._aux_data = np.asarray(aux_data)
        self.scatter_kwargs = _defaults.DEFAULT_SECTION_KWARGS["scatter_kwargs"]
        self.colorbar_kwargs = _defaults.DEFAULT_SECTION_KWARGS["colorbar_kwargs"]
        self.general_kwargs = _defaults.DEFAULT_SECTION_KWARGS["general"]

    def update_scatter_kwargs(self, **kwargs):
        r"""
        Update kwargs passed directly to matplotlib.pyplot.Axes.scatter. 
        
        This method updates *only* the kwargs specified.
        """
        kwargs = {**self.scatter_kwargs, **kwargs}
        self.set_scatter_kwargs(**kwargs)
    
    def update_colorbar_kwargs(self, **kwargs):
        r"""
        Update kwargs passed directly to matplotlib.pyplot.Figure.colorbar. 
        
        This method updates *only* the kwargs specified.
        """
        kwargs = {**self.colorbar_kwargs, **kwargs}
        self.set_colorbar_kwargs(**kwargs)
    
    def update_general_kwargs(self, **kwargs):
        r"""Update general plot kwargs. 
        
        This method updates *only* the kwargs specified.

        :param matplotlib.pyplot.Axes ax: 
        :param float fig_width:
        :param seispy.coords.GeographicCoordinates origin:
        :param float strike:
        :oaram float length:
        :param float ymin:
        :param float ymax:
        """
        kwargs = {**self.general_kwargs, **kwargs}
        self.set_general_kwargs(**kwargs)
    
    def set_scatter_kwargs(self, **kwargs):
        self.scatter_kwargs = kwargs

    def set_colobar_kwargs(self, **kwargs):
        self.colorbar_kwargs = kwargs

    def set_general_kwargs(self, **kwargs):
        self.general_kwargs = kwargs

    def plot(self, ax=None):
        r"""Plot the vertical transect.
        
        :param matplotlib.pyplot.Axes ax: The axes to plot to.
        """
        self._data = self._rdata.to_ned(origin=self.general_kwargs["origin"]
                               ).rotate(np.radians(self.general_kwargs["strike"]))
        bool_idx = (np.abs(self._data[:,0]) < self.general_kwargs["length"])\
                  &(np.abs(self._data[:,1]) < self.general_kwargs["width"])
        data = self._data[bool_idx]
    
        if "c" in self.scatter_kwargs:
            self.scatter_kwargs["c"] = self.scatter_kwargs["c"][bool_idx]
        if ax is None:
            print("ax is None")
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1, aspect=1)
        else:
            fig = ax.get_figure()
        hwr = (self.general_kwargs["ymax"] - self.general_kwargs["ymin"]) \
            / (self.general_kwargs["length"]*2.15)
        fig.set_size_inches(self.general_kwargs["fig_width"], 
                            self.general_kwargs["fig_width"]*hwr)
        pts = ax.scatter(data[:,0], data[:,2], **self.scatter_kwargs)
        if self.general_kwargs["special"] is not None:
            for special in self.general_kwargs["special"]:
                sdata = self._data[(self._aux_data >= special["threshon"])
                                  &(self._aux_data < special["threshoff"])]
                ax.scatter(sdata[:,0], sdata[:,2], **special["kwargs"])
        ax.set_xlim(-self.general_kwargs["length"], 
                    self.general_kwargs["length"])
        ax.set_ylim(self.general_kwargs["ymin"], self.general_kwargs["ymax"])
        ax.invert_yaxis()
        ax.set_xlabel(r"Horizontal offset [$km$]")
        ax.set_ylabel(r"Depth [$km$]")
        if "c" in self.scatter_kwargs:
            cbar = fig.colorbar(pts, ax=ax, **self.colorbar_kwargs)
            cbar.ax.invert_yaxis()
            cbar.set_alpha(1)
            if "colorbar_label" in self.general_kwargs:
                cbar.set_label(self.general_kwargs["colorbar_label"])
        return(ax)