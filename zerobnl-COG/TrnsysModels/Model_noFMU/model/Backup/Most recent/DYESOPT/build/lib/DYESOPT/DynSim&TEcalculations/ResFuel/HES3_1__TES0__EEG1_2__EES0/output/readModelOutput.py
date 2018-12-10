import os
import numpy as np


#paths to TRNSYS output files#
powerFile = os.path.join('C:\DYESOPT\DYESOPT\DynSim&TEcalculations','ResFuel', 'HES3_1__TES0__EEG1_2__EES0', 'model', 'Power.txt')

#read data from output files# (Columns are stated because the number of columns is confusing due to the shift in the title bar)--> Osama
powerData = np.loadtxt(powerFile, comments='#', delimiter='\t', converters=None, skiprows=1, usecols=(0,1,2,3,4,5,6,7,8,9,10,11), unpack=False, ndmin=0)

#extract field power values#
result_plant_P_HPT       = np.maximum(0, powerData[:,1])
result_plant_P_LPT       = np.maximum(0, powerData[:,2])
result_plant_PARS_1      = np.maximum(0, powerData[:,3])
result_plant_PARS_2      = np.maximum(0, powerData[:,4])
result_plant_PARS_3      = np.maximum(0, powerData[:,5])
result_plant_EpNet       = np.maximum(0, powerData[:,6])
result_plant_EpGross     = np.maximum(0, powerData[:,7])
result_plant_FUEL        = np.maximum(0, powerData[:,11])
result_plant_Eparas      = result_plant_PARS_1 + result_plant_PARS_2 + result_plant_PARS_3

result_success = 1
