import json
import os
import shutil
import sys
import tempfile

import numpy as np

from regmaxsn.core.RegMaxSPars import RegMaxSParNames
from regmaxsn.core.iterativeRegistration import composeRefSWC
from regmaxsn.core.misc import parFileCheck
from regmaxsn.core.swcFuncs import transSWC
from regmaxsn.scripts.algorithms.RegMaxS import runRegMaxS


def reg2RegSets(parFile, parNames):
    ch = raw_input('Using parameter File {}.\n Continue?(y/n)'.format(parFile))

    if ch != 'y':
        print('User Abort!')
        sys.exit()

    parList = parFileCheck(parFile, parNames)

    for pars in parList:

        resDir = pars['resDir']

        if os.path.isdir(resDir):

            ch = raw_input('Folder exists: ' + resDir + '\nDelete(y/n)?')
            if ch == 'y':
                shutil.rmtree(resDir)
            else:
                quit()

        os.mkdir(resDir)

        refSWCList = pars['refSWCList']

        for swc in refSWCList:
            assert os.path.isfile(swc), 'Could  not find {}'.format(swc)
            assert swc.endswith('.swc'), 'Elements of swcList must be of SWC format with extension \'.swc\''

        testSWCList = pars['testSWCList']

        for swc in testSWCList:
            assert os.path.isfile(swc), 'Could  not find {}'.format(swc)
            assert swc.endswith('.swc'), 'Elements of swcList must be of SWC format with extension \'.swc\''

    for parInd, pars in enumerate(parList):

        refSWC = os.path.join(resDir,  'refTemplate.swc')
        testSWC = os.path.join(resDir, 'testTemplate.swc')
        resFile = os.path.join(resDir, 'testTemplateReg.swc')

        resDir = pars['resDir']
        refSWCList = pars['refSWCList']
        testSWCList = pars['testSWCList']
        usePartsDir = pars['usePartsDir']
        gridSizes = pars['gridSizes']
        rotBounds = pars['rotBounds']
        transBounds = pars['transBounds']
        scaleBounds = pars['scaleBounds']
        transMinRes = pars['transMinRes']
        minScaleStepSize = pars['minScaleStepSize']
        rotMinRes = pars['rotMinRes']
        nCPU = pars['nCPU']
        retainTempFiles = False
        tempDir, tempName = os.path.split(testSWC[:-4])
        inPartsDir = None
        outPartsDir = None

        thrash = composeRefSWC(refSWCList, refSWC, gridSizes[-1])
        thrash = composeRefSWC(testSWCList, testSWC, gridSizes[-1])

        fd, tempParFile = tempfile.mkstemp(suffix='.json', dir=resDir)
        ns = vars()
        tempPars = [{k: ns[k] for k in RegMaxSParNames}]

        with open(tempParFile, 'w') as fle:
            json.dump(tempPars, fle)

        runRegMaxS(tempParFile, RegMaxSParNames)

        with open(resFile[:-4] + 'Sol.txt', 'r') as fle:
            pars = json.load(fle)
            presTrans = np.array(pars['finalTransMat'])

        for arefswc in refSWCList:

            opFile = os.path.join(resDir, os.path.split(arefswc)[1])
            shutil.copyfile(arefswc, opFile)

            if usePartsDir:
                partsDir = arefswc[:-4]
                if os.path.isdir(partsDir):

                    dirList = os.listdir(partsDir)
                    dirList = [x for x in dirList if x.endswith('swc')]

                    resPartsDir = opFile[:-4]
                    if not os.path.isdir(resPartsDir):
                        os.mkdir(resPartsDir)

                    for entry in dirList:
                        shutil.copyfile(os.path.join(partsDir, entry), os.path.join(resPartsDir, entry))


        for atestswc in testSWCList:

            opFile = os.path.join(resDir, os.path.split(atestswc)[1])
            transSWC(atestswc, presTrans[:3, :3], presTrans[:3, 3], opFile)

            if usePartsDir:
                partsDir = atestswc[:-4]
                if os.path.isdir(partsDir):

                    dirList = os.listdir(partsDir)
                    dirList = [x for x in dirList if x.endswith('swc')]

                    resPartsDir = opFile[:-4]
                    if not os.path.isdir(resPartsDir):
                        os.mkdir(resPartsDir)

                    for entry in dirList:
                        transSWC(os.path.join(partsDir, entry),
                                 presTrans[:3, :3], presTrans[:3, 3],
                                 os.path.join(resPartsDir, entry))



if __name__ == '__main__':

    from GJMorph.reg2regParNames import Reg2RegParNames
    assert len(sys.argv) == 2, 'Improper usage! Please use as \'python reg2RegSets.py parFile\''

    parFile = sys.argv[1]

    reg2RegSets(parFile, Reg2RegParNames)











