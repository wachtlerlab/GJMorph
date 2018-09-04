import sys
import os
homeFolder = os.path.expanduser('~')
sys.path.append(homeFolder + '/repos/BlenderSWCVizualizer')
import numpy as np
from blenderHelper import BlenderSWCImporter
import bpy

dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/DL-Int-1/'

fExpNames = [
                # 'HB130313-4',
                # 'HB130322-1',
                # 'HB130326-2',
                # # 'HB130408-1',
                # 'HB130425-1',
                # # 'HB130501-2',
                # 'HB130705-1',
                # 'HB140424-1',
            ]

nExpNames = [
                'HB130523-3',
                'HB130605-1',
                'HB130605-2',
                # 'HB140701-1',
                'HB140813-3',
                'HB140917-1',
                'HB140930-1',
                # 'HB141030-1',
              ]

expNames = fExpNames + nExpNames
# expNames = fExpNames
# expNames = nExpNames
# expNames = ['Forager', 'NE']

refInd = 0
# resDir = os.path.join(homeFolder,  'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20',
#                       'Forager_refHB130313-4')
# resDir = os.path.join(homeFolder,  'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20',
#                       'NE_refHB141030-1')
# resDir1 = os.path.join(homeFolder,  'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1',
#                       'Forager_refHB130408-1')
# resDir2 = os.path.join(homeFolder,  'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1',
#                       'Forager_refHB140424-1')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1',
#                       'NE_refHB130605-1')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1',
#                       'NE_refHB130605-2')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1',
#                       'NE_refHB141030-1')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg2Reg', 'DL-Int-1',
#                       'Forager_refHB130313-4_NE_refHB130605-2')

# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg2Reg', 'DL-Int-1_subset1',
#                       'Forager_refHB130313-4_NE_refHB130605-2', 'FminusNE400p05')

# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg2Reg', 'DL-Int-1',
#                       'Forager_refHB130313-4_NE_refHB130605-2', 'FminusNE400p05')

# resDir = os.path.join(homeFolder,  'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min5',
#                       'Forager_refHB130313-4')
# resDir1 = os.path.join(homeFolder,  'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min5',
#                       'Forager_refHB130408-1')
# resDir2 = os.path.join(homeFolder,  'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min5',
#                       'Forager_refHB140424-1')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min5',
#                       'NE_refHB130605-1')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min5',
#                       'NE_refHB130605-2')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min5',
#                       'NE_refHB141030-1')

# resDir = homeFolder + '/DataAndResults/morphology/Backups/directPixelBased/DL-Int-1_Forager_NE_2015/Forager_NE_norm/'
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/DL-Int-1_Forager_NE/Forager_NE_norm/'
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/DL-Int-1_Forager_NE/Forager_NE/'
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/DL-Int-1_Forager_NE/'
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/DL-Int-1_Foragers/'
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/DL-Int-1_NE/'

# resDir = os.path.join(homeFolder,  'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_subset1',
#                       'Forager_refHB130313-4')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_subset1',
#                       'NE_refHB130605-1')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg2Reg', 'DL-Int-1_subset1',
#                       'Forager_refHB130313-4_NE_refHB130605-1')
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg2Reg', 'DL-Int-1_subset1',
#                       'Forager_refHB130322-1_NE_refHB130605-2')

# resDir1 = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_12Nrns_min20',
#                       'Forager_refHB130425-1')
resDir1 = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_12Nrns_min20',
                      'NE_refHB130523-3')
# resDir2 = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg-MaxS-N', 'DL-Int-1_min20',
#                       'NE_refHB130605-1_scaled5pc')

# resDir2 = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg2Reg', 'DL-Int-1_min20',
#                       'Forager_refHB130322-1_NE_refHB130605-1')
# resDir3 = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg2Reg', 'DL-Int-1_min20',
#                       'Forager_refHB130322-1_NE_refHB130605-1_scaled5pc')
# resDir1 = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg2Reg', 'DL-Int-1_min20',
#                       'Forager_refHB130313-4_NE_refHB130605-1')
# resDir1 = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Reg2Reg', 'DL-Int-1_min20',
#                       'Forager_refHB130501-2_NE_refHB141030-1')

# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', "DL-Int-1Results", "voxelWiseDistAnalysis",
#                       "FMinusNE_vs20_0p05", "Forager_refHB130322-1_NE_refHB130605-2_scaled5pc")
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', "DL-Int-1Results", "voxelWiseDistAnalysis",
#                       "Pooled_NE5Scaled", "FMinusNE_vs20_0p001", "Forager_refHB130322-1_NE_refHB130605-2_scaled5pc")
# resDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', "DL-Int-1Results", "voxelWiseDistAnalysis",
#                       "NestedWelch_NE5pcScaled", "FminusNE_vs20_0p05", "Forager_refHB130322-1_NE_refHB130605-2_scaled5pc")
# ----------------------------------------------------------------------------------------------------------------------

refF = lambda dirPath, fName, resDir: os.path.join(dirPath, fName + '.swc')
finalRefF = lambda resDir: os.path.join(resDir, 'finalRef.swc')
origF = lambda dirPath, fName, resDir: os.path.join(dirPath, fName + '.swc')
origFPart = lambda dirPath, fName, part: os.path.join(dirPath, fName, fName + part + '.swc')
regF = lambda dirPath, fName, resDir: os.path.join(resDir, fName + '.swc')
regFNorm = lambda dirPath, fName, resDir: os.path.join(resDir, fName + '_norm.swc')
regFNormNorm = lambda dirPath, fName, resDir: os.path.join(resDir, fName + '_norm_norm.swc')
regABF = lambda A, B, resDir: os.path.join(resDir, A + '-' + B + '.swc')
startPt = lambda dirPath, fName, resDir: os.path.join(resDir, fName + 'trans', '0.swc')
startPtAB = lambda A, B, resDir: os.path.join(resDir, A + '-' + B + 'trans', '0.swc')
intermediateF = lambda itert, fName, resDir: os.path.join(resDir, fName + 'trans', itert + '.swc')
intermediateFIt = lambda itert, fName, resDir, iterNo: os.path.join(resDir, fName + str(iterNo)
                                                                    + 'trans', itert + '.swc')
regPart = lambda fName, resDir, part: os.path.join(resDir, fName, fName + part + '.swc')
regPartNorm = lambda fName, resDir, part: os.path.join(resDir, fName + '_norm', fName + part + '_norm.swc')
regPartNormNorm = lambda fName, resDir, part: os.path.join(resDir, fName + '_norm_norm',
                                                           fName + part + '_norm_norm.swc')
regIt = lambda resDir, expName, iterNo: os.path.join(resDir, expName + str(iterNo) + '.swc')
regItPart = lambda resDir, expName, iterNo, part: os.path.join(resDir, expName + str(iterNo),
                                                               expName + part + '.swc')
refIt = lambda resDir, iterNo: os.path.join(resDir, 'ref' + str(iterNo) + '.swc')
refdensity = lambda resDir, expName: os.path.join(resDir, 'DensityResults', expName + '_density.sswc')
refDiffDensity = lambda resDir, expName: os.path.join(resDir, 'DensityDiffResults', expName + '_density.sswc')
refDiffDensityPart = lambda resDir, expName, part: os.path.join(resDir, 'DensityDiffResults', expName + part + '_density.sswc')

swcs = []
# swcs.append(refF(dirPath, expNames[refInd], resDir))

iterNo = 0

# swcs.append(refIt(resDir, 0))
# swcs.append(refIt(resDir, 1))
# swcs.append(refIt(resDir, 2))
# swcs.append(refIt(resDir, iterNo - 1))
# swcs.append(refIt(resDir, iterNo))


# swcs.append(finalRefF(resDir))

# expNames = expNames[:5]

for expInd, expName in enumerate(expNames):

    # swcs.append(origF(dirPath, expName, None))
    # swcs.append(origF(testPath, expName, None))
