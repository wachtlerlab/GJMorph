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





def getRawDF(inputXL, TDLWNXL, outputXL, gridSize, overlappingWindows=False, resampleLength=1):


    if overlappingWindows:

        translationIndicators = [x for x in itertools.product([0, 1], [0, 1], [0, 1])]

    else:
        translationIndicators = [[0, 0, 0]]

    inputDF = pd.read_excel(inputXL)
    TDLWNDF = pd.read_excel(TDLWNXL).set_index(["initRefs", "Experiment ID"])

    tempDFs = []

    for rowInd, (expId, laborState, initRefs, swcFile) in inputDF.iterrows():
        print("Doing {}".format(swcFile))

        bc, bL, swcData = resampleSWC(swcFile, resampleLength, calculateBranchLens=True)

        expIdWN = expId[:-2] + "WN"
        pdl = 100 * bL / TDLWNDF.loc[(initRefs, expIdWN), "WN_TDL"]
        for translationIndicator in translationIndicators:

            # print('GridSize={}, swc={}, translationIndicator={}'.format(gridSize, swcFile,
            #                                                             translationIndicator))

            centers = windowSWCPts(bc,
                                   gridSize, translationIndicator)

            tempDF = pd.DataFrame()
            tempDF.loc[:, 'voxel center'] = map(tuple, centers)
            tempDF.loc[:, 'percentage neurite length'] = pdl

            tempDF = tempDF.groupby('voxel center').sum().reset_index()
            tempDF.loc[:, 'set name'] = laborState
            tempDF.loc[:, 'expID'] = expId
            tempDF.loc[:, "initRefs"] = initRefs
            tempDF.loc[:, 'voxel size'] = gridSize
            tempDFs.append(tempDF)

    rawDF = pd.concat(tempDFs, ignore_index=True)

    rawDF.to_excel(outputXL)





def partFuncDir(dir, partStr):

    return '{}-{}'.format(dir, partStr)


if __name__ == '__main__':

    assert len(sys.argv) == 6, 'Improper usage! Please use as \'python generateRawDF.py <inputXL> <TDLWNXL> <voxelSize> <overlappingWindowsBool> <outXL>\''
    inputXL = sys.argv[1]
    TDLWNXL = sys.argv[2]
    voxelSize = float(sys.argv[3])
    if sys.argv[4] in ["True", "TRUE", "1"]:
        overlappingWindows = True
    elif sys.argv[4] in ["False", "FALSE", "0"]:
        overlappingWindows = False
    else:
        raise(IOError("Unknown value for <overlappingWindowsBool>, use one of [\"True\", \"TRUE\", \"1\"] for True and one of [\"False\", \"FALSE\", \"0\"] for False"))
    outputXL = sys.argv[5]


    getRawDF(inputXL=inputXL,
             gridSize=voxelSize,
             TDLWNXL=TDLWNXL,
             outputXL=outputXL,
             overlappingWindows=overlappingWindows,
             resampleLength=1)





