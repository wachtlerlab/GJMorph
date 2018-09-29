"""
Description:         This file contains functions for saving scalar morphometric and topological measures of forager and
                     newly emerged neuron morphologies stored in SWC files and performing statistical tests on them.
Usage:               1. Specify SWCs using the variables "foragerSWCPath" and "newlyEmergedSWCPath" in the script
                     for directories containing the morphologies and the variables "foragerNrns" and "newlyEmergedNrns"
                     for and the names of SWC files.
                     2. Execute the python script without arguments to get a list of usages. Each usage is
                     associated with function and calls it. See documentation of functions for more info.

Note:                This script implicitly uses a specification file, with it's path stored in
                     GJMorph.folderDefs.specFile. It is an excel file with the columns "Measure", "Divisor", "Units",
                     "Program" and "MeasureName". It specifies a list of measures names to use as well as its units,
                     divisor to divide the value of the measure if required, the program to use to calculate the \
                     measure and the name of the measure in that program.
"""

import os
import numpy as np
from scipy.stats import ttest_ind, f_oneway, kruskal
from pylatex import Document, Tabular, Command, Math, Package
from pylatex.utils import NoEscape, bold
from GJMorph.folderDefs import homeFolder, specFile
from btmorph2.globalFeatures import getGlobalFeautures as getGlobalFeaturesBTM
from pyVaa3d.global_neuron_features import getGlobalNeuronFeatures as getGlobalFeaturesVaa3d
import pandas as pd
import sys
import logging
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from matplotlib import pyplot as plt
import seaborn as sns
from GJMorph.matplotlibRCParams import mplPars, getLighterColor
from scipy.spatial import ConvexHull
from matplotlib.patches import Polygon
import warnings
warnings.filterwarnings(action='once')



def bootstrapWelsch_ttest(vals1, vals2, nBootstrap=1000):

    """
    Calculates the pVal of difference of means of vals1 and vals2 using the Welsch t-test.
    It uses bootstrap sampling to determine the distribution of the Welsch t-statistic.

    Refs:
    1. http://www.biostat.umn.edu/%7Ewill/6470stuff/Class21-12/Handout21.pdf
    2. https://en.wikipedia.org/wiki/Welch%27s_t-test

    :param vals1: iterable
    :param vals2: iterable
    :param nBootstrap: number of bootstraps to use
    :return: tStat, pVal : float, float
    """

    try:
        vals1 = np.array(vals1)
    except Exception as e:
        raise(ValueError('vals1 must be an iterable of numbers'))

    try:
        vals2 = np.array(vals2)
    except Exception as e:
        raise (ValueError('vals2 must be an iterable of numbers'))

    N1 = len(vals1)
    N2 = len(vals2)

    vals1Mean = vals1.mean()
    vals2Mean = vals2.mean()

    observedTStat = (vals1Mean - vals2Mean) / np.sqrt((np.var(vals1) / N1) + (np.var(vals2) / N2))

    vals10Mean = vals1 - vals1Mean
    vals20Mean = vals2 - vals2Mean

    bootstrapSamples1 = np.random.choice(vals10Mean, size=(nBootstrap, N1))
    bootstrapSamples2 = np.random.choice(vals20Mean, size=(nBootstrap, N2))

    BSSampleMeans1 = bootstrapSamples1.mean(axis=1)
    BSSampleMeans2 = bootstrapSamples2.mean(axis=1)

    BSSampleVar1 = bootstrapSamples1.var(axis=1)
    BSSampleVar2 = bootstrapSamples1.var(axis=1)

    temp1 = (BSSampleVar1 / N1)
    temp2 = (BSSampleVar2 / N2)

    tStats = (BSSampleMeans1 - BSSampleMeans2) / np.sqrt(temp1 + temp2)

    pVal = (np.abs(tStats) >= np.abs(observedTStat)).sum() / float(nBootstrap)

    return observedTStat, pVal


# ----------------------------------------------------------------------------------------------------------------------
# foragerSWCPath = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1')
foragerSWCPath = os.path.join("/home/aj/ownCloud/GinJang_data/GinJang_ProcessedData/Hide/2016NewSegmentation")
foragerNrns = [
    'HB130313-4',
    'HB130322-1',
    'HB130326-2',
    # 'HB130408-1',
    'HB130425-1',
    # 'HB130501-2',
    'HB130705-1',
    'HB140424-1',
]

# ----------------------------------------------------------------------------------------------------------------------

# newlyEmergedSWCPath = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'OriginalData', 'DL-Int-1')
newlyEmergedSWCPath = os.path.join("/home/aj/ownCloud/GinJang_data/GinJang_ProcessedData/Hide/2016NewSegmentation")

newlyEmergedNrns = [
                'HB130523-3',
                'HB130605-1',
                'HB130605-2',
                'HB140813-3',
                'HB140917-1',
                'HB140930-1',
                # 'HB141030-1',
                    ]
# ----------------------------------------------------------------------------------------------------------------------
# composeFN = lambda x, y, part: os.path.join(y, x, x + part + '.swc')
composeFN = lambda x, y, part: os.path.join(y, x, '{}-{}C10S10.swc'.format(x, part))
# ----------------------------------------------------------------------------------------------------------------------


