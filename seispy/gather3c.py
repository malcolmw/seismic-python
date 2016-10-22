#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 18:04:04 2016

@author: malcolcw
"""
from seispy.signal.detect import detectS as _detectS_cc
from seispy.signal.detect import create_polarization_filter
from copy import deepcopy
import matplotlib.pyplot as plt
import obspy.core


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
