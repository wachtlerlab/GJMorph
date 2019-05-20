import pandas as pd
from scipy.stats import shapiro, mannwhitneyu
import numpy as np
import sys
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from GJMorph.matplotlibRCParams import mplPars
from GJMorph.customStats import art_two_way_anova

def checkNormalityByRegion(densityDataXL, regionMaskingXL, outFig):

    densityDataDF = pd.read_excel(densityDataXL)
    regionMaskingDF = pd.read_excel(regionMaskingXL)

    densityDataDF_indexed = densityDataDF.set_index("voxel center")
    regionMaskingDF_indexed = regionMaskingDF.set_index("voxel center")

    for ind, row in regionMaskingDF_indexed.iterrows():
        if ind in densityDataDF_indexed.index:
            densityDataDF_indexed.loc[ind, "Is Distal?"] = row["Is Distal?"]

    densityWithMaskDF = densityDataDF_indexed.reset_index()

    resDF = pd.DataFrame()

    fig, ax = plt.subplots(figsize=(7, 5.6))
    g = sns.FacetGrid(densityWithMaskDF, row="set name", col="Is Distal?")
    g = g.map(plt.hist, "percentage neurite length", bins=10000)
    g.savefig(outFig, dpi=300)
    

    for isDistal, isDistalDF in densityWithMaskDF.groupby("Is Distal?"):

        for ls, lsDF in isDistalDF.groupby("set name"):

            print("Doing Is Distal ={}, ls={}".format(isDistal, ls))

            tempS = pd.Series()
            stat, pVal = shapiro(lsDF["percentage neurite length"])
            tempS["labor state"] = ls
            tempS["Is Distal?"] = isDistal
            tempS["stat"] = stat
            tempS["P-Value"] = pVal
            tempS['N'] = lsDF.shape[0]

            resDF = resDF.append(tempS, ignore_index=True)

    print(resDF)


def saveAllDataMasked(dataAllXL, masksWNXL, outXL):

    dataAllDF = pd.read_excel(dataAllXL)
    masksWNDF = pd.read_excel(masksWNXL)

    dataAllDF_indexed = dataAllDF.set_index(keys=["voxel center"])
    masksWNDF_indexed = masksWNDF.set_index(keys=["voxel center"])

    for vc, maskRow in masksWNDF_indexed.iterrows():
        print("Setting Is Distal flags for vc={}".format(vc))
        if vc in dataAllDF_indexed.index:
            dataAllDF_indexed.loc[vc, "Is Distal?"] = maskRow["Is Distal?"]

    outputDF = dataAllDF_indexed.reset_index()
    outputDF.to_excel(outXL)