def saveData(outFile, part):
    """
    Calculates and saves the measures in an excel file
    :param outFile: string, where the output excel file is to be written
    :param part: string, one of ['WN', 'MB', 'VB', 'DB']
    :return:
    """
    foragerSWCs = [composeFN(x, foragerSWCPath, part) for x in foragerNrns]
    newlyEmergedSWCs = [composeFN(x, newlyEmergedSWCPath, part) for x in newlyEmergedNrns]
    allSWCs = foragerSWCs + newlyEmergedSWCs
    laborStates = ["Forager"] * len(foragerSWCs) + ["Newly Emerged"] * len(newlyEmergedSWCs)

    btmorphGlobalFeatures = getGlobalFeaturesBTM(allSWCs)
    vaa3dGlobalFeatures = getGlobalFeaturesVaa3d(allSWCs)

    specsDF = pd.read_excel(specFile, index_col=0, header=0)

    allData = pd.DataFrame()

    programMap = {"btmorph2": btmorphGlobalFeatures,
                  "vaa3d": vaa3dGlobalFeatures}

    for swc, laborState in zip(allSWCs, laborStates):
        tempS = pd.Series()
        tempS["SWC File"] = swc
        tempS["Labor State"] = laborState
        for measureName, (divisor, UnitStr, program, programMeasure) in specsDF.iterrows():
            if pd.isnull(UnitStr):
                measureNameWithUnits = measureName
            else:
                measureNameWithUnits = "{} (\({}\))".format(measureName, UnitStr)

            if programMeasure in programMap[program].columns:
                measureValue = programMap[program].loc[swc, programMeasure]
                tempS[measureNameWithUnits] = measureValue / float(divisor)
            else:
                tempS[measureNameWithUnits] = np.nan
                logging.warning("For SWC {}, Measure {} was not found in the output of program {}".format(
                    swc, programMeasure, program))
        allData = allData.append(tempS, ignore_index=True)

    allData.set_index(["Labor State", "SWC File"], inplace=True)

    allData.to_excel(outFile)


