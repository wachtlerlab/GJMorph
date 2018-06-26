'''
This file contains a list of parameters used for co-registering two set of co-registered morphologies. Reg-MaxS is
internally used for co-registering "average" (i.e. Union) representations of the morphologies in each set.
Each morphology of the test set is transformed using the same transformation that was used to co-register the test
average.

This list is used to for a json dictionary of parameters.

resDir: string,  path into which the results of co-registering co-registered morphologies will be written.

refSWCList: list of strings, each string is the path of SWCs in the reference set, which is the set that will not be
transformed.

testSWCList: list of strings, each string is the path of an SWC in the test set, which is the set that will be
transformed to be colocated with the reference set.

usePartsDir: boolean. If True, then the procedure checks if for every SWC in swcList, a folder exists with the
                        same name and path without the '.swc' extention. If such folders exist, the SWCs in them are
                        transformed exactly the same as their corresponding SWCs and written into folders with the same
                        names in resDir.

Rest of the parameters are the same as for Reg-MaxS (see regmaxs.core.RegMaxSPars)
'''

Reg2RegParNames = [
                    'resDir',
                    'refSWCList', 'testSWCList',
                    'usePartsDir',
                    'gridSizes',
                    'rotBounds', 'transBounds', 'scaleBounds',
                    'rotMinRes', 'transMinRes', 'minScaleStepSize',
                    'nCPU',
                    ]