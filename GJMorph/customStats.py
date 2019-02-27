import numpy as np
import pandas as pd
from rpy2 import robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects import packages as rpackages
from rpy2.rinterface import RRuntimeError
pandas2ri.activate()

def getWelchDF(var1, var2, N1, N2, df1, df2):
    """
    Calculate degree of freedom according to Welch-Satterthwaite equation.
    https://en.wikipedia.org/wiki/Welch's_t-test
    :param var1: float, variance of set1
    :param var2: float, variance of set2
    :param N1: float, size of set 1
    :param N2: float, size of set 2
    :param df1: degree of freedom of set1
    :param df2: degree of freedom of set2
    :return: int, calculated degrees of freedom
    """


    tmp1, tmp2 = var1 / N1, var2 / N2

    df = ((tmp1 + tmp2) ** 2) / (tmp1 ** 2 / (df1 - 1) + tmp2 ** 2 / (df2 - 1))

    if np.isnan(df):
        return df
    else:
        return int(round(df))

# shamelessly stolen from https://github.com/scipy/scipy/pull/4933#issuecomment-292314817
def r_mannwhitneyu(sample1, sample2, exact=True, alternative="two.sided"):
    sample1 = "c({})".format(str(list(sample1))[1:-1])
    sample2 = "c({})".format(str(list(sample2))[1:-1])
    robjects.R()("""wres <- wilcox.test({}, {}, alternative="{}"{});
                       rm(sample1);
                       rm(sample2);""".format(sample1, sample2, alternative,
                                              ", exact=TRUE" if exact else ""))
    wres = robjects.r['wres']
    uval = wres[0][0]
    pval = wres[2][0]
    return uval, pval

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


def art_two_way_anova(dataDF):
    """
    Performs Aligned rank transform of the data followed by two-way Anova.
    Ref: Wobbrock, J.O., Findlater, L., Gergle, D. and Higgins, J.J. (2011).
    "The Aligned Rank Transform for nonparametric factorial analyses using only ANOVA procedures."
    Proceedings of the ACM Conference on Human Factors in Computing Systems (CHI '11). doi: 10.1145/1978942.1978963
    :param dataDF: pandas.DataFrame with the following column ordering:
                      Column 1. Factor 1
                      Column 2. Factor 2
                      Column 3. Measurements
    :return: correctness_ART, pVal_tuple
             correctness_ART: bool, correctness of ART procedure (see section "Ensuring Correctness" of the reference
                              paper)
             pVal_tuple: tuple, has three members -- pVal for effect of Factor 1, pVal for effect of Factor 2,
                         pVal for the interaction effect between Factor 1 and Factor 2.

    """

    assert type(dataDF) is pd.DataFrame, "Input <dataDF> is not a pandas DataFrame as expected"
    assert type(dataDF.shape[1] == 3), "The number of columns in <dataDF> is not 4 as expected"

    ART_IPDF_r = robjects.DataFrame({"f1": robjects.FactorVector(dataDF.iloc[:, 0]),
                                   "f2": robjects.FactorVector(dataDF.iloc[:, 1]),
                                   "m": robjects.FloatVector(dataDF.iloc[:, 2])})

    rUtils = rpackages.importr("utils")
    rUtils.chooseCRANmirror(ind=1)

    try:
        rpackages.importr("ARTool")
    except RRuntimeError as re:
        if str(re).find("Error in loadNamespace") >= 0:
            print("Insatalling package \"ARTool\" in the embedded R. This might take a while")
            rUtils.install_packages(robjects.StrVector(["ARTool"]))
            rpackages.importr("ARTool")
        else:
            raise re

    ARTFunc_r = robjects.r["art"]

    modelFormula = robjects.Formula("m~f1*f2")
    ART_OPDF = ARTFunc_r(modelFormula, data=ART_IPDF_r)
    rsummary = robjects.r["summary"]

    try:
        ART_OP_SUM = rsummary(ART_OPDF)
    except RRuntimeError as re:
        if str(re).find("Error in Anova.lm") >= 0:
            return 1, (np.nan, np.nan, np.nan)
        else:
            raise(re)

    columnSums = np.array(ART_OP_SUM[10])
    fVal_aligned_anova = np.array(ART_OP_SUM[11][4])

    ART_success = np.allclose(columnSums, 0) and np.allclose(fVal_aligned_anova, 0)

    ranova = robjects.r("anova")
    ART_res = ranova(ART_OPDF)

    return ART_success, tuple(ART_res[6])

#***********************************************************************************************************************

def HodgesLehmannEstimate(x, y):
    """
    Calculates the Hodges-Lehmann estimate of the difference between medians of two populations x, y. The output is to
    be interpreted as "x-y". It constructs all possible sets of two elements where one element is from x and one from y,
    and calculates differences between the elements for all sets, and calculates the median of the resulting differences.
    bewteen
    :param x: iterable of float
    :param y: iterable of float
    :return: float, h-l estimate
    """

    return np.median([(a - b) for a in x for b in y])

#***********************************************************************************************************************








