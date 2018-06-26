import sys
import os
import pandas as pd
from regmaxsn.core.swcFuncs import readSWC_numpy, writeSWC_numpy
import seaborn as sns
import numpy as np
from ast import literal_eval as make_tuple
from scipy.spatial import cKDTree
from GJMorph.matplotlibRCParams import mplPars

if __name__ == '__main__':

    sns.set(rc=mplPars)

    assert len(sys.argv) == 4, 'Improper usage! Please use as \'python sigVoxelsAcrossInits.py <inputXL>' \
                               '<filteredDataXL> ' \
                               '<outDir>\''

    inputXL = sys.argv[1]
    filteredDataXL = sys.argv[2]
    mainOutDir = sys.argv[3]

    meanDiffCappedAt = 40
    fractionInitRefsSignifLimit = 0.65

    inDF = pd.read_excel(inputXL)
    nInitRefs = inDF["initRefs"].unique().size
    nInitRefsLimit = nInitRefs * fractionInitRefsSignifLimit

    filteredDataDF = pd.read_excel(filteredDataXL, index_col=0)
    criterion = lambda x: x["Significant Difference"] == 1
    filteredDataFilteredDF = filteredDataDF.loc[criterion, :]
    finalVoxelSet = map(make_tuple, filteredDataFilteredDF["voxel center"])
    voxelSize = filteredDataFilteredDF["voxel size"].iloc[0]
    finalVoxelKDTree = cKDTree(finalVoxelSet, leafsize=100)



    for rowInd, (expId, laborState, initRefs, swcFile) in inDF.iterrows():

        print('Doing {}'.format(swcFile))
        headr, swcData = readSWC_numpy(swcFile)

        outDir = os.path.join(mainOutDir, initRefs)
        if not os.path.isdir(outDir):
            os.makedirs(outDir)
        if len(finalVoxelSet) > 0:

            nearestInGridDist, nearestInGridIndices = \
                finalVoxelKDTree.query(swcData[:, 2:5], distance_upper_bound=voxelSize / 2, n_jobs=6)

            nodepresences = nearestInGridDist != np.inf
            # when a nearest neighbor with specified distance is not found
            nearestInGridIndices[nearestInGridIndices == len(finalVoxelKDTree.data)] = 0
            temp1 = finalVoxelKDTree.data[nearestInGridIndices]
            temp2 = map(str, map(tuple, temp1))
            tempDF = filteredDataFilteredDF.set_index("voxel center")
            temp3 = np.minimum(
                np.maximum(tempDF.loc[temp2, "Difference of Means"].values, -meanDiffCappedAt),
                               meanDiffCappedAt)
            temp = np.array(nodepresences, dtype=np.float) * temp3

            nodeHLs = temp.reshape((swcData.shape[0], 1))

            finalSWCData = np.concatenate((swcData, nodeHLs), axis=1)

            finalSWCData = np.concatenate((finalSWCData,
                                               np.array([[finalSWCData[:, 0].max() + 1, 1] +
                                                          finalSWCData[0, 2:5].tolist() +
                                                          [0.00001] +
                                                          [finalSWCData[:, 6].min() - 1, meanDiffCappedAt]]
                                                        )), axis=0)

            finalSWCData = np.concatenate((finalSWCData,
                                           np.array([[finalSWCData[:, 0].max() + 1, 1] +
                                                     finalSWCData[0, 2:5].tolist() +
                                                     [0.00001] +
                                                     [finalSWCData[:, 6].min() - 1, -meanDiffCappedAt]])), axis=0)

            outFle = os.path.join(outDir, "{}.swc".format(expId))
            writeSWC_numpy(outFle, finalSWCData, headr)









    # with sns.axes_style('darkgrid'):
    #
    #     fig1, ax1 = plt.subplots(figsize=(14, 11.2), sharex=True)
    #
    #     # sns.violinplot(x='voxel center', y='HL Estimate',
    #     #                data=allSigVoxelDF, ax=ax1[0], palette='Set2', scale='count', width=0.9)
    #     sns.stripplot(x='voxel center', y='HL Estimate', data=allSigVoxelDF, ax=ax1,
    #                   jitter=True, palette='Set2', size=10)
    #     ax1.grid(True)
    #
    #     tempY = max(allSigVoxelDF['HL Estimate']) * 1.2
    #     tempTicks = ax1.get_xticks()
    #
    #
    #     for xtick, xlabel, col in zip(tempTicks, ax1.get_xticklabels(), sns.color_palette('Set2', len(tempTicks))):
    #
    #         ax1.text(xtick, tempY, str(countDF.loc[xlabel.get_text(), 'voxel size']),
    #                  ha='center', va='center', color=col)
    #
    #     ax1.set_xticklabels([x.get_text().replace('.0', '') for x in ax1.get_xticklabels()], rotation=90)
    #     fig1.suptitle('voxel size={}'.format(voxelSize2Use))
    #
    # fig1.tight_layout()
    # raw_input('Enter any key to exit...')