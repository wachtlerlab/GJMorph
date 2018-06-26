"""
Description:        This file is used to generate a json parameter file for co-registering two set of co-registered
                    morphologies.Reg-MaxS is internally used for co-registering "average" (i.e. Union) representations
                    of the morphologies in each set. Each morphology of the test set is transformed using the same
                    transformation that was used to co-register the test average.
                    The generated JSON file will contain a dict with keys specified in GJMorph.reg2regParNames

Usage:              python constructReg2RegSetsParFile.py

Action:             creates a parameter file for co-registering two sets of co-registered morphologies

Usage guidelines:   There are a couple of cases with examples shown below.
                    Read the comments therein.
                    Essentially edit the values of some variables in this script and run it.
"""

import json
import os
from itertools import product

from numpy import pi, deg2rad

from GJMorph.reg2regParNames import Reg2RegParNames
from regmaxsn.core.RegMaxSPars import RegMaxSNParNames
from GJMorph.folderDefs import homeFolder

temp = os.path.split(os.path.abspath(__file__))[0]
temp1 = os.path.split(temp)[0]


# **********************************************************************************************************************

# # Default parameters
# # distances in um, angles in radians
# gridSizes = [40.0, 20.0, 10.0]
# transBounds = [[-30, 30], [-30, 30], [-30, 30]]
# transMinRes = 1
# rotBounds = [[-pi / 6, pi / 6], [-pi / 6, pi / 6], [-pi / 6, pi / 6]]
# rotMinRes = deg2rad(1).round(4)
# scaleBounds = [[0.5, 1 / 0.5], [0.5, 1 / 0.5], [0.5, 1 / 0.5]]
# minScaleStepSize = 1.005
# usePartsDir = False
# nCPU = 6
# maxIter = 100

# **********************************************************************************************************************

# User defined parameters. Change these if required
# distances in um, angles in radians
gridSizes = [160, 80, 40.0, 20.0]
transBounds = [[-30, 30], [-30, 30], [-30, 30]]
transMinRes = 1
rotBounds = [[-pi / 6, pi / 6], [-pi / 6, pi / 6], [-pi / 6, pi / 6]]
rotMinRes = deg2rad(1).round(4)
scaleBounds = [[0.5, 1 / 0.5], [0.5, 1 / 0.5], [0.5, 1 / 0.5]]
minScaleStepSize = 1.005
usePartsDir = True
nCPU = 6
maxIter = 100

# **********************************************************************************************************************
# fpars = []
# # homeFolder = os.path.join(os.path.expanduser("~"), 'atlasHome')
# # parFile = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'ParFiles', 'Reg-MaxS-N',
# #                        'DL-Int-1_forager1_ind0.json')
# # -----------------------------------------------------------------------------------
# # job 1
# # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130313-4.swc')
# swcDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1')
# expNames = [
#                 'HB130313-4',
#                 'HB130322-1',
#                 'HB130326-2',
#                 'HB130408-1',
#                 'HB130425-1',
#                 'HB130501-2',
#                 'HB130705-1',
#                 'HB140424-1',
#             ]
# swcList = [os.path.join(swcDir, expName + '.swc') for expName in expNames]
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1', 'Forager_refHB130313-4')
# finallyNormalizeWRT = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1',
#                                    'HB130425-1.swc')
#
# ns = vars()
# fpars += [{k: ns[k] for k in RegMaxSNParNames}]
#
# # -----------------------------------------------------------------------------------
# # job 2
# # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130408-1.swc')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1', 'Forager_refHB130408-1')
#
# ns = vars()
# fpars += [{k: ns[k] for k in RegMaxSNParNames}]
#
# # -----------------------------------------------------------------------------------
# # job 3
# # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB140424-1.swc')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1', 'Forager_refHB140424-1')
#
# ns = vars()
# fpars += [{k: ns[k] for k in RegMaxSNParNames}]
# # -----------------------------------------------------------------------------------
# # job 4
# # -----------------------------------------------------------------------------------
#
# npars = []
#
# initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130605-2.swc')
# swcDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1')
# expNames = [
#                 'HB130523-3',
#                 'HB130605-1',
#                 'HB130605-2',
#                 'HB140813-3',
#                 'HB140917-1',
#                 'HB140930-1',
#                 'HB141030-1',
#             ]
# swcList = [os.path.join(swcDir, expName + '.swc') for expName in expNames]
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1', 'NE_refHB130605-2')
# finallyNormalizeWRT = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1',
#                                    'HB130605-2.swc')
#
# ns = vars()
# npars += [{k: ns[k] for k in RegMaxSNParNames}]
#
# # -----------------------------------------------------------------------------------
# # job 5
# # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130605-1.swc')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1', 'NE_refHB130605-1')
#
# ns = vars()
# npars += [{k: ns[k] for k in RegMaxSNParNames}]
#
# # -----------------------------------------------------------------------------------
# # job 6
# # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB141030-1.swc')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1', 'NE_refHB141030-1')
#
# ns = vars()
# npars += [{k: ns[k] for k in RegMaxSNParNames}]
# # **********************************************************************************************************************

