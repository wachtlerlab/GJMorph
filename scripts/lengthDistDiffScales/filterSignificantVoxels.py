import pandas as pd
import sys
from scipy.stats import ttest_ind
from GJMorph.pandasFuncs import dfInterHueFunc
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from GJMorph.matplotlibRCParams import mplPars


if __name__ == '__main__':

    assert len(sys.argv) == 3, 'Improper usage! Please use as \'python filterSignificantVoxels.py ' \
                               '<dataXL> <outputBase>\''

    dataXL = sys.argv[1]
    outBase = sys.argv[2]

    def welchTestAndMeanStatsFVNE(ser):

        foragerData = ser['neurite length']["Forager"]
        neData = ser['neurite length']["Newly Emerged"]
        foragerValues = foragerData.values
        neValues = neData.values

        tStat, pVal = ttest_ind(foragerValues, neValues, equal_var=False)
        foragerMean = foragerValues.mean()
        neMean = neValues.mean()
        meanDiff = foragerMean - neMean
        maxMean = max(foragerMean, neMean)
        if maxMean == 0:
            pcRedux = 0
        else:
            pcRedux = 100 * meanDiff / maxMean


        return pd.Series({"T-Statistic": tStat,
                          "P-Value": pVal,
                          "Difference of Means": meanDiff,
                          "Maximum of Means": maxMean,
                          "Percentage Change": pcRedux})

    dataDF = pd.read_excel(dataXL, index_col=0)

    # unstacking is required to fill up the sparse data with zeros
    indexedDF = dataDF.set_index(keys=["voxel size", 'voxel center', 'set name', 'expID', "initRefs"])
    pivotedDF = indexedDF.unstack(level=('set name', "initRefs", 'expID'), fill_value=0)

    dataFullDF = pivotedDF.stack(level=('set name', "initRefs", "expID")).reset_index()
    tmp2 = dataFullDF.groupby(["voxel size", 'voxel center', "set name", "initRefs"])
    averageNLWithinIR = tmp2.mean()
    averageNLWithinIRPivoted = averageNLWithinIR.unstack(level=("set name", "initRefs"), fill_value=0)

    sigsForInitRefs = pd.DataFrame()

    for initRef, irDF in dataFullDF.groupby("initRefs"):
        tmp = irDF.set_index(keys=["voxel size", 'voxel center', "set name", "expID"])
        del tmp["initRefs"]
        tmp1 = tmp.unstack(level=("set name", "expID"), fill_value=0)
        mask = tmp1.apply(lambda x: np.any(x.values), axis=1)
        tmp1 = tmp1.loc[mask, :]
        currVCStats = tmp1.apply(welchTestAndMeanStatsFVNE, axis=1)
        currVCStats["initRefs"] = initRef
        sigsForInitRefs = sigsForInitRefs.append(currVCStats)


    sigsAcrossAveragesForIRs = averageNLWithinIRPivoted.apply(welchTestAndMeanStatsFVNE, axis=1)


    # for voxelCenter, vcDF in dataDF.groupby("voxel center"):
    #
    #     statsSForAvgs = dfInterHueFunc(data=averageNLWithinIR, hue="set name", func=welchTestAndMeanStatsFVNE,
    #                                    pars=["neurite length"], outLabels=["T-Stat", "P-Value",
    #                                                                     "Difference of Means",
    #                                                                     "Maximum of Means",
    #                                                                     "Percentage Change"])
    #
    #     statsSForAvgs["voxel center"] = voxelCenter
    #     sigsAcrossAveragesForIRs = sigsAcrossAveragesForIRs.append(statsSForAvgs, ignore_index=True)
    #
    #     for initRef, initRefDF in vcDF.groupby("initRefs"):
    #         statsS = dfInterHueFunc(data=initRefDF, hue="set name", func=welchTestAndMeanStatsFVNE,
    #                                 pars=["neurite length"], outLabels=["T-Stat", "P-Value",
    #                                                                     "Difference of Means",
    #                                                                     "Maximum of Means",
    #                                                                     "Percentage Change"])
    #
    #
    #         statsS["initRefs"] = initRef
    #         statsS["voxel center"] = voxelCenter
    #         sigsForInitRefs = sigsForInitRefs.append(statsS, ignore_index=True)

    sigsForIRFiltered0p05 = sigsForInitRefs.loc[lambda x: x["P-Value"] < 0.05, :]
    sigsForIRFiltered0p01 = sigsForInitRefs.loc[lambda x: x["P-Value"] < 0.01, :]

    sigsForAvgIRsFiltered0p05 = sigsAcrossAveragesForIRs.loc[lambda x: x["P-Value"] < 0.05, :]
    sigsForAvgIRsFiltered0p01 = sigsAcrossAveragesForIRs.loc[lambda x: x["P-Value"] < 0.01, :]
    sigsForAvgIRsFiltered0p01.loc[:, "Number of InitRefs for \nwhich difference is significant"] = \
        sigsForIRFiltered0p01.groupby(by=["voxel size", "voxel center"]).count()["P-Value"]
    sigsForAvgIRsFiltered0p01.fillna(0, inplace=True)
    sigsForAvgIRsFiltered0p01.reset_index(inplace=True)
    sigsForAvgIRsFiltered0p05.loc[:, "Number of InitRefs for \nwhich difference is significant"] = \
        sigsForIRFiltered0p05.groupby(by=["voxel size", "voxel center"]).count()["P-Value"]
    sigsForAvgIRsFiltered0p05.fillna(0, inplace=True)
    sigsForAvgIRsFiltered0p05.reset_index(inplace=True)

    sigsAcrossAveragesForIRs.reset_index(inplace=True)
    sigsAcrossAveragesForIRs.to_excel("{}_acrossAvgs_all.xlsx".format(outBase), index=False)
    sigsForAvgIRsFiltered0p01.to_excel("{}_acrossAvgs_filtered0p01.xlsx".format(outBase), index=False)
    sigsForAvgIRsFiltered0p05.to_excel("{}_acrossAvgs_filtered0p05.xlsx".format(outBase), index=False)

    sigsForInitRefs.reset_index(inplace=True)
    sigsForIRFiltered0p01.reset_index(inplace=True)
    sigsForIRFiltered0p05.reset_index(inplace=True)
    sigsForInitRefs.to_excel("{}_forInitRefs_all.xlsx".format(outBase), index=False)
    sigsForIRFiltered0p05.to_excel("{}_forInitRefs_filtered0p05.xlsx".format(outBase), index=False)
    sigsForIRFiltered0p01.to_excel("{}_forInitRefs_filtered0p01.xlsx".format(outBase), index=False)


