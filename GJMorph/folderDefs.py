'''
Contains the definitions of several important paths for data input and output. Also contains a couple of convenience
functions
'''

import os

'''
A folder to store all data. All input data, intermediate processed data and output data will be collected here.
(SMR files containing raw electrophysiological traces need to be manually placed in "spike2Path" below)
'''
homeFolder = "/home/aj/"

'''
Path to the excel file containing all metadata
'''
excel = os.path.join(homeFolder, 'DataAndResults/Ginjang-Metadata/neuron_database.xlsx')

'''
Name of the sheet of "excel" containing metadata of all experiments
'''
excelSheet = 'Kai-san final report150803'

'''
Spec File for calculating scalar morphometrics. Needs to have five columns exactly in the following order:
1. Measure: strings, A label for the maesure
2. Divisor: floats, The calculated measure will be divided by this number. It's an option for normalization
3. Units: strings, units of the measures
4. Program: strings, The program to use for calculating the measure. Currently "btmorph2" and "vaa3d" are supported.
5. MeasureName: strings, name of the function in the program for calculating the measure. 

NOTE: An example is provided in the source repo on github at GJMorph/etc/DL-Int-1_globalMeasuresSpec.xlsx
'''
specFile = os.path.join(homeFolder, "DataAndResults", "morphology", "DL-Int-1Results", "ScalarParameters",
                        "DL-Int-1_globalMeasuresSpec.xlsx")