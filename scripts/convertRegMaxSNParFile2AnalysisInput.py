"""
Description:            Converts a JSON parameter file for co-registering two co-registered sets to an excel file that
                        can be used for the scripts compareLengthVsDist.py and lengthDistDiffScales.generateRawDF.py

Usage:                  python convertRegMaxSNParFile2AnalysisInput.py <JSON Parameter file> <part> <output file>

Note:                   <part> can take values in ["WN", "MB", "VB", "DB"]
"""

from GJMorph.reg2regParNames import Reg2RegParNames
from regmaxsn.core.misc import parFileCheck
import pandas as pd
import os
import sys

fExpNames = [
                'HB130313-4',
                'HB130322-1',
                'HB130326-2',
                'HB130408-1',
                'HB130425-1',
                'HB130501-2',
                'HB130705-1',
                'HB140424-1',
            ]

nExpNames = [
                'HB130523-3',
                'HB130605-1',
                'HB130605-2',
                'HB140813-3',
                'HB140917-1',
                'HB140930-1',
                'HB141030-1',
              ]

def partFunc(fle, partStr, subDir=False):

    fleName, fleExt = fle.split('.')
    direc, name = os.path.split(fleName)

    if subDir:
        return os.path.join(direc, name, '{}-{}.{}'.format(name, partStr, fleExt))
    else:
        return os.path.join(direc, '{}-{}.{}'.format(name, partStr, fleExt))

def convert(parFile, part, outXL):

    parsList = parFileCheck(parFile, Reg2RegParNames)

    outDF = pd.DataFrame()

    for pars in parsList:

        laborStates = ["Forager"] * len(pars["refSWCList"]) + ["Newly Emerged"] * len(pars["testSWCList"])
        fSWCFiles = [os.path.join(pars["resDir"], os.path.split(x)[1]) for x in pars["refSWCList"]]
        neSWCFiles = [os.path.join(pars["resDir"], os.path.split(x)[1]) for x in pars["testSWCList"]]
        fSWCFiles = [partFunc(x, part, True) for x in fSWCFiles]
        neSWCFiles = [partFunc(x, part, True) for x in neSWCFiles]
        allSWCFiles = fSWCFiles + neSWCFiles
        for swcFile, laborState in zip(allSWCFiles, laborStates):
            tempS = pd.Series()
            expID = os.path.split(swcFile)[1][:-4]
            tempS["Labor State"] = laborState
            tempS["Experiment ID"] = expID
            tempS["swcFile"] = swcFile
            tempS["initRefs"] = os.path.split(pars["resDir"])[1]
            outDF = outDF.append(tempS, ignore_index=True)

    outDF.to_excel(outXL, index=False)


if __name__ == "__main__":

    assert len(sys.argv) == 4, "Improper Usage! Please use as: python {currentFile} /"
    "<input parFile> <part> <output XL>".format(sys.argv[0])

    convert(sys.argv[1], sys.argv[2], sys.argv[3])



