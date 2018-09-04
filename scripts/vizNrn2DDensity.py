"""
Description:            This script is used to plot 2D visualizations of SWCs with circles representing SWC nodes and
                        lines representing connections between nodes. The areas behind such plots is divided into
                        squares, with squares containing atleast one SWC node highlighted. Joint visualization of
                        multiple SWCS, with each SWC highlighted in a different color, is also possible.

Usage:                  Modify the definition of the following variables and run the script:
                        1. dirPath: string, containing the path of a directory containing input SWCs
                        2. expNames: list of strings, each containing the names of SWCS
                        3. gridSize: size of the squares into which the area behind SWCs is divided.

Note:                   This file was used to generate the top row of Figure 1 in
                        Kumaraswamy et al. "Spatial Registration of Neuron Morphologies Based on Maximization of
                        Volume Overlap." BMC Bioinformatics 19.143 (2018).https://doi.org/10.1186/s12859-018-2136-z
"""

from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import patches as mpatches
import os
from GJMorph.folderDefs import homeFolder
from GJMorph.matplotlibRCParams import getLighterColor, mplPars

plt.ion()


sns.set(rc=mplPars)







# swcFiles = [
#             os.path.join(homeFolder,
#                          'DataAndResults/morphology/OriginalData/borstHSN2D/HSN-fluoro01.CNG2D.swc'),
#             os.path.join(homeFolder,
#                                 'DataAndResults/morphology/OriginalData/borstHSN2D/HSN-fluoro01.CNG2DRandRot.swc')
#             # os.path.join(homeFolder,
#             #              'DataAndResults/morphology/OriginalData/borstHSN2D/HSN-fluoro01.CNG2DRandRot1.swc'),
#             # os.path.join(homeFolder,
#             #         'DataAndResults/morphology/OriginalData/borstHSN2D/HSN-fluoro01.CNGNoiseStd42DRandRot1.swc'),
#             # os.path.join(homeFolder,
#             #              'DataAndResults/morphology/OriginalData/borstHSN2D/HSN-fluoro01.CNG2DRandTranslate1.swc'),
#             # os.path.join(homeFolder,
#             #              'DataAndResults/morphology/OriginalData/borstHSN2D/HSN-fluoro01.CNG2DRandScale.swc'),
#            ]

fExpNames = [
                'HB130313-4',
                # 'HB130322-1',
                # 'HB130326-2',
                # 'HB130408-1',
                'HB130425-1',
                # 'HB130501-2',
                # 'HB130705-1',
                # 'HB140424-1',
            ]

nExpNames = [
                'HB130523-3',
                # 'HB130605-1',
                # 'HB130605-2',
                # # 'HB140701-1',
                'HB140813-3',
                # 'HB140917-1',
                # 'HB140930-1',
                # 'HB141030-1',
              ]
expNames = fExpNames + nExpNames
dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/'
                                   'Reg2Reg/DL-Int-1/Forager_refHB140424-1_NE_refHB141030-1')
swcFiles = [os.path.join(dirPath, expName + '.swc') for expName in expNames]

initTrans = np.array([
                       [-1, 0, 0],
                       [0, -1, 0],
                       [0, 0,  1]
                       ])

# gridSize = 20.0
gridSize = 40.0
# gridSize = 10.0
minMarkerSize = 5
maxMarkerSize = 10

minRad = 1
maxRad = 5

cols = plt.cm.rainbow(np.linspace(0, 1, len(swcFiles)))

xDis = []
yDis = []
with sns.axes_style('whitegrid'):
    fig, ax = plt.subplots(figsize=(7, 5.6))

for swcInd, swcFile in enumerate(swcFiles):

    print('Doing {}'.format(swcFile))
    data = np.loadtxt(swcFile)
    dataXYZ = np.dot(initTrans, data[:, 2:5].T).T

    slope = (maxMarkerSize - minMarkerSize) / (maxRad - minRad)

    rad2MarkerSize = lambda rad: minMarkerSize + slope * (rad - minRad)

    xs = []
    ys = []
    rads = data[:, 5]
    for ind in range(1, data.shape[0]):

        xs.append([dataXYZ[ind, 1], dataXYZ[int(data[ind, 6]) - 1, 1]])
        ys.append([dataXYZ[ind, 0], dataXYZ[int(data[ind, 6]) - 1, 0]])


    xs = np.array(xs).T
    ys = np.array(ys).T

    xyDis = gridSize * np.array(np.around(dataXYZ[:, 2::-1] / gridSize), np.intp)
    xDis += xyDis[:, 0].tolist()
    yDis += xyDis[:, 1].tolist()

    xySet = set(map(tuple, xyDis))

    with sns.axes_style('whitegrid'):
        col = cols[swcInd]
        lightCol = getLighterColor(col[:3], 0.5)
        for xy in xySet:

            ax.add_patch(
                mpatches.Rectangle((xy[0] - 0.5 * gridSize, xy[1] - 0.5 * gridSize), width=gridSize, height=gridSize,
                                   fc=lightCol))

        ax.plot(xs, ys, color=col, ls='-', ms=3)

    for x, y, r in zip(xs[0, :], ys[0, :], rads):
        with sns.axes_style('whitegrid'):
            ax.plot(x, y, color=col, marker='o', ms=rad2MarkerSize(r))

ax.axis('square')


xmax = max(xDis) + 0.5 * gridSize
xmin = min(xDis) - 0.5 * gridSize
width = xmax - xmin

ymax = max(yDis) + 0.5 * gridSize
ymin = min(yDis) - 0.5 * gridSize
height = ymax - ymin

ax.set_xlim(xmin - gridSize, xmax + gridSize)
ax.set_ylim(ymin - gridSize, ymax + gridSize)

xticks = np.arange(xmin, xmax + gridSize, gridSize)
yticks = np.arange(ymin, ymax + gridSize, gridSize)

ax.set_xticks(xticks)
ax.set_yticks(yticks)

# xticklabels = ['' if x % 5 else str(y) for x, y in enumerate(xticks)]
# yticklabels = ['' if x % 5 else str(y) for x, y in enumerate(yticks)]

xticklabels = []
yticklabels = []

ax.set_xticklabels(xticklabels, rotation=90)
ax.set_yticklabels(yticklabels)

# ax.set_xlabel(r'X in $\mu$m')
# ax.set_ylabel(r'Y in $\mu$m')
ax.grid(True)

fig.tight_layout()
# fig.canvas.draw()


