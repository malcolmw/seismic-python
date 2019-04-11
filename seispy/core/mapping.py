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
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as bm
import pandas as pd
import obspy
import pkg_resources

from . import coords as _coords
from . import defaults as _defaults


def _remove_keys(dict_in, *keys):
    dict_out = dict_in.copy()
    for key in keys:
        del (dict_out[key])
    return(dict_out)


class Basemap(bm.Basemap):
    r"""A basic map to get started with.

    .. todo:: Document this class.
    """

    def __init__(self, basekwargs=None, **kwargs):
        import warnings
        warnings.filterwarnings("ignore")

        if basekwargs is None:
            basekwargs = _defaults.DEFAULT_BASEMAP_BASEKWARGS
        else:
            assert isinstance(basekwargs, dict)
            basekwargs = {**_defaults.DEFAULT_BASEMAP_BASEKWARGS,
                          **basekwargs}
        for kw in kwargs:
            if isinstance(kwargs[kw], dict) and kw in _defaults.DEFAULT_BASEMAP_KWARGS:
                kwargs[kw] = {
                    **_defaults.DEFAULT_BASEMAP_KWARGS[kw], **kwargs[kw]}
        kwargs = {**_defaults.DEFAULT_BASEMAP_KWARGS, **kwargs}

        self.kwargs = kwargs

# Set the current Axes object to the provided handle if one exists.
        if "ax" in self.kwargs and self.kwargs["ax"] is not None:
            plt.sca(self.kwargs["ax"])

        super(Basemap, self).__init__(**basekwargs)