def plotCompareAll(allDataMaskedXL, outBase):

    allDataMaskedDF = pd.read_excel(allDataMaskedXL)
    
    dataAllDF_proxIndexed = allDataMaskedDF.set_index("Is Distal?")

    sns.set(style="whitegrid", rc=mplPars)
    proxFig, proxAx = plt.subplots(figsize=(7, 5.6))
    distalFig, distalAx = plt.subplots(figsize=(7, 5.6))

    sns.violinplot(hue="set name", y="percentage neurite length", x="region",
                    data=dataAllDF_proxIndexed.loc[False, :], ax=proxAx, hue_order=['Newly Emerged', 'Forager'],
                       palette=[(1, 0, 0, 1), (0, 0, 1, 1)],
                    order=["WN", "DB", "VB"], split=True, scale="area", inner=None, cut=0, linewidth=0, scale_hue=False)

    sns.pointplot(hue="set name", y="percentage neurite length", x="region",
                    data=dataAllDF_proxIndexed.loc[False, :], ax=proxAx, hue_order=['Newly Emerged', 'Forager'], palette=['w', 'w'], join=False,
                  estimator=np.median, order=["WN", "DB", "VB"],
                      markers="_", dodge=True, ci=None, size=30)

    sns.violinplot(hue="set name", y="percentage neurite length", x="region",
                    data=dataAllDF_proxIndexed.loc[True, :], ax=distalAx, hue_order=['Newly Emerged', 'Forager'],
                       palette=[(1, 0, 0, 1), (0, 0, 1, 1)],
                    order=["WN", "DB", "VB"], split=True, scale="area", inner=None, cut=0, linewidth=0, scale_hue=False)

    sns.pointplot(hue="set name", y="percentage neurite length", x="region",
                    data=dataAllDF_proxIndexed.loc[True, :], ax=distalAx, hue_order=['Newly Emerged', 'Forager'], palette=['w', 'w'], join=False,
                  estimator=np.median, order=["WN", "DB", "VB"],
                      markers="_", dodge=True, ci=None, size=30)

    columnTempNames = {"voxel center": "vc",
                       "percentage neurite length": "nl",
                       "set name": "ls"}
    alpha = 0.05
    outputDF = pd.DataFrame()

    for isDistal, ax in [[True, distalAx], [False, proxAx]]:
        for region, regionDF in dataAllDF_proxIndexed.loc[isDistal, :].groupby("region"):
            colInd = ["WN", "DB", "VB"].index(region)
            foragerMask = regionDF["set name"] == "Forager"
            neMask = regionDF["set name"] == "Newly Emerged"

            fVals = regionDF.loc[foragerMask, "percentage neurite length"]
            neVals = regionDF.loc[neMask, "percentage neurite length"]

            fMedian = np.median(fVals)
            neMedian = np.median(neVals)

            
            # t, pVal = mannwhitneyu(fVals, neVals)

            tempDF = regionDF.rename(columns=columnTempNames)

            tempDF_reordered = tempDF.loc[:, ["vc", "ls", "initRefs", "nl"]]
            artRes = art_two_way_anova(tempDF_reordered.set_index("vc"))

            tempS = pd.Series()
            tempS["IsDistal"] = isDistal
            tempS["region"] = region
            tempS["Percentage change in Median"] = 100 * (fMedian - neMedian) / neMedian

            if not np.isnan(artRes[1]).any():

                art_correctness, (pVal_ls, pVal_initRefs, pVal_interaction) = artRes

                tempS["ART correctness"] = art_correctness
                tempS["pVal LS"] = pVal_ls
                tempS["pVal initRefs"] = pVal_initRefs
                tempS["pVal_interaction"] = pVal_interaction
                bfCorrectedAlpha = alpha / tempDF["initRefs"].unique().shape[0]

                sigDiffExists = (pVal_interaction > alpha) and \
                           (pVal_ls < bfCorrectedAlpha)
                if sigDiffExists:
                    ax.plot([colInd], [-0.05], "*k", ms=10)

            outputDF = outputDF.append(tempS, ignore_index=True)
            


    proxAx.set_ylim(-0.1, 1)
    proxAx.set_ylabel("$PDL_{voxel}$")
    proxAx.set_xticklabels(("WA", "DB", "VB"))
    proxAx.set_xlabel("")

    distalAx.set_ylim(-0.1, 1)
    distalAx.set_ylabel("$PDL_{voxel}$")
    distalAx.set_xticklabels(("WA", "DB", "VB"))
    distalAx.set_xlabel("")
                    
    proxAx.legend().set_visible(False)
    distalAx.legend().set_visible(False)

    proxFig.tight_layout()
    proxFig.savefig("{}_proximal.png".format(outBase), dpi=300)

    distalFig.tight_layout()
    distalFig.savefig("{}_distal.png".format(outBase), dpi=300)

    outputDF.to_excel("{}.xlsx".format(outBase))

    

if __name__ == "__main__":

    errStr = "Improper usage! Please use as\n" \
                                 "python {currFile} shapiro densityDataXL regionMaskingXL outFig or\n"\
                                 "python {currFile} saveAllDataMasked densityAllXL regionMaskAllXL outXL or\n"\
                                 "python {currFile} plotCompareAll allDataMaskedXL outBase".format(currFile=sys.argv[0])
    
    assert len(sys.argv) in [4, 5], errStr

    if sys.argv[1] == "shapiro":

        checkNormalityByRegion(*sys.argv[2:])

    elif sys.argv[1] == "saveAllDataMasked":

        saveAllDataMasked(*sys.argv[2:])

    elif sys.argv[1] == "plotCompareAll":

        plotCompareAll(*sys.argv[2:])

    else:
        raise(IOError(errStr))
