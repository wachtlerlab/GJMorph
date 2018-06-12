import pandas as pd
from matplotlib import pyplot as plt
from GJMorph.matplotlibRCParams import mplPars
from regmaxsn.core.occupancyBasedMeasure import occupancyEMD
import sys
import seaborn as sns
import os

expNames = {
    "Forager": [
                'HB130313-4',
                'HB130322-1',
                'HB130326-2',
                'HB130408-1',
                'HB130425-1',
                'HB130501-2',
                'HB130705-1',
                'HB140424-1',
            ],
    "Newly Emerged": [
                'HB130523-3',
                'HB130605-1',
                'HB130605-2',
                'HB140813-3',
                'HB140917-1',
                'HB140930-1',
                'HB141030-1',
            ]
            }


def saveRegErrVsDiffSVS(inFile, outFile):

    inDF = pd.read_excel(inFile)

    for ind, (laborState, svs, initRef, resDir) in inDF.iterrows():

        expNamesLS = expNames[laborState]
        swcFilesLS = [os.path.join(resDir, x + ".swc") for x in expNamesLS]
        print("Doing SVS={} for {} with {} as initial reference".format(svs, laborState, initRef))
        inDF.loc[ind, "Registration Error"] = occupancyEMD(swcFilesLS, svs)

    inDF.to_excel(outFile)


def plotRegErrVsDiffSVS(dataFile):

    df = pd.read_excel(dataFile)
    plt.ion()

    sns.set(rc=mplPars, style="darkgrid")
    fig, ax = plt.subplots(figsize=(7, 5.6))
    sns.swarmplot(ax=ax, x="Smallest Voxel Size", y="Registration Error", hue="Labor State", data=df)
    fig.tight_layout()
    raw_input("Press any key to continue...")


if __name__ == "__main__":

    if len(sys.argv) == 4 and sys.argv[1] == "saveData":
        inFile = sys.argv[2]
        outFile = sys.argv[3]
        saveRegErrVsDiffSVS(inFile, outFile)

    elif len(sys.argv) == 3 and sys.argv[1] == "plotData":
        dataFile = sys.argv[2]
        plotRegErrVsDiffSVS(dataFile)

    else:
        assert False, "Improper usage! Please use as:\n " \
                      "python {a} saveData <inFile> <outFile> or\n " \
                      "python {a} plotData <data file>".format(a=sys.argv[0])

