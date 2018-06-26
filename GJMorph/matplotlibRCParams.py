'''
A set of matplotlib rcParams with user specified values. These go well with a figure of size (7, 5.6)
'''

import matplotlib as mpl
import numpy as np


mplPars = {'text.usetex': True,
           'axes.labelsize': 'large',
           'axes.titlesize': 24,
           'font.family': 'sans-serif',
           'font.sans-serif': "cmbright",
           'font.style': "normal",
           'font.size': 24,
           'font.weight': 'black',
           'xtick.labelsize': 20,
           'ytick.labelsize': 20,
           'legend.fontsize': 20,
           'legend.frameon': True,
           'legend.framealpha': 0,
           'legend.fancybox': True,
           'text.latex.preamble': r'\usepackage{cmbright}'
           }

pts = np.linspace(0, np.pi * 2, 24)
circ = np.c_[np.sin(pts) / 2, -np.cos(pts) / 2]
vert = np.r_[circ, circ[::-1] * .7]

'''
This is a valid argument for a marker. This makes markers to be open circles.
'''
openCircleMarker = mpl.path.Path(vert)