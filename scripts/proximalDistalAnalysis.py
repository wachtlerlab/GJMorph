import pandas as pd
from GJMorph.auxFuncs import windowSWCPts
from btmorph2 import NeuronMorphology
from scipy.spatial import cKDTree
from ast import literal_eval as make_tuple
from regmaxsn.core.swcFuncs import readSWC_numpy, writeSWC_numpy
import numpy as np
import sys
import os


def generate_raw_data(inputXL, outputCSV, gridSize):
    """
    For each swc in inputXL, and for every node in each swc, Terminal proximity is calculated, its
    XYZ is approximated to the center of the voxel which contains it
    :param inputXL:
    :param outputXL:
    :param gridSize:
    :return:
    """
    inputDF = pd.read_excel(inputXL)

    tempDFs = []

    for rowInd, (expId, laborState, initRefs, swcFile) in inputDF.iterrows():
        print("Doing {}".format(swcFile))

        nrn = NeuronMorphology(swcFile, ignore_type=True, correctIfSomaAbsent=True)

        terminal_proxs_dict = nrn.get_terminal_proximities_all_nodes()

        nodeXYZs = []
        terminal_proxs = []
        for node_ind, terminal_prox in terminal_proxs_dict.iteritems():
            nodeXYZs.append(nrn.tree.get_node_with_index(node_ind).content["p3d"].xyz)
            terminal_proxs.append(terminal_prox)
        nodeXYZs = np.array(nodeXYZs)

        centers = windowSWCPts(nodeXYZs, gridSize)

        tempDF = pd.DataFrame()
        tempDF.loc[:, 'voxel center'] = map(tuple, centers)
        tempDF.loc[:, 'terminal proximity'] = terminal_proxs
        tempDF.loc[:, 'set name'] = laborState
        tempDF.loc[:, 'expID'] = expId
        tempDF.loc[:, "initRefs"] = initRefs
        tempDF.loc[:, 'voxel size'] = gridSize
        tempDFs.append(tempDF)

    rawDF = pd.concat(tempDFs, ignore_index=True)

    rawDF.to_csv(outputCSV)


def classify_proximal_distal(dataCSV, outXL, thres):

    dataDF = pd.read_csv(dataCSV, index_col=0)

    dataDFRestricted = dataDF.loc[:, ["voxel center", "terminal proximity"]]
    medianTerminalProximityDF = pd.DataFrame()
    medianTerminalProximityDF["terminal proximity"] = dataDFRestricted.groupby("voxel center").apply(np.median)

    medianTerminalProximityDF["Is Distal?"] = medianTerminalProximityDF["terminal proximity"] > thres
    medianTerminalProximityDF["voxel size"] = dataDF["voxel size"].iloc[0]

    medianTerminalProximityDF.to_excel(outXL)


def generateDistalColoredSSWCs(distalIndicatorXL, inputXL, outDir):

    if not os.path.isdir(outDir):
        os.mkdir(outDir)

    inputDF = pd.read_excel(inputXL)
    distalIndicatorDF = pd.read_excel(distalIndicatorXL)
    gridSize = distalIndicatorDF["voxel size"].iloc[0]

    finalVoxelSet = map(make_tuple, distalIndicatorDF["voxel center"])
    finalVoxelKDTree = cKDTree(finalVoxelSet, leafsize=100)

    # distalIndicatorDF.set_index("voxel center", inplace=True)

    for rowInd, (expId, laborState, initRefs, swcFile) in inputDF.iterrows():
        print("Doing {}".format(swcFile))

        headr, swcData = readSWC_numpy(swcFile)

        nearestInGridDist, nearestInGridIndices = \
                                                  finalVoxelKDTree.query(swcData[:, 2:5], n_jobs=6)
        

        extraCol = np.array(distalIndicatorDF["Is Distal?"].iloc[nearestInGridIndices].values, dtype=int)
        extraCol = extraCol.reshape((extraCol.shape[0], 1))
        sswcData = np.concatenate((swcData, extraCol), axis=1)

        initRefDir = os.path.join(outDir, initRefs)

        if not os.path.isdir(initRefDir):
            os.mkdir(initRefDir)

        outSWC = os.path.join(initRefDir, os.path.split(swcFile)[1])
        writeSWC_numpy(outSWC, sswcData, headr)



if __name__ == "__main__":

    assert len(sys.argv) in [5], "Improper Usage! Please use as\n" \
                                 "python {currFile} genRawData <inputXL> <outputCSV> <gridSize>" \
                                 "python {currFile} classify <inputCSV> <outputXL> <thresh>" \
                                 "python {currFile} genSSWC <classificationXL> <inputXL> <outdir>" \
                                 "".format(currFile=sys.argv[0])

    if sys.argv[1] == "genRawData":
        generate_raw_data(*(sys.argv[2:-1] + [int(sys.argv[-1])]))
    elif sys.argv[1] == "classify":
        classify_proximal_distal(*sys.argv[2:-1] + [float(sys.argv[-1])])
    elif sys.argv[1] == "genSSWC":
        generateDistalColoredSSWCs(*sys.argv[2:])
