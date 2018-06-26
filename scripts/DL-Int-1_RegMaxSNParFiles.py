"""
A copy of regmaxsn.scripts.utils.constructRegMaxSNParFile adapted to work with DL-Int-1 data.
"""

import json
import os
from itertools import product

from numpy import pi, deg2rad

from regmaxsn.core.RegMaxSPars import RegMaxSNParNames
from GJMorph.folderDefs import homeFolder

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
gridSizes = [160.0, 80.0, 40.0, 20.0]
transBounds = [[-30, 30], [-30, 30], [-30, 30]]
transMinRes = 1
rotBounds = [[-pi / 6, pi / 6], [-pi / 6, pi / 6], [-pi / 6, pi / 6]]
rotMinRes = deg2rad(1).round(4)
scaleBounds = [[0.5, 1 / 0.5], [0.5, 1 / 0.5], [0.5, 1 / 0.5]]
minScaleStepSize = 1.005
usePartsDir = True
nCPU = 6
maxIter = 100


pars = []
parFile = os.path.join(homeFolder, "DataAndResults", "morphology",
                       'ParFiles', 'Reg-MaxS-N', 'DL-Int-1_min20_all.json')
# parFile = os.path.join(homeFolder, "DataAndResults", "morphology",
#                        'ParFiles', 'Reg-MaxS-N', 'DL-Int-1_N_141030-1.json')
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
pars += [{k: ns[k] for k in RegMaxSNParNames}]

# -----------------------------------------------------------------------------------
# job 2
# -----------------------------------------------------------------------------------
initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130501-2.swc')
resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20',
                      'Forager_refHB130501-2')

ns = vars()
pars += [{k: ns[k] for k in RegMaxSNParNames}]

# -----------------------------------------------------------------------------------
# job 3
# -----------------------------------------------------------------------------------
initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130322-1.swc')
resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20',
                      'Forager_refHB130322-1')

ns = vars()
pars += [{k: ns[k] for k in RegMaxSNParNames}]


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
resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20', 'NE_refHB130605-2')
finallyNormalizeWRT = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1',
                                   'HB130523-3.swc')
ns = vars()
pars += [{k: ns[k] for k in RegMaxSNParNames}]

# -----------------------------------------------------------------------------------
# job 5
# -----------------------------------------------------------------------------------
initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB130605-1.swc')
resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20', 'NE_refHB130605-1')
ns = vars()
pars += [{k: ns[k] for k in RegMaxSNParNames}]

# -----------------------------------------------------------------------------------
# job 6
# -----------------------------------------------------------------------------------
initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB141030-1.swc')
resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20', 'NE_refHB141030-1')
ns = vars()
pars += [{k: ns[k] for k in RegMaxSNParNames}]
# **********************************************************************************************************************
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


# # # -----------------------------------------------------------------------------------
# # # job 4
# # # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1', 'HB141030-1.swc')
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
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20', 'NE_refHB141030-1')
# finallyNormalizeWRT = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1',
#                                    'HB130523-3.swc')
# ns = vars()
# pars += [{k: ns[k] for k in RegMaxSNParNames}]
# # **********************************************************************************************************************
# write the parameters into the parameter file.
with open(parFile, 'w') as fle:
    json.dump(pars, fle)

