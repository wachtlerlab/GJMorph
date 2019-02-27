'''
Description:        This script is used to divide the space containing the input SWCs into voxels and calculate
                    the dendritic length of each SWC in each voxel. These calculated data stored in a table with one
                    row for every combination of SWC and voxel. Meta data such as Labor State, initRefs, swcFile and
                    Experiment ID are also saved.

Usage:              python generateRawDF.py <inputXL> <voxel size> <outputXL>
                    <inputXL>: string containing the path of an excel file with the columns "Experiment ID",
                    "Labor State", "initRefs" and "swcFile".
                    <voxel size>: string, which represents a float, the desired size of the voxels
                    <outputXL>: string, path where the output excel file will be written.
'''

import itertools
import pandas as pd
from GJMorph.auxFuncs import resampleSWC, windowSWCPts
from regmaxsn.core.misc import parFileCheck
import numpy as np
import os
import sys





def getRawDF(inputDF, gridSize, overlappingWindows=False, resampleLength=1):


    if overlappingWindows:

        translationIndicators = [x for x in itertools.product([0, 1], [0, 1], [0, 1])]

    else:
        translationIndicators = [[0, 0, 0]]


    branchCenters = []
    percentBranchLens = []

    for swc in inputDF["swcFile"]:

        print('Initializing SWCTree for {}'.format(swc))
        bc, bL, swcData = resampleSWC(swc, resampleLength, calculateBranchLens=True)
        bL_np = np.array(bL)
        percent_bL = bL_np/bL_np.sum()
        branchCenters.append(bc)
        percentBranchLens.append(percent_bL)

    tempDFs = []

    for rowInd, (expId, laborState, initRefs, swcFile) in inputDF.iterrows():
        print("Doing {}".format(swcFile))

        for translationIndicator in translationIndicators:

            # print('GridSize={}, swc={}, translationIndicator={}'.format(gridSize, swcFile,
            #                                                             translationIndicator))

            centers = windowSWCPts(branchCenters[rowInd],
                                   gridSize, translationIndicator)

            tempDF = pd.DataFrame()
            tempDF.loc[:, 'voxel center'] = map(tuple, centers)
            tempDF.loc[:, 'percentage neurite length'] = percentBranchLens[rowInd]

            tempDF = tempDF.groupby('voxel center').sum().reset_index()
            tempDF.loc[:, 'set name'] = laborState
            tempDF.loc[:, 'expID'] = expId
            tempDF.loc[:, "initRefs"] = initRefs
            tempDF.loc[:, 'voxel size'] = gridSize
            tempDFs.append(tempDF)

    rawDF = pd.concat(tempDFs, ignore_index=True)

    return rawDF





def partFuncDir(dir, partStr):

    return '{}-{}'.format(dir, partStr)


if __name__ == '__main__':

    assert len(sys.argv) == 4, 'Improper usage! Please use as \'python generateRawDF.py <inputXL>' \
                               '<voxelSize> <outXL>\''
    inputXL = sys.argv[1]
    voxelSize = float(sys.argv[2])
    outputXL = sys.argv[3]


    inputDF = pd.read_excel(inputXL)

    rawDF = getRawDF(inputDF=inputDF,
                     gridSize=voxelSize,
                     overlappingWindows=True,
                     resampleLength=1)

    rawDF.to_excel(outputXL)



