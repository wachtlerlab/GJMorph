import pandas as pd
import sys
from scipy.stats import ttest_ind
from GJMorph.pandasFuncs import dfInterHueFunc
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from GJMorph.matplotlibRCParams import mplPars
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm


if __name__ == '__main__':

    assert len(sys.argv) == 3, 'Improper usage! Please use as \'python filterSignificantVoxels.py ' \
                               '<dataXL> <outputBase>\''

    dataXL = sys.argv[1]
    outBase = sys.argv[2]

    columnTempNames = {"voxel center": "vc",
                       "neurite length": "nl",
                       "set name": "ls"}

    dataDF = pd.read_excel(dataXL, index_col=0)
    # unstacking is required to fill up the sparse data with zeros
    indexedDF = dataDF.set_index(keys=["voxel size", 'voxel center', 'set name', 'expID', "initRefs"])
    pivotedDF = indexedDF.unstack(level=('set name', "initRefs", 'expID'), fill_value=0)
    dataFullDF = pivotedDF.stack(level=('set name', "initRefs", "expID")).reset_index()
    dataDFR = dataFullDF.rename(columns=columnTempNames)

    formula = "nl~C(ls) + C(initRefs) + C(ls):C(initRefs)"
    statsDF = pd.DataFrame()

    totalVCs = dataDFR["vc"].unique().shape[0]
    for vcInd, (vc, vcDF) in enumerate(dataDFR.groupby("vc")):
        print("Doing {}, Number {}/{}".format(vc, vcInd + 1, totalVCs))
        model = ols(formula, vcDF).fit()
        aov_table = anova_lm(model, typ=2)
        toAppend = aov_table["PR(>F)"][:3]
        toAppend["voxel center"] = vc
        toAppend["F(ls)"] = aov_table.loc["C(ls)", "F"]
        toAppend["voxel size"] = vcDF["voxel size"].iloc[0]
        temp = vcDF.set_index("ls")
        toAppend["Difference of Means"] = temp.loc["Forager", "nl"].mean() - temp.loc["Newly Emerged", "nl"].mean()
        statsDF = statsDF.append(toAppend, ignore_index=True)

    alpha = 0.05
    boniferriCorrectedAlpha = alpha / statsDF.shape[0]

    sigDifFunc = lambda x: (x["C(ls):C(initRefs)"] > alpha) and \
                           (x["C(ls)"] < boniferriCorrectedAlpha) and (x["C(initRefs)"] > alpha)
    statsDF["Significant Difference"] = statsDF.apply(sigDifFunc, axis=1)
    statsDF.to_excel("{}.xlsx".format(outBase))