# Store a handle to the current Axes
        self.ax = plt.gca()

        if self.kwargs["bgstyle"] == "basic":
            self._basic_background()
        elif self.kwargs["bgstyle"] == "relief":
            self._relief_background()
        elif self.kwargs["bgstyle"] == "bluemarble":
            self._bluemarble_background()

        if self.kwargs["meridians"]["stride"] is not None:
            self.drawmeridians(np.arange(-180,
                                         180,
                                         self.kwargs["meridians"]["stride"]),
                               **_remove_keys(self.kwargs["meridians"], "stride"))
        if self.kwargs["parallels"]["stride"] is not None:
            self.drawparallels(np.arange(-90,
                                         90,
                                         self.kwargs["parallels"]["stride"]),
                               **_remove_keys(self.kwargs["parallels"], "stride"))

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
                       nmin=100,
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
            ZZ[ix, iy] = func(z[idx]) if np.count_nonzero(idx) >= nmin else np.inf
        XX = XX - dx/2
        YY = YY - dy/2
        XX, YY = self(XX, YY)

        qmesh = self.pcolormesh(XX, YY, ZZ,
                                zorder=3,
                                **kwargs)
        return(qmesh)

    def overlay_pcolormesh(self, x, y, z, zorder=2, **kwargs):
        df = pd.DataFrame.from_dict({"X": x, "Y": y, "Z": z})
        df = df.sort_values(["X", "Y"])
        x = df["X"].drop_duplicates()
        y = df["Y"].drop_duplicates()
        ZZ = df["Z"].values.reshape((len(x), len(y)))
        x = np.concatenate([[x.iloc[0] - x.iloc[:2].diff().iloc[1]/2],
                            x.rolling(2).mean().dropna(),
                            [x.iloc[-1] + x.iloc[-2:].diff().iloc[1]/2]])
        y = np.concatenate([[y.iloc[0] - y.iloc[:2].diff().iloc[1]/2],
                            y.rolling(2).mean().dropna(),
                            [y.iloc[-1] + y.iloc[-2:].diff().iloc[1]/2]])
        XX, YY = np.meshgrid(x, y, indexing="ij")
        XX, YY = self(XX, YY)
        qmesh = self.pcolormesh(XX, YY, ZZ,
                                zorder=zorder,
                                **kwargs)
        return (qmesh)

    def scatter(self, *args, **kwargs):
        x, y = self(np.asarray(args[0]), np.asarray(args[1]))
        return (super(Basemap, self).scatter(x, y, *args[2:], **kwargs))

    def axhline(self, y=0, xmin=None, xmax=None, **kwargs):
        x, y = self(np.mean(self.boundarylons), y)
        return (self.ax.axhline(y, **kwargs))


    def axvline(self, x=0, ymin=None, ymax=None, **kwargs):
        x, y = self(x, np.mean(self.boundarylats))
        return (self.ax.axvline(x, **kwargs))


    def add_faults(self, **kwargs):
        if "color" not in kwargs:
            kwargs["color"] = self.kwargs["fault_color"]
        if "linewidth" not in kwargs:
            kwargs["linewidth"] = self.kwargs["fault_linewidth"]
        faults = CaliforniaFaults()
        return(
            [self.plot(*self(segment[:, 0], segment[:, 1]), **kwargs)
                for segment in faults.subset(self.latmin, self.latmax,
                                             self.lonmin, self.lonmax)]
        )

    
    def add_focal_mech(self, lat, lon, focal_mech, **kwargs):
        x, y = self(lon, lat)
        kwargs = {**_defaults.DEFAULT_BEACHBALL_KWARGS, **kwargs}
        print(kwargs)
        bb = obspy.imaging.beachball.beach(focal_mech, xy=(x, y), axes=self.ax, **kwargs)
        self.ax.add_collection(bb)
    
    
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
            ha = kwargs["ha1"] if "ha1" in kwargs else "right"
            va = kwargs["va1"] if "va1" in kwargs else "bottom"
            text = self.ax.text(*self(geo[0, 1], geo[0, 0]), kwargs["label"],
                                color="w",
                                ha=ha,
                                va=va)
            text.set_path_effects([path_effects.Stroke(linewidth=3,
                                                       foreground="black"),
                                   path_effects.Normal()])
            ha = kwargs["ha2"] if "ha2" in kwargs else "left"
            va = kwargs["va2"] if "va2" in kwargs else "top"
            text = self.ax.text(*self(geo[1, 1], geo[1, 0]),
                                kwargs["label"] + "'",
                                color="w",
                                ha=ha,
                                va=va)
            text.set_path_effects([path_effects.Stroke(linewidth=3,
                                                       foreground="black"),
                                   path_effects.Normal()])
        plot_kwargs = {} if plot_kwargs is None else plot_kwargs
        return(self.plot(*self(geo[:, 1], geo[:, 0]), **plot_kwargs))


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
        def cond1(coords): return latmin <= coords[1] <= latmax and\
            lonmin <= coords[0] <= lonmax

        def cond2(segment): return np.any(
            [cond1(coords) for coords in segment])
        return(np.asarray(list(filter(cond2, self.data))))


class CaliforniaFaults(FaultCollection):
    r"""
    Faults in California.
    """

    def __init__(self):
        fname = pkg_resources.resource_filename("seispy",
                                                "data/ca_scitex.flt")
        super(CaliforniaFaults, self).__init__(fname)