#     swcs.append(origF(dirPath1, expName, None))
#     # swcs.append(origF(dirPath2, expName, None))
#     # swcs.append(regPart(expName, dirPath, '_part0'))
#     # swcs.append(regPart(expName, dirPath, '_part1'))
#     swcs.append(origFPart(dirPath, expName, '-DB'))
#     swcs.append(origFPart(dirPath, expName, '-VB'))
#     swcs.append(origFPart(dirPath, expName, '-MB'))
#     # swcs.append(regIt(resDir, expName, iterNo - 1))
#     swcs.append(regIt(resDir, expName, iterNo))
#     for tempInd in range(7):
#         swcs.append(regIt(resDir, expName, iterNo + tempInd))
#     # swcs.append(regItPart(resDir, expName, iterNo, '_part0'))
#     # swcs.append(regItPart(resDir, expName, iterNo, '_part1'))
#     # swcs.append(intermediateFIt('0', expName, resDir, iterNo))
#     swcs.append(regF(None, expName, resDir))
    swcs.append(regF(None, expName, resDir1))
#     swcs.append(regF(None, expName, resDir2))
    # swcs.append(regF(None, expName, resDir3))
#     # swcs.append(regF(None, expName, resDir4))
#     swcs.append(regF(None,  expName + '-WN', resDir + '-WN'))
#     swcs.append(regF(None, expName + '-VB', resDir + '-VB'))
#     swcs.append(regF(None, expName + '-DB', resDir + '-DB'))
#     swcs.append(regF(None, expName + '-MB', resDir + '-MB'))

    # swcs.append(regF(None, expName + '-VB', resDir))
    # swcs.append(regF(None, expName + '-DB', resDir))
    # swcs.append(regF(None, expName + '-MB', resDir))
    # swcs.append(regF(None, expName + '-WN', resDir))


#     # swcs.append(regPart(expName, resDir, '_part0'))
#     # swcs.append(regPart(expName, resDir, '_part1'))
#     # swcs.append(regFNorm(None, expName, resDir))
#     # swcs.append(regFNormNorm(None, expName, resDir))
#     # swcs.append(regPartNorm(expName, resDir, '_part1'))
#     swcs.append(regPart(expName, resDir, '-VB'))
#     swcs.append(regPart(expName, resDir, '-DB'))
#     swcs.append(regPart(expName, resDir, '-MB'))
#     swcs.append(regPart(expName, resDir, '-WN'))
#     swcs.append(regPart(expName, resDir1, '-VB'))
#     swcs.append(regPart(expName, resDir2, '-VB'))

#     # swcs.append(refdensity(resDir, expName))
#     # swcs.append(refDiffDensityPart(resDir, expName, '_part1'))
#
    # swcs.append(origF(testPath, expName, None))
    # swcs.append(refF(refPath, expName, None))
#     # swcs.append(startPt(None, expName, resDir))
#
    # if expInd != refInd:
    # if True:
    #
    #     # swcs.append(origF(dirPath1, expName, None))
    #     # swcs.append(regABF(expName, expNames[refInd], resDir))
    #     # swcs.append(startPtAB(expName, expNames[refInd], resDir))
    #     # swcs.append(regF(None, expName, resDir))

        # swcs.append(regF(None, expName, resDir1))
        # swcs.append(regF(None, expName, resDir2))
        # swcs.append(regF(None, expName, resDir3))
        # swcs.append(regF(None, expName, resDir4))
    #     # swcs.append(startPt(dirPath, expName, resDir))
    #     #
    #     # # swcs.append(intermediateF('0', expName, resDir))
    #     # swcs.append(intermediateF('11r', expName, resDir))
    #     # swcs.append(intermediateF('4r', expName, resDir))
    #       swcs.append(regF(None, expNames[refInd] + '-' + expName, resDir))

