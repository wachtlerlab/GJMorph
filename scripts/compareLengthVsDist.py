'''
Description:      This file contains functions for saving and plotting the distribution of dendritic length over
                  spherical shells for newly emerged vs forager DL-Int-1s

Usage:            Run the file without any command line arguments to get a list of usages. Each usage calls a function.
                  See the docuementation of individual functions.
'''


import matplotlib as mpl
mpl.use("Agg")
import pandas as pd
from btmorph2 import NeuronMorphology
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from GJMorph.matplotlibRCParams import mplPars, openCircleMarker
import sys
from scipy.stats import ttest_ind
from GJMorph.pandasFuncs import dfInterHueFunc
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm



# ----------------------------------------------------------------------------------------------------------------------
binEdges = np.arange(0, 350, 20)
binWidth = binEdges[1] - binEdges[0]
binCenters = binEdges[:-1] + 0.5 * (binWidth)
# manually entered value of origin. It is the average of the roots of all WN morphologies.
origin = [254.79213333, 119.54293333, 168.7052]
# ----------------------------------------------------------------------------------------------------------------------

def saveData(inXL, dataXL, origin=origin):
    """
    Saves the dendritic length of each DL-Int-1 specified in <inXL> for each of the spatial bins described above. The
    data is stored one spatial bin of one DL-Int-1 per row, with metadata like <Bin Center (um)>,<Experiment ID> and
    <Labor State>
    :param inXL: string, path of an excel file. The excel file should contain three columns with headings
    "Experiment ID", "Labor State", "initRefs" and "swcFile".
    :param dataXL: string, path where the generated data is stored as an excel file.
    :param origin: list of three floats, the origin to use when constructing spherical shells.
    :return:
    """
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
    """
    Legacy function, do not use.
    :param dataXL:
    :param outFig:
    :return:
    """
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

        nForager = allForagerData["Experiment ID"].unique().size
        nNE = allNEData["Experiment ID"].unique().size

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

    l1, = ax.plot((), (), 'r-o', label="Newly Emerged (n={})".format(nForager))
    l2, = ax.plot((), (), 'b-o', label="Forager (n={})".format(nNE))

    ax.grid(True)

    ax.set_ylim(-1, 40)
    ax.set_xlim(-2, binCenters.shape[0] + 2)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.legend(handles=[l1, l2], loc="upper center", ncol=2)
    ax.set_xlabel("Shell Radius ($\mu m$)")
    fig.tight_layout()
    fig.savefig(outFig, dpi=300)
    return fig


def plot2WayAnova(dataXL, outBase):
    """
    Performs two-way ANOVA (http://www.biostathandbook.com/twowayanova.html) to determine whether labor state
    affects dendritic length per shell, whether registration initial reference affects dendritic length per shell and
    whether the two effects are independent. Plots dendritic length per shell averaged over labor state vs shell radius.
    :param dataXL: string, excel file generated by "saveData" function above.
    :param outBase: string, figure will be saved as "<outBase>.png"
    :return:
    """

    dataDF = pd.read_excel(dataXL)

    nForager = dataDF.loc[lambda x: x["Labor State"] == "Forager",
                           "Experiment ID"].unique().size
    nNE = dataDF.loc[lambda x: x["Labor State"] == "Newly Emerged",
                    "Experiment ID"].unique().size
    columnTempNames = {"Bin Center $(\mu m)$":'bin', "Labor State": "ls",
                                     "Percentage Dendritic Length":"pdl"}

    dataDFR = dataDF.rename(columns=columnTempNames)

    formula = "pdl~C(ls) + C(initRefs) + C(ls):C(initRefs)"
    statsDF = pd.DataFrame(columns=["C(ls)", "C(initRefs)", "C(ls):C(initRefs)", "F(ls)"])

    for binInd, (binCenter, bcDF) in enumerate(dataDFR.groupby("bin")):
        model = ols(formula, bcDF).fit()
        aov_table = anova_lm(model, typ=2)
        toAppend = aov_table["PR(>F)"][:3]
        toAppend.name = binCenter
        toAppend["F(ls)"] = aov_table.loc["C(ls)", "F"]
        statsDF = statsDF.append(toAppend)

    alpha = 0.05
    boniferriCorrectedAlpha = alpha / statsDF.shape[0]

    sigDifFunc = lambda x: (x["C(ls):C(initRefs)"] > alpha) and \
                           (x["C(ls)"] < boniferriCorrectedAlpha) and (x["C(initRefs)"] > alpha)
    statsDF["Significant Difference"] = statsDF.apply(sigDifFunc, axis=1)
    statsDF.to_excel("{}.xlsx".format(outBase))

    sns.set(rc=mplPars, style="darkgrid")
    fig, ax = plt.subplots(figsize=(7, 5.6))

    sns.pointplot(data=dataDFR, x="bin", y="pdl", hue="ls", ax=ax, hue_order=["Newly Emerged", "Forager"],
                  palette=['r', 'b'], dodge=True, ci="sd", size=10)
    sigBCs = statsDF.loc[lambda x: x["Significant Difference"], :].index
    sigBCInds = [binCenters.tolist().index(bc) for bc in sigBCs]
    ax.plot(sigBCInds, [-2.5] * len(sigBCInds), "*k", ms=10)

    
    l1, = ax.plot((), (), 'r-o', label="Newly Emerged\n(n={})".format(nForager))
    l2, = ax.plot((), (), 'b-o', label="Forager\n(n={})".format(nNE))

    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_xlabel("Shell Radius $(\mu m)$")
    ax.set_ylabel("Percentage Dendritic Length")
    ax.legend(handles=(l1, l2), loc="upper center", ncol=2)
    ax.set_ylim(-5, 25)
    ax.grid(True)

    fig.tight_layout()
    fig.savefig("{}.png".format(outBase), dpi=300)





if __name__ == "__main__":

    assert len(sys.argv) == 4, "Improper Usage! Please use as on the following:\n" \
                               "python {currFile} saveData <input XL File> <output XL File> or \n" \
                               "python {currFile} plotData <data XL File> <output PNG File> or \n"  \
                               "python {currFile} plot2WayAnova <data XL File> <outBase>".format(
        currFile=sys.argv[0])

    if sys.argv[1] == "saveData":
        saveData(*sys.argv[2:])
    elif sys.argv[1] == "plotData":
        plotData(*sys.argv[2:])
    elif sys.argv[1] == "plot2WayAnova":
        plot2WayAnova(*sys.argv[2:])










