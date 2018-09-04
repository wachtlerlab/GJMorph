'''
A set of matplotlib rcParams with user specified values. These go well with a figure of size (7, 5.6)
'''

import matplotlib as mpl
import numpy as np
import colorsys


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

def getLighterColor(col, saturation):
    '''
    Returns a color with the same hue and value as the color `col', but with the given saturation
    :param col: 3 member iterable with values in [0, 1]
    :param saturation: float in [0, 1]
    :return:
    '''

    assert len(col) == 3, 'col must be a 3 member iterable'
    assert all([0 <= x <= 1 for x in col]), 'col can only contain values in [0, 1]'
    assert 0 <= saturation <= 1, 'saturation must be in [0, 1]'

    hsv = colorsys.rgb_to_hsv(*col)
    return colorsys.hsv_to_rgb(hsv[0], saturation, hsv[2])