# temp = "/home/aj/pCloudDrive/pCloudSync/Documents/talks/CNS Seminar/" \
#        "Reg-MaxS/methods_Reg-MaxS/Reg-MaxS/VGlut-F-300181_Standardized-VGlut-F-500147.CNGtrans"
#
# tempSWCNames = [
#     "0", "0t", "1r", "2t", "3r", "4t", "5r", "6s", "7t", "8r", "9s"]
#
# for tempSWCName in tempSWCNames:
#     swcs.append(origF(temp, tempSWCName, None))

# swcs = ['/tmp/HSN-fluoro02.CNG.swc', '/tmp/2.swc']
# swcs = [
#     '/home/ajay/repos/btmorph_v2/tests/resampleTest/v_e_moto1.CNG_resampled0p5.swc',
#     '/home/ajay/repos/btmorph_v2/tests/resampleTest/v_e_moto1.CNG.swc',
#         ]

# swcs = [
#     '/home/aj/ownCloud/GinJang_data/GinJang_Teamwork/Manuscripts/Ai_et_al_2017/CoverArt/HB140930-1flipRegist.swc',
#     '/home/aj/ownCloud/GinJang_data/GinJang_Teamwork/Manuscripts/Ai_et_al_2017/CoverArt/HB130119-1regist.swc',
#     '/home/aj/ownCloud/GinJang_data/GinJang_Teamwork/Manuscripts/Ai_et_al_2017/CoverArt/HB131217-2regist.swc',
# ]

# swcs += [
#     "/home/aj/DataAndResults/ImagingAndReconstruction/130425-1_tryAJ/HB130425-1-somaNeurite.swc"
# ]

# ----------------------------------------------------------------------------------------------------------------------
# cols = [[ 0.        ,  0.        ,  0.5       ],
#         [ 0.        ,  0.00196078,  1.        ],
#         [ 0.        ,  0.50392157,  1.        ],
#         [ 0.08538899,  1.        ,  0.88235294],
#         [ 0.49019608,  1.        ,  0.47754586],
#         [ 0.89500316,  1.        ,  0.07273877],
#         [ 1.        ,  0.58169935,  0.        ],
#         [ 1.        ,  0.11692084,  0.        ]]

brightRed, brightGreen, blue, magenta, cyan, lime_green = [
                                            [1, 0, 0],
                                            [0, 1, 0],
                                            [0, 0, 1],
                                            [1, 0, 1],
                                            [0, 1, 1],
                                            [1, 1, 0]
                                          ]
darkViolet = [0.224, 0, 1]
darkGreen = [0, 0.5, 0]
darkRed = [0.5, 0, 0]
white = [1, 1, 1]

snsMagenta = [0.667, 0.000, 0.667]
snsRed = [0.667, 0.00, 0.00]
snsYellow = [0.667, 0.667, 0.000]
snsGreen = [0.000, 0.667, 0.000]
snsLightBlue = [0, 0.667, 0.667]
snsDarkBlue = [0, 0, 0.667]


# baseCols = np.array([snsGreen, snsMagenta, snsLightBlue, snsGreen, snsMagenta, snsLightBlue])

#
# baseCols = np.concatenate([baseCols] * 3)

# baseCols = np.array([[0, 0, 1], [1, 0, 0]])

# baseCols = np.array([[ 1.        ,  0.58169935,  0.        ]])

# cols = np.array([[27, 158, 119], [231, 41, 138]]) / 256.




# # 4 color jet
# darkBlue, brightBlue, yellow, darkRed  = np.array([[0.        , 0.        , 0.5],
#                                                    [ 0.        ,  0.83333333,  1.        ],
#                                                    [ 1.        ,  0.90123457,  0.        ],
#                                                    [ 0.5       ,  0.        ,  0.        ]])



# baseCols = np.array([snsGreen, snsGreen,
#                      snsDarkBlue, snsDarkBlue,
#                      snsRed, snsRed
#                      ])

# baseCols = np.array([snsDarkBlue, snsLightBlue, snsGreen, snsYellow, snsMagenta, snsRed])

# cols = [[0, 0.2, 0.2], [0.1, 0, 0.1]]