def saveStats(inFile, outFile_prefix):
    """
    Runs statistical tests to check if the values are statistically different, format results in a table in pdf format
    :param inFile: string, path of an excel file generated by the function "saveData" above
    :param outFile_prefix: string, output pdf will be saved as "<outFile_prefix>.pdf". The calculated stats are also
    saved as "<outFile_prefix>.xlsx".
    :return:
    """
    allData = pd.read_excel(inFile, index_col=(0, 1), header=0)
    allData.reset_index(inplace=True)
    statsData = pd.DataFrame()

    doc = Document("{}_table".format(outFile_prefix))
    doc.packages.append(Package('geometry', options=['paperwidth=160mm',
                                                     'paperheight=205mm',
                                                     'top=2mm', 'left=1mm']))
    doc.packages.append(Package('xcolor'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('cmbright'))
    doc.packages.append(Package('fontenc', options=['T1']))
    doc.append(Command('pagenumbering', 'gobble'))
    doc.append(Command(command='renewcommand', arguments=[NoEscape(r'\arraystretch'), 2]))
    table1 = Tabular('|c|c|c|c|')
    table1.add_hline()
    table1.add_row(map(bold, ['Measure', 'Newly emerged', 'Forager', 'pVal']))
    table1.add_hline()
    table1.add_hline()

    specsDF = pd.read_excel(specFile, index_col=0, header=0)
    for measureName, (divisor, UnitStr, program, programMeasure) in specsDF.iterrows():

        if pd.isnull(UnitStr):
            measure = measureName
        else:
            measure = "{} (\({}\))".format(measureName, UnitStr)

        measureS = pd.Series()
        measureS["Measure"] = measure

        fMeasures = allData.loc[lambda df:df["Labor State"] == "Forager", measure].values
        nMeasures = allData.loc[lambda df:df["Labor State"] == "Newly Emerged", measure].values

        fMean = np.mean(fMeasures)
        nMean = np.mean(nMeasures)
        fStd = np.std(fMeasures)
        nStd = np.std(nMeasures)

        if np.isnan(fMean) or np.isnan(nMean):
            pVal = float("nan")
        else:
            # tstat, pVal = bootstrapWelsch_ttest(fMeasures, nMeasures, 1000)
            # print('Bootstrap', tstat, pVal)
            tstat1, pVal = ttest_ind(fMeasures, nMeasures, equal_var=False)
            # print('Welsch T-Test', tstat1, pVal1)

        measureS["P-Value"] = pVal
        measureS["Forager Mean"] = fMean
        measureS["Newly Emerged Mean"] = nMean
        measureS["Forager S.D."] = fStd
        measureS["Newly Emerged S.D."] = nStd

        statsData = statsData.append(measureS, ignore_index=True)

        pm = '\pm'
        pValStr = str(round(pVal, 4))

        [fMean, fStd, nMean, nStd] = ["{:.3g}".format(x) for x in [fMean, fStd, nMean, nStd]]

        if pVal <= 0.05:
            [fMean, fStd, nMean, nStd, pm, measure, pValStr] = \
            map(lambda x: r'\color{red}{' + x + '}',
                    [fMean, fStd, nMean, nStd, pm, measure, pValStr])

        measureEntry = Math(data=[NoEscape(r'\text{' + measure + '}')],
                            inline=True)

        if np.isnan(pVal):
            fEntry = "N/A"
            nEntry = "N/A"
            pValEntry = "N/A"
        else:
            fEntry = Math(data=[NoEscape(fMean), NoEscape(pm), NoEscape(fStd)], inline=True)
            nEntry = Math(data=[NoEscape(nMean), NoEscape(pm), NoEscape(nStd)], inline=True)
            pValEntry = Math(data=[NoEscape(pValStr)], inline=True)

        tableEntry = [measureEntry, nEntry, fEntry, pValEntry]
        table1.add_row(tableEntry)
        table1.add_hline()

    statsData.to_excel("{}.xlsx".format(outFile_prefix))

    doc.append(table1)
    doc.generate_pdf()


def savePCAProjections(dataXL, outBase):
    """
    #TODO
    :param inFile: string, path of an excel file generated by the function "saveData" above
    :param outFile_prefix: string, output pdf will be saved as "<outFile_prefix>.pdf". The calculated stats are also
    saved as "<outFile_prefix>.xlsx".
    :return:
    """

    dataDF = pd.read_excel(dataXL, header=0, index_col=(0, 1)).reset_index()

    colMap = {"Forager": [0, 0, 1], "Newly Emerged": [1, 0, 0]}

    featuresOnlyDF = dataDF.dropna("columns").drop(["Labor State", "SWC File"], axis=1)
    featureMatrix = featuresOnlyDF.values
    featuresPCA = PCA(n_components=2, whiten=True)
    featuresProjected2D = featuresPCA.fit_transform(featureMatrix)

    pcaProjectionsDF = pd.DataFrame()
    pcaProjectionsDF["Labor State"] = dataDF["Labor State"]
    pcaProjectionsDF["SWC File"] = dataDF["SWC File"]
    pcaProjectionsDF["PCA1"] = featuresProjected2D[:, 0]
    pcaProjectionsDF["PCA2"] = featuresProjected2D[:, 1]
    print("Fraction of variances Explained: {}".format(featuresPCA.explained_variance_ratio_))

    pcaProjectionsDF.to_excel("{}.xlsx".format(outBase))

    sns.set(style="darkgrid")
    fig2, ax2 = plt.subplots(figsize=(7, 5.6))
    featureNames = featuresOnlyDF.columns
    pcaComponentsDF = pd.DataFrame(columns=pd.Index(data=featureNames, name="Feature Name"),
                                   index=pd.Index(name='Component Number', data=[1, 2]))
    pcaComponentsDF.loc[[1, 2], :] = featuresPCA.components_
    pcaComponentsDFStacked = pcaComponentsDF.stack().reset_index()
    pcaComponentsDFStacked.rename(columns={0: "Feature Value"}, inplace=True)
    sns.barplot(data=pcaComponentsDFStacked, x="Feature Value", y="Feature Name", hue="Component Number", ax=ax2)
    ax2.set_ylabel("")
    fig2.tight_layout()
    fig2.savefig("{}_PCAcomponents.png".format(outBase), dpi=300)


    sns.set(rc=mplPars, style="white")
    fig1, ax1 = plt.subplots(figsize=(7, 5.6))

    for ls, lsDF in pcaProjectionsDF.groupby("Labor State"):
        lsPCAProjections = lsDF.drop(["Labor State", "SWC File"], axis=1).values
        convexHull = ConvexHull(lsPCAProjections)

        polygon = Polygon(lsPCAProjections[convexHull.vertices], facecolor=colMap[ls], fill=True,
                          edgecolor=None, alpha=0.4)
        ax1.add_patch(polygon)
        ax1.plot(lsPCAProjections[:, 0], lsPCAProjections[:, 1], color=colMap[ls], marker='o', ls="None")

    ax1.set_xlabel("PCA$_1$")
    ax1.set_ylabel("PCA$_2$")

    fig1.tight_layout()
    fig1.savefig("{}_PCAProjections.png".format(outBase), dpi=300)


if __name__ == "__main__":

    assert len(sys.argv) == 4, "Improper Usage! Please use as:\n" \
                               "python {a} saveData <outFile> <part Suffix> or \n"  \
                               "python {a} saveStats <dataFile> <outFile Prefix> or \n" \
                               "python {a} plotPCA <dataFile> <outFile Prefix>".format(a=sys.argv[0])

    if sys.argv[1] == "saveData":
        saveData(sys.argv[2], sys.argv[3])

    elif sys.argv[1] == "saveStats":
        saveStats(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "plotPCA":
        savePCAProjections(*sys.argv [2:])
    else:
        print("Improper option! Please use as:\n"
              "python {a} saveData <outFile> <part Suffix> or \n"
              "python {a} saveStats <inFile> <outFile Prefix> or \n" 
              "python {a} plotPCA <dataFile> <outFile Prefix>".format(a=sys.argv[0]))





