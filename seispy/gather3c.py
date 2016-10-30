#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 18:04:04 2016

@author: malcolcw
"""
from seispy.signal.detect import detectS as _detectS_cc
from seispy.signal.detect import create_polarization_filter
from copy import deepcopy
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import obspy.core
from obspy.geodetics import gps2dist_azimuth

class Gather(obspy.core.Stream):     
    def apply_offsets(self, lat0, lon0):
        offsets = [gps2dist_azimuth(lat0,
                                    lon0,
                                    trace.stats.station.lat,
                                    trace.stats.station.lon)[0]\
                   for trace in self.traces]
        max_offset = max(offsets)
        offsets = [offset / max_offset for offset in offsets]
        [self.traces[i].amplitude_offset(offsets[i])\
                 for i in range(len(self.traces))]

    def azimuths(self, lat0, lon0):
        return [gps2dist_azimuth(lat0,
                                 lon0,
                                 trace.stats.station.lat,
                                 trace.stats.station.lon)[1]\
                    for trace in self.traces]

    def detrend(self, *args, **kwargs):
        [trace.detrend(*args) for trace in self.traces]
         
    def distances(self, lat0, lon0):
        return [gps2dist_azimuth(lat0,
                                 lon0,
                                 trace.stats.station.lat,
                                 trace.stats.station.lon)[0] / 1000.\
                    for trace in self.traces]
                    
    def distance_sort(self, lat0, lon0):
        if lon0 > 180.:
            lon0 -= 360.
        key = lambda trace: gps2dist_azimuth(lat0,
                                             lon0,
                                             trace.stats.station.lat,
                                             trace.stats.station.lon)
        self.traces = sorted(self.traces, key=key)
        
    def normalize(self):
        for trace in self.traces:
            max_amp = max(trace.data) * len(self.traces)
            trace.normalize(max_amp=max_amp)
            
    def plot(self, plot_type, *args, **kwargs):
        if plot_type == "section":
            self._plot_section(*args, **kwargs)
        else:
            return None

    def _plot_section(self,
                      lat0,
                      lon0,
                      t0,
                      arrivals=None,
                      cmap=None,
                      show=True,
                      subplot_ax=None,
                      set_xticks_position="top",
                      set_yticks_position="right"):
        if subplot_ax:
            ax = subplot_ax
        else:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
        self.distance_sort(lat0, lon0)
        self.detrend("demean")
        self.normalize()
        self.apply_offsets(lat0, lon0)
        for trace in self.traces:
            station = trace.stats.station
            channel = trace.stats.channel.code 
            if not cmap == None:
                color= cmap(gps2dist_azimuth(lat0,
                                             lon0,
                                             station.lat,
                                             station.lon)[1] / 360.)
            else:
                if channel[2] == "Z":
                    color, alpha = 'k', 0.5
                elif channel[2] == "N" or channel[2] == "1":
                    color, alpha = 'b', 0.5
                elif channel[2] == "E" or channel[2] == "2":
                    color, alpha = 'r', 0.5
            ax.plot(trace.data,
                    trace.times(),
                    color=color,
                    zorder=1)
        offsets = self.distances(lat0, lon0)
        max_offset = max(offsets)
        # plot arrivals if any were provided
        if not arrivals == None:
            offsets = [offset / max_offset for offset in offsets]
            station_offsets = {}
            for pair in zip([trace.stats.station.name for trace in self.traces],
                            offsets):
                name, offset = pair
                if name not in station_offsets:
                    station_offsets[name] = offset
            for arrival in arrivals:
                try:
                    offset = station_offsets[arrival.station.name]
                except KeyError:
                    continue
                xmin = offset - 0.1
                xmax = offset + 0.1
                ax.hlines(float(arrival.time - t0),
                          xmin,
                          xmax,
                          linewidth=3.0,
                          zorder=2)
        ax.set_ylim(0, max([max(trace.times()) for trace in self.traces]))
        ax.invert_yaxis()
        # configure tick labelling / positioning
        ax.xaxis.set_ticks_position(set_xticks_position)
        if max_offset < 10.:
            xtick_stride = 2.
        elif 10. <= max_offset < 25.:
            xtick_stride = 5.
        elif 25. <= max_offset < 50.:
            xtick_stride = 10.
        else:
            xtick_stride = 25.
        xmin, xmax = ax.get_xlim()
        xmax *= max_offset
        xticks = np.arange(0,
                           xmax + xtick_stride / 2.,
                           xtick_stride)/ max_offset
        xtick_labels = [i * xtick_stride for i in range(len(xticks))]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels)
        ax.yaxis.set_ticks_position(set_yticks_position)
        if subplot_ax:
            return ax
        elif show:
            plt.show()
        return fig
        

class Gather3C(obspy.core.Stream):
    """
    .. todo::
        Document this class.
    .. warning::
       This constructor for this class assumes traces argument is in V,
       H1, H2 order.
    """
    def __init__(self, traces):
        # This call may need to pass a deepcopy of traces argument
        super(self.__class__, self).__init__(traces=traces)
        self.V = self[0]
        self.H1 = self[1]
        self.H2 = self[2]
        self.stats = deepcopy(traces[0].stats)
        channel_set = [tr.stats.channel for tr in traces]
        self.stats.channel = "%s:%s%s%s" % (channel_set[0][:2],
                                            channel_set[0][2],
                                            channel_set[1][2],
                                            channel_set[2][2])
        self.stats.channel_set = channel_set

    def detectS(self, cov_twin=3.0, k_twin=1.0):
        output = _detectS_cc(self.V.data,
                             self.H1.data,
                             self.H2.data,
                             cov_twin,
                             self.stats.delta,
                             k_twin)
        lag1, lag2, snr1, snr2, pol_fltr, S1, S2, K1, K2 = output
        # Checking for the various possible pick results
        if lag1 > 0 and lag2 > 0:
            if snr1 > snr2:
                lag = lag1
                snr = snr1
                channel = self.H1.stats.channel
            else:
                lag = lag2
                snr = snr2
                channel = self.H2.stats.channel
        elif lag1 > 0:
            lag = lag1
            snr = snr1
            channel = self.H1.stats.channel
        elif lag2 > 0:
            lag = lag2
            snr = snr2
            channel = self.H2.stats.channel
        else:
            return
        return Detection(self.stats.station,
                         channel,
                         self.stats.starttime + lag,
                         'S')

    def filter(self, *args, **kwargs):
        self.V.filter(*args, **kwargs)
        self.H1.filter(*args, **kwargs)
        self.H2.filter(*args, **kwargs)

    def plot(self,
             starttime=None,
             endtime=None,
             arrivals=None,
             detections=None,
             show=True,
             xticklabel_fmt=None):
        fig, axs = plt.subplots(nrows=3, sharex=True, figsize=(12, 9))
        fig.subplots_adjust(hspace=0)
        fig.suptitle("Station %s" % self.stats.station, fontsize=20)
        axV, axH1, axH2 = axs
        detections_V = [d for d in detections
                        if d.channel == self.V.stats.channel]\
            if detections\
            else None
        arrivals_V = [a for a in arrivals
                      if a.channel == self.V.stats.channel]\
            if arrivals\
            else None
        axV = self.V.subplot(axV,
                             starttime=starttime,
                             endtime=endtime,
                             arrivals=arrivals_V,
                             detections=detections_V,
                             xticklabel_fmt=xticklabel_fmt)
        detections_H1 = [d for d in detections
                         if d.channel == self.H1.stats.channel]\
            if detections\
            else None
        arrivals_H1 = [a for a in arrivals
                       if a.channel == self.H1.stats.channel]\
            if arrivals\
            else None
        axH1 = self.H1.subplot(axH1,
                               starttime=starttime,
                               endtime=endtime,
                               arrivals=arrivals_H1,
                               detections=detections_H1,
                               xticklabel_fmt=xticklabel_fmt)
        detections_H2 = [d for d in detections
                         if d.channel == self.H2.stats.channel]\
            if detections\
            else None
        arrivals_H2 = [a for a in arrivals
                       if a.channel == self.H2.stats.channel]\
            if arrivals\
            else None
        axH2 = self.H2.subplot(axH2,
                               starttime=starttime,
                               endtime=endtime,
                               arrivals=arrivals_H2,
                               detections=detections_H2,
                               xticklabel_fmt=xticklabel_fmt)
        if show:
            plt.show()
        else:
            return fig

    def polarize(self, cov_twin=3.0):
        fltr = create_polarization_filter(self.V.data,
                                          self.H1.data,
                                          self.H2.data,
                                          cov_twin,
                                          self.stats.delta)
        self.H1.data = self.H1.data * fltr
        self.H2.data = self.H2.data * fltr
