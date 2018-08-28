#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 14:00:58 2018

@author: malcolcw

This provides access to default arguments.
"""

import matplotlib.pyplot as plt

DEFAULT_RECTANGLE_KWARGS = {"origin": (33.5731, -116.633, 0),
                            "strike": 125,
                            "length": 40,
                            "width": 25}
   
DEFAULT_BASEMAP_KWARGS = {
        "latmin": 32.5,
        "lonmin": -117.5,
        "latmax": 34.5,
        "lonmax": -115.5,
        "bgstyle": "basic",
        "resolution": "c",
        "fill_color": "aqua",
        "continent_color": "coral",
        "lake_color": "aqua",
        "projection": "cyl",
        "meridian_stride": 1,
        "meridian_labels": [False, False, False, True],
        "parallel_stride": 1,
        "parallel_labels": [True, False, False, False],
        "fault_color": "k",
        "fault_linewidth": 1,
        }

DEFAULT_SECTION_KWARGS = {
        "general": {"ax": None,
                    "fig_width": 8,
                    "origin": (33.5, -116.5, 0),
                    "strike": 135,
                    "length": 50,
                    "width": 15,
                    "ymin": 0,
                    "ymax": 25,
                    "special": None,
                   },
        "scatter_kwargs": {"s": 1,
                           "cmap": plt.get_cmap("hot_r"),
                           "zorder": 2
                          },
        "colorbar_kwargs": {"shrink": 0.75}
        }