baseCols = np.asarray(   [[1.0, 0.11692084, 0.0],
                         [1.0, 0.58169935, 0.0],
                         [0.89500316, 1.0, 0.07273877],
                         [0.49019608, 1.0, 0.47754586],
                         [0.08538899, 1.0, 0.88235294],
                         [0.0, 0.50392157, 1.0],
                         [1.0, 0.11692084, 0.0],
                         [0.0, 0.0, 0.5]] )


# baseCols = []
# for i in range(15):
#     baseCols.extend([snsRed, snsDarkBlue])
# baseCols = np.array(baseCols)

nPts = baseCols.shape[0]
nSWC = len(swcs)

if nPts == nSWC:
    cols = baseCols
else:
    cols = np.zeros([nSWC, 3])


    for ind in range(3):
        cols[:, ind] = np.interp(np.linspace(0, nPts, nSWC), range(nPts), baseCols[:, ind])




# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------Colors of SSWC Materials--------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

nPts = 8

# density value of 0 indicates newlyEmergedDensity-foragerDensity=1
SbaseCols = np.array([
    [ 0.78235294,  0.        ,  0.        ,  1.        ],
    [ 1.        ,  0.14509804,  0.14509804,  1.        ],
    [ 1.        ,  0.70980392,  0.70980392,  1.        ],
    [ 0.73333333,  0.89019608,  0.03921569,  0.5       ],
    [ 0.73333333,  0.89019608,  0.03921569,  0.5       ],
    [ 0.70980392,  0.70980392,  1.        ,  1.        ],
    [ 0.14509804,  0.14509804,  1.        ,  1.        ],
    [ 0.        ,  0.        ,  0.69529412,  1.        ]
    ]
    )

# SbaseCols = np.array([[0.78235294, 0., 0., 1.],
#                       [1., 1., 1., 0.5],
#                       [1., 1., 1., 0.5],
#                       [1., 1., 1., 0.5],
#                       [1., 1., 1., 0.5],
#                       [1., 1., 1., 0.5],
#                       [1., 1., 1., 0.5],
#                       [0., 0., 0.69529412, 1.]])

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------Emit values of SSWC Materials--------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
emits = [1 for x in range(nPts)]
# ----------------------------------------------------------------------------------------------------------------------
# --------------------------Alpha values of SSWC Materials--------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
alphas = [1 for x in range(nPts)]
# alphas = [1, 1, 1, 0.5, 0.5, 1, 1, 1]
# ----------------------------------------------------------------------------------------------------------------------

if nPts % len(SbaseCols) > 0:
    raise(ValueError('nPts must be a integral multiple of ' + str(len(SbaseCols))))

Scols = np.zeros([nPts, 3])
scaleFactor = int(nPts / len(SbaseCols))

for ind in range(3):
    Scols[:, ind] = np.interp(range(nPts), range(0, nPts, scaleFactor), SbaseCols[:, ind])

# ----------------------------------------------------------------------------------------------------------------------
nrnsBlender = []
matchOrigin = False


for nrnInd, nrn in enumerate(swcs):

    if nrnInd == 0:
        add = False
    else:
        add = True

    # tmpB = BlenderSWCImporter(nrn, add, matchOrigin, colMap=cols)
    # tmpB.importWholeSWC()

    # matchOrigin = True

    sswcMaterials = []
    for scolInd, scol in enumerate(Scols):
        mat = bpy.data.materials.new("Material {}".format(scolInd))
        mat.use_transparency = True
        mat.diffuse_color = scol
        mat.diffuse_intensity = 1.0
        mat.alpha = alphas[scolInd]
        mat.emit = emits[scolInd]
        sswcMaterials.append(mat)

    tmpB = BlenderSWCImporter(os.path.abspath(nrn), add, matchOrigin, sswcMaterials=sswcMaterials)
    tmpB.importWholeSWC(col=cols[nrnInd])

    nrnsBlender.append(tmpB)


# tmpB.addSphere(position=[0, 0, 0], col=[1, 0, 0], radius=2)