# fpars = []
# # -----------------------------------------------------------------------------------
# # job 1
# # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130313-4.swc')
# swcDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1')
# expNames = [
#                 'HB130313-4',
#                 'HB130322-1',
#                 'HB130326-2',
#                 'HB130408-1',
#                 'HB130425-1',
#                 'HB130501-2',
#                 'HB130705-1',
#                 'HB140424-1',
#             ]
# swcList = [os.path.join(swcDir, expName + '.swc') for expName in expNames]
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20',
#                       'Forager_refHB130313-4')
# finallyNormalizeWRT = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1',
#                                    'HB130425-1.swc')
# ns = vars()
# fpars += [{k: ns[k] for k in RegMaxSNParNames}]
#
# # -----------------------------------------------------------------------------------
# # job 2
# # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130501-2.swc')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20',
#                       'Forager_refHB130501-2')
#
# ns = vars()
# fpars += [{k: ns[k] for k in RegMaxSNParNames}]
#
# # -----------------------------------------------------------------------------------
# # job 3
# # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130322-1.swc')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20',
#                       'Forager_refHB130322-1')
#
# ns = vars()
# fpars += [{k: ns[k] for k in RegMaxSNParNames}]
#
#
# npars = []
# # # -----------------------------------------------------------------------------------
# # # job 4
# # # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130605-2.swc')
# swcDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1')
# expNames = [
#                 'HB130523-3',
#                 'HB130605-1',
#                 'HB130605-2',
#                 'HB140813-3',
#                 'HB140917-1',
#                 'HB140930-1',
#                 'HB141030-1',
#             ]
# swcList = [os.path.join(swcDir, expName + '.swc') for expName in expNames]
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20', 'NE_refHB130605-2')
# finallyNormalizeWRT = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1',
#                                    'HB130523-3.swc')
# ns = vars()
# npars += [{k: ns[k] for k in RegMaxSNParNames}]
# # -----------------------------------------------------------------------------------
# # job 5
# # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130605-1.swc')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20', 'NE_refHB130605-1')
# ns = vars()
# npars += [{k: ns[k] for k in RegMaxSNParNames}]
#
# # -----------------------------------------------------------------------------------
# # job 6
# # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB141030-1.swc')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20', 'NE_refHB141030-1')
# ns = vars()
# npars += [{k: ns[k] for k in RegMaxSNParNames}]
# # **********************************************************************************************************************
#

# fpars = []
# # -----------------------------------------------------------------------------------
# # job 1
# # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(temp1, 'TestFiles', 'HSNL', 'HSN-fluoro02.CNG.swc')
# swcDir = os.path.join(temp1, 'TestFiles', 'HSNL')
# expNames = [
#             'HSN-fluoro02.CNG',
#             'HSN-fluoro03.CNG',
#             'HSN-fluoro06.CNG',
#             'HSN-fluoro08.CNG',
#             'HSN-fluoro10.CNG',
#             ]
# swcList = [os.path.join(swcDir, expName + '.swc') for expName in expNames]
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'HSNL')
# finallyNormalizeWRT = initRefSWC
#
# # obtains the list of variables in the current work space
# ns = vars()
# # forms the dictionary of parameters to be saved into the parameter file.
# fpars += [{k: ns[k] for k in RegMaxSNParNames}]
#
# npars = []
# # -----------------------------------------------------------------------------------
# # job 2
# # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(temp1, 'TestFiles', 'HSNR', 'HSN-fluoro01.CNG.swc')
# swcDir = os.path.join(temp1, 'TestFiles', 'HSNR')
# expNames = [
#             'HSN-fluoro01.CNG',
#             'HSN-fluoro04.CNG',
#             'HSN-fluoro05.CNG',
#             'HSN-fluoro07.CNG',
#             'HSN-fluoro09.CNG',
#             ]
# swcList = [os.path.join(swcDir, expName + '.swc') for expName in expNames]
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'HSNR')
# finallyNormalizeWRT = initRefSWC
#
# # obtains the list of variables in the current work space
# ns = vars()
# # forms the dictionary of parameters to be saved into the parameter file.
# npars += [{k: ns[k] for k in RegMaxSNParNames}]
# # **********************************************************************************************************************

