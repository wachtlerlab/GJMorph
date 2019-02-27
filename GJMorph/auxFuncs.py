import numpy as np


# **********************************************************************************************************************
def resampleSWC(swcFile, resampleLength, mask=None, swcData=None, calculateBranchLens=False):
    '''
    Resample the SWC points to place points at every resamplelength along the central line of every segment. Radii are interpolated.
    :param swcData: nx4 swc point data
    :param resampleLength: length at with resampling is done.
    :return:    branchCenters, branchLens,
                ndarray of shape (#pts, 7) with each row containing (node ID, node type, x, y, z, r, parent ID)
    '''

    if swcData is None:
        swcData = np.loadtxt(swcFile)
    inds = swcData[:, 0].tolist()
    oldNewDict = {}

    currentMax = 1
    if mask is None:
        mask = [True] * swcData.shape[0]
    else:
        assert len(mask) == swcData.shape[0], 'Supplied mask is invalid for ' + swcFile
    resampledSWCData = []

    getSegLen = lambda a, b: np.linalg.norm(a - b)

    if calculateBranchLens:
        branchCenters = []
        branchLens = []
    totalLen = 0
    for pt in swcData:

        if pt[6] < 0:
            if mask[inds.index(int(pt[0]))]:
                resampledSWCData.append([currentMax] + pt[1:].tolist())
                oldNewDict[pt[0]] = currentMax
                currentMax += 1

        if (pt[6] > 0) and (int(pt[6]) in inds):
            if mask[inds.index(int(pt[0]))]:

                parentPt = swcData[inds.index(pt[6]), :]
                segLen = getSegLen(pt[2:5], parentPt[2:5])
                totalLen += segLen
                currentParent = oldNewDict[pt[6]]

                if segLen > resampleLength:

                    temp = pt[2:5] - parentPt[2:5]
                    distTemp = np.linalg.norm(temp)
                    unitDirection = temp / distTemp
                    radGrad = (pt[5] - parentPt[5]) / distTemp



                    for newPtsInd in range(1, int(np.floor(segLen / resampleLength)) + 1):

                        temp = [currentMax, pt[1]] + \
                               (parentPt[2:5] + newPtsInd * resampleLength * unitDirection).tolist()
                        temp.append(parentPt[5] + newPtsInd * radGrad * resampleLength)
                        if calculateBranchLens:
                            branchLens.append(resampleLength)
                            branchCenters.append(parentPt[2:5] + (newPtsInd - 0.5) * resampleLength * unitDirection)
                        temp.append(currentParent)
                        currentParent = currentMax
                        currentMax += 1
                        resampledSWCData.append(temp)

                    if calculateBranchLens:
                        branchCenters.append(0.5 * (pt[2:5] + np.array(resampledSWCData[-1][2:5])))
                        branchLens.append(np.linalg.norm(pt[2:5] - np.array(resampledSWCData[-1][2:5])))
                    resampledSWCData.append([currentMax] + pt[1:6].tolist() + [currentParent])
                    oldNewDict[pt[0]] = currentMax
                    currentMax += 1


                else:
                    if calculateBranchLens:
                        branchCenters.append(0.5 * (pt[2:5] + parentPt[2:5]))
                        branchLens.append(segLen)
                    resampledSWCData.append([currentMax] + pt[1:6].tolist() + [currentParent])
                    oldNewDict[pt[0]] = currentMax
                    currentMax += 1

    if calculateBranchLens:
        return np.array(branchCenters), np.array(branchLens), np.array(resampledSWCData)
    else:
        return totalLen, np.array(resampledSWCData)

#***********************************************************************************************************************

def windowSWCPts(branchMeans, gridSize, translationIndicator=(0, 0, 0)):
    """
    Custom internal function, use at your own risk!

    Approximates points represented by rows of branchMeans to nearest voxel centers, where voxels are cubes of side
    <gridSize> and are constructed so that there is a voxel with center at the origin. If translationIndicator is
    specified, then the voxels are constructed in a way such that a voxel has a center at
    - <translationIndicator> * <gridSize> * 0.5.
    :param branchMeans: np.array of shape (nRows, 3)
    :param gridSize: float
    :param translationIndicator: three member iterable of floats
    :return: voxelCenters, np.array of shape (nRows, 3), rounded to 6 digits
    """

    offset = np.array(translationIndicator) * gridSize * 0.5
    temp = branchMeans + offset
    voxelCenters = np.array(np.round(temp / gridSize), dtype=np.int32) * gridSize - offset
    return np.round(voxelCenters, 6)

#***********************************************************************************************************************