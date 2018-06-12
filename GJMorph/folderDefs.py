'''
Contains the definitions of several important paths for data input and output. Also contains a couple of convenience
functions
'''

import os
from GJEphys.KKHAXLParsing import parseMetaDataFile, getExpIDsByCategory

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

specFile = os.path.join(homeFolder, "DataAndResults", "morphology", "DL-Int-1Results", "ScalarParameters",
                        "DL-Int-1_globalMeasuresSpec")