# Ajayrama Kumaraswamy, 2017, LMU Munich

import numpy as np
import os
from regmaxsn.core.transforms import compose_matrix
from regmaxsn.core.swcFuncs import transSWC_rotAboutPoint
from regmaxsn.core.RegMaxSPars import RegMaxSNParNames
from regmaxsn.core.misc import parFileCheck
import json
from GJEMS.folderDefs import homeFolder


def transAndSave(inFile, outFile, jsonFile, rotMat, translation, rotCenter):
    rotCenter = np.loadtxt(inFile)[:, 2:5].mean(axis=0)
    transSWC_rotAboutPoint(inFile, rotMat, translation, outFile, rotCenter)
    with open(jsonFile, 'w') as jsonFle:
        toWrite = {'inFile': inFile,
                   'translation': translation, 'angles': rotation, 'scale': scale,
                   'comments': 'rotation and scaling about inFile centroid'}
        json.dump(toWrite, jsonFle)


# ----------------------------------------------------------------------------------------------------------------------
# temp = os.path.split(__file__)[0]
# dirPath = os.path.join(os.path.split(temp)[0], 'TestFiles')
# expNames = [
#                 'HSN-fluoro01.CNG',
#                 # 'HSN-fluoro01.CNGNoiseStd1',
#                 # 'HSN-fluoro01.CNGNoiseStd2',
#                 # 'HSN-fluoro01.CNGNoiseStd3',
#                 # 'HSN-fluoro01.CNGNoiseStd4',
#                 # 'HSN-fluoro01.CNGNoiseStd5',
#               ]
#
# outPath = dirPath
# N = 1
# ----------------------------------------------------------------------------------------------------------------------

parFile = os.path.join(homeFolder, "DataAndResults", "morphology", "ParFiles", "Reg-MaxS-N", "DL-Int-1_min20_all.json")

suffix = "_scaled5pc"

parsList = parFileCheck(parFile, RegMaxSNParNames)

for parInd, pars in enumerate(parsList):

    swcList = pars["swcList"]
    resDir = pars["resDir"]
    outDir = resDir + suffix

    if not os.path.isdir(outDir):
        os.mkdir(outDir)

    scale = [1.05, 1.05, 1.05]
    translation = [0, 0, 0]
    rotation = [0, 0, 0]

    rotMat = compose_matrix(angles=rotation, scale=scale)[:3, :3]

    for swc in swcList:

        expName = os.path.split(swc)[1][:-4]
        inFile = os.path.join(resDir, expName + ".swc")
        outFile = os.path.join(outDir, expName + ".swc")
        jsonFile = os.path.join(outDir, "{}.json".format(expName))
        rotCenter = np.loadtxt(inFile)[:, 2:5].mean(axis=0)
        transAndSave(inFile, outFile, jsonFile, rotMat, translation, rotCenter)

        inFile = os.path.join(resDir, "finalRef.swc")
        outFile = os.path.join(outDir, "finalRef.swc")
        jsonFile = os.path.join(outDir, "finalRef.json")
        rotCenter = np.loadtxt(inFile)[:, 2:5].mean(axis=0)
        transAndSave(inFile, outFile, jsonFile, rotMat, translation, rotCenter)

        partDir = os.path.join(resDir, expName)
        outPartDir = os.path.join(outDir, expName)
        if os.path.isdir(partDir):
            partDirList = os.listdir(partDir)
            for partFle in partDirList:
                if partFle.endswith(".swc"):
                    if not os.path.isdir(outPartDir):
                        os.mkdir(outPartDir)
                    inPartFle = os.path.join(partDir, partFle)
                    outPartFle = os.path.join(outPartDir, partFle)
                    partRotCenter = np.loadtxt(inPartFle)[:, 2:5].mean(axis=0)
                    partJSONFile = os.path.join(outPartDir, "{}.json".format(partFle[:-4]))
                    transAndSave(inPartFle, outPartFle, partJSONFile, rotMat, translation, partRotCenter)





