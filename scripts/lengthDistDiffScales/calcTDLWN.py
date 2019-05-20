'''
Description:        This script is used to calculate the total dendritic length of WN subregions. These calculated data stored in a table with one
                    row for every combination of SWC and voxel. Meta data such as Labor State, initRefs, swcFile and
                    Experiment ID are also saved.

Usage:              python calcTDLWN.py <inputXL> <outputXL>
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





def calcTDLWN(inputXL, outputXL, resampleLength=1):

    inputDF = pd.read_excel(inputXL)

    outputDF = inputDF.copy()

    for rowInd, (expId, laborState, initRefs, swcFile) in inputDF.iterrows():

        assert swcFile.endswith("WN.swc"), "calcTDLWN can only work with WN subregion, {} specified".format(swcFile)
        print("Doing {}".format(swcFile))

        tdl,_ = resampleSWC(swcFile, resampleLength)

        outputDF.loc[rowInd, "WN_TDL"] = tdl

    outputDF.to_excel(outputXL)




if __name__ == '__main__':

    assert len(sys.argv) == 3, 'Improper usage! Please use as \'python clacTDLWN.py <inputXL> <outXL>\''
    inputXL = sys.argv[1]
    outputXL = sys.argv[2]

    calcTDLWN(inputXL, outputXL)



