from GJMorph.reg2regParNames import Reg2RegParNames
from regmaxsn.core.misc import parFileCheck
import os
import json
from regmaxsn.core.transforms import decompose_matrix
import sys


def printTestScaling(parFile):

    parList = parFileCheck(parFile, Reg2RegParNames)

    for pars in parList:
        resDir = pars["resDir"]
        solFile = os.path.join(resDir, "testTemplateRegSol.txt")
        with open(solFile) as fle:
            solVals = json.load(fle)
        finalTransMat = solVals["finalTransMat"]
        scale, shear, angles, tran, persp = decompose_matrix(finalTransMat)
        print("{} {} {} {}".format(os.path.split(resDir)[1], *scale))


if __name__ == "__main__":

    assert len(sys.argv) == 2, "Improper Usage! Please use as : python {} <Reg2regParFile>".format(sys.argv[0])

    printTestScaling(sys.argv[1])
