import os
import pandas as pd
from btmorph2 import NeuronMorphology
import numpy as np
from GJMorph.matplotlibRCParams import mplPars, openCircleMarker
import seaborn as sns
from matplotlib import pyplot as plt
import sys
from scipy.stats import ttest_ind
from GJMorph.pandasFuncs import dfInterHueFunc


# ----------------------------------------------------------------------------------------------------------------------
binEdges = np.arange(0, 350, 20)
binCenters = binEdges[:-1] + 0.5 * (binEdges[1] - binEdges[0])
# manually entered value of origin. It is the average of the roots of all WN morphologies.
origin = [254.79213333, 119.54293333, 168.7052]
# ----------------------------------------------------------------------------------------------------------------------


def saveData(inXL, dataXL, origin=origin):

    inDF = pd.read_excel(inXL)

    dataDF = pd.DataFrame()

    for rowInd, (expId, laborState, initRefs, swcFile) in inDF.iterrows():

        print("Doing {}".format(swcFile))
        nm = NeuronMorphology(swcFile, correctIfSomaAbsent=True, ignore_type=True)
        lengths = nm.getLengthVsDistance(radii=binEdges[1:], centeredAt=origin)
        percentageLengths = np.array(lengths) * 100 / float(sum(lengths))

        for binCenter, pcLength in zip(binCenters, percentageLengths):
            tempS = pd.Series()
            tempS["Experiment ID"] = expId
            tempS["Labor State"] = laborState
            tempS["Bin Center $(\mu m)$"] = binCenter
            tempS["Percentage Dendritic Length"] = pcLength
            tempS["swc File"] = swcFile
            tempS["initRefs"] = initRefs
            dataDF = dataDF.append(tempS, ignore_index=True)

    dataDF.to_excel(dataXL)


def plotData(dataXL, outFig):

    dataDF = pd.read_excel(dataXL)

    sns.set(rc=mplPars, style="darkgrid")
    fig, ax = plt.subplots(figsize=(7, 5.6))
    tmp1 = dataDF.groupby(["Labor State", "Bin Center $(\mu m)$", "initRefs"])
    averagePDLWithinIR = tmp1["Percentage Dendritic Length"].mean().reset_index()
    sns.pointplot(data=averagePDLWithinIR, x="Bin Center $(\mu m)$", y="Percentage Dendritic Length", hue="Labor State",
                  ax=ax, hue_order=["Newly Emerged", "Forager"], palette=['r', 'b'], dodge=True,
                  ci=None, size=20)
    sns.stripplot(data=averagePDLWithinIR, x="Bin Center $(\mu m)$", y="Percentage Dendritic Length",
                  hue="Labor State", ax=ax, hue_order=["Newly Emerged", "Forager"], palette=["w", "w"], dodge=True)
    sns.stripplot(data=averagePDLWithinIR, x="Bin Center $(\mu m)$", y="Percentage Dendritic Length",
                  hue="Labor State", ax=ax, hue_order=["Newly Emerged", "Forager"], palette=['r', 'b'], dodge=True,
                  marker=openCircleMarker, linewidth=0.001)

    allMaxVal = dataDF["Percentage Dendritic Length"].max()

    signifsForInitRefs = pd.DataFrame()

    for binInd, (binCenter, bcDF) in enumerate(dataDF.groupby("Bin Center $(\mu m)$")):

        for initRefInd, (initRef, initRefDF) in enumerate(bcDF.groupby("initRefs")):
            currentIRSigs = dfInterHueFunc(initRefDF, hue="Labor State", pars=["Percentage Dendritic Length"],
                           func=lambda x, y: ttest_ind(x, y, equal_var=False), outLabels=["T-Stat", "P-Value"])
            currentIRSigs["Bin Center $(\mu m)$"] = binCenter
            currentIRSigs["initRefs"] = initRef
            signifsForInitRefs = signifsForInitRefs.append(currentIRSigs, ignore_index=True)

    signifsForInitRefs["P-Value Significant?"] = signifsForInitRefs["P-Value"] < 0.05
    withinIRSigsCount = signifsForInitRefs.groupby("Bin Center $(\mu m)$")["P-Value Significant?"].sum()


    for binInd, (binCenter, bcDF) in enumerate(averagePDLWithinIR.groupby("Bin Center $(\mu m)$")):

        allForagerData = bcDF.loc[lambda x: x["Labor State"] == "Forager", :]
        foragerData = allForagerData["Percentage Dendritic Length"]
        allNEData = bcDF.loc[lambda x: x["Labor State"] == "Newly Emerged", :]
        neData = allNEData["Percentage Dendritic Length"]


        tVal, pVal = ttest_ind(foragerData, neData, equal_var=False)
        # df = getWelchDF(foragerData, neData, len(allForagerData["Experiment ID"].unique()),
        #                 len(allNEData["Experiment ID"].unique()))
        # pVal = getPValFromTStatAndDF(tVal, df)
        pColor = 'k'
        if pVal < 0.05:
            pColor = "g"

        fMean, fStd = foragerData.mean(), foragerData.std()
        neMean, neStd = neData.mean(), neData.std()

        maxVal = max(fMean + fStd, neMean + neStd)


        if not np.isnan(pVal):
            ax.text(binInd, maxVal + 0.4 * abs(allMaxVal),
                    "{:1.1e}({:d})".format(pVal, int(withinIRSigsCount[binCenter])),
                     fontdict={'color': pColor}, fontsize=plt.rcParams['xtick.labelsize'], rotation=90,
                     horizontalalignment='center', verticalalignment='center')

    l1, = ax.plot((), (), 'r-o', label="Newly Emerged")
    l2, = ax.plot((), (), 'b-o', label="Forager")

    ax.grid(True)

    ax.set_ylim(-1, 40)
    ax.set_xlim(-2, binCenters.shape[0] + 2)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.legend(handles=[l1, l2], loc="upper center", ncol=2)
    ax.set_xlabel("Shell Radius ($\mu m$)")
    fig.tight_layout()
    fig.savefig(outFig, dpi=300)
    return fig


if __name__ == "__main__":

    assert len(sys.argv) == 4, "Improper Usage! Please use as on the following:\n" \
                               "python {currFile} saveData <input XL File> <output XL File> or \n" \
                               "python {currFile} plotData <data XL File> <output PNG File>".format(
        currFile=sys.argv[0])

    if sys.argv[1] == "saveData":
        saveData(*sys.argv[2:])
    elif sys.argv[1] == "plotData":
        plotData(*sys.argv[2:])