fpars = []
# -----------------------------------------------------------------------------------
# job 1
# -----------------------------------------------------------------------------------
initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130313-4.swc')
swcDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1')
expNames = [
                'HB130313-4',
                'HB130322-1',
                'HB130326-2',
                'HB130408-1',
                'HB130425-1',
                'HB130501-2',
                'HB130705-1',
                'HB140424-1',
            ]
swcList = [os.path.join(swcDir, expName + '.swc') for expName in expNames]
resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20',
                      'Forager_refHB130313-4')
finallyNormalizeWRT = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1',
                                   'HB130425-1.swc')
ns = vars()
fpars += [{k: ns[k] for k in RegMaxSNParNames}]

# -----------------------------------------------------------------------------------
# job 2
# -----------------------------------------------------------------------------------
initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130501-2.swc')
resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20',
                      'Forager_refHB130501-2')

ns = vars()
fpars += [{k: ns[k] for k in RegMaxSNParNames}]

# -----------------------------------------------------------------------------------
# job 3
# -----------------------------------------------------------------------------------
initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130322-1.swc')
resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20',
                      'Forager_refHB130322-1')

ns = vars()
fpars += [{k: ns[k] for k in RegMaxSNParNames}]


npars = []
# # -----------------------------------------------------------------------------------
# # job 4
# # -----------------------------------------------------------------------------------
initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130605-2.swc')
swcDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1')
expNames = [
                'HB130523-3',
                'HB130605-1',
                'HB130605-2',
                'HB140813-3',
                'HB140917-1',
                'HB140930-1',
                'HB141030-1',
            ]
swcList = [os.path.join(swcDir, expName + '.swc') for expName in expNames]
resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20',
                      'NE_refHB130605-2_scaled5pc')
finallyNormalizeWRT = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1',
                                   'HB130523-3.swc')
ns = vars()
npars += [{k: ns[k] for k in RegMaxSNParNames}]
# -----------------------------------------------------------------------------------
# job 5
# -----------------------------------------------------------------------------------
initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130605-1.swc')
resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20',
                      'NE_refHB130605-1_scaled5pc')
ns = vars()
npars += [{k: ns[k] for k in RegMaxSNParNames}]

# -----------------------------------------------------------------------------------
# job 6
# -----------------------------------------------------------------------------------
initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB140813-3.swc')
resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20',
                      'NE_refHB141030-1_scaled5pc')
ns = vars()
npars += [{k: ns[k] for k in RegMaxSNParNames}]
# **********************************************************************************************************************
#
pars = []
# parFile = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'ParFiles', 'Reg2Reg',
#                        'DL-Int-1_forager3_ne3_subset1.json')
# parFile = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'ParFiles', 'Reg2Reg',
#                        'DL-Int-1_all_min20.json')
parFile = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'ParFiles', 'Reg2Reg',
                       'DL-Int-1_all_NEscaled5pc_min20.json')
# parFile = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'ParFiles', 'Reg2Reg',
#                        'DL-Int-1_F_130322-1_NE_refHB130605-1_scaled5pc.json')
# parFile = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'ParFiles', 'Reg2Reg',
#                        'DL-Int-1_F_130322-1_NE_refHB130605-1_scaled10pc.json')
# parFile = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'ParFiles', 'Reg2Reg',
#                        'HSNL-HSNR.json')
#
#
for fpar, npar in product(fpars, npars):

    refSWCList = [os.path.join(fpar['resDir'], os.path.split(x)[1]) for x in fpar['swcList']]
    testSWCList = [os.path.join(npar['resDir'], os.path.split(x)[1]) for x in npar['swcList']]
    resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg2Reg', 'DL-Int-1_min20',
                          os.path.split(fpar['resDir'])[1] + '_' +
                          os.path.split(npar['resDir'])[1])
    pars += [{k: ns[k] for k in Reg2RegParNames}]


with open(parFile, 'w') as fle:
    json.dump(pars, fle)