class VerticalPlaneProjector(object):
    r"""
    This is the VerticalPlaneProjector docstring.

    :param list lat: Event latitude coordinates.
    :param list lon: Event longitude coordinates.
    :param list depth: Event depth coordinates.
    :param list aux_data: Auxiliary data.

    .. automethod:: set_scatter_kwargs

    .. automethod:: update_scatter_kwargs
    """

    def __init__(self, lat, lon, depth, aux_data=None):
        self._rdata = _coords.GeographicCoordinates(len(lat))
        self._rdata[:, 0], self._rdata[:,
                                       1], self._rdata[:, 2] = lat, lon, depth
        self._aux_data = np.asarray(aux_data)
        sk = _defaults.DEFAULT_SECTION_KWARGS["scatter_kwargs"]
        ck = _defaults.DEFAULT_SECTION_KWARGS["colorbar_kwargs"]
        gk = _defaults.DEFAULT_SECTION_KWARGS["general"]
        self.scatter_kwargs = sk
        self.colorbar_kwargs = ck
        self.general_kwargs = gk

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

    def set_colorbar_kwargs(self, **kwargs):
        self.colorbar_kwargs = kwargs

    def set_general_kwargs(self, **kwargs):
        self.general_kwargs = kwargs

    def plot_raw(self, ax=None):
        r"""Plot the vertical transect with no frills.

        :param matplotlib.pyplot.Axes ax: The axes to plot to.
        """
        strike = np.radians(self.general_kwargs["strike"])
        self._data = self._rdata.to_ned(origin=self.general_kwargs["origin"]
                                        ).rotate(strike)
        bool_idx = (np.abs(self._data[:, 0]) < self.general_kwargs["length"])\
            & (np.abs(self._data[:, 1]) < self.general_kwargs["width"])
        data = self._data[bool_idx]

        if "c" in self.scatter_kwargs:
            self.scatter_kwargs["c"] = self.scatter_kwargs["c"][bool_idx]
        if ax is None:
            print("ax is None")
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1, aspect=1)
        pts = ax.scatter(data[:, 0], data[:, 2], **self.scatter_kwargs)
        # if self.general_kwargs["special"] is not None:
        #    for special in self.general_kwargs["special"]:
        #        sdata = self._data[(self._aux_data >= special["threshon"])
        #                           & (self._aux_data < special["threshoff"])]
        #        ax.scatter(sdata[:, 0], sdata[:, 2], **special["kwargs"])
        ax.set_xlim(-self.general_kwargs["length"],
                    self.general_kwargs["length"])
        ax.set_ylim(self.general_kwargs["ymin"], self.general_kwargs["ymax"])
        ax.invert_yaxis()
        return(pts)

    def plot(self, ax=None, vmodel=None, phase="Vs"):
        r"""Plot the vertical transect.

        :param matplotlib.pyplot.Axes ax: The axes to plot to.
        """
        strike = np.radians(self.general_kwargs["strike"])
        self._data = self._rdata.to_ned(origin=self.general_kwargs["origin"]
                                        ).rotate(strike)
        bool_idx = (np.abs(self._data[:, 0]) < self.general_kwargs["length"])\
            & (np.abs(self._data[:, 1]) < self.general_kwargs["width"])
        data = self._data[bool_idx]

        if "c" in self.scatter_kwargs and not isinstance(self.scatter_kwargs["c"], str):
            self.scatter_kwargs["c"] = self.scatter_kwargs["c"][bool_idx]
        if ax is None:
            print("ax is None")
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1, aspect=1)
        else:
            fig = ax.get_figure()
        if self.general_kwargs["fig_width"] is not None:
            hwr = (self.general_kwargs["ymax"] - self.general_kwargs["ymin"]) \
                / (self.general_kwargs["length"]*2)
            fig.set_size_inches(self.general_kwargs["fig_width"],
                                self.general_kwargs["fig_width"]*hwr)
        pts = ax.scatter(data[:, 0], data[:, 2], **self.scatter_kwargs)
        ax.yaxis.tick_right()
        ax.yaxis.set_label_position("right")
        ax.set_xlim(-self.general_kwargs["length"],
                    self.general_kwargs["length"])
        ax.set_ylim(self.general_kwargs["ymin"], self.general_kwargs["ymax"])
        ax.invert_yaxis()
        ax.set_xlabel(self.general_kwargs["xlabel"])
        ax.set_ylabel(self.general_kwargs["ylabel"])
        if "c" in self.scatter_kwargs:
            cbar = fig.colorbar(pts, ax=ax, **self.colorbar_kwargs)
            if self.general_kwargs["invert_colorbar"]:
                cbar.ax.invert_yaxis()
            cbar.set_alpha(1)
            cbar.draw_all()
            if "colorbar_label" in self.general_kwargs:
                cbar.set_label(self.general_kwargs["colorbar_label"])
            return(cbar)
        return (ax)
