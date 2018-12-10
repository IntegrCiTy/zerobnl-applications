import DYESOPT
import importlib
from Core.setModelLabel import *
from Core.setDefaultParameters import *
from model_Choice import *
EEG_DP_module= importlib.import_module('DesignParameters.'+EEGname+'_Def_Par')
HES_DP_module= importlib.import_module('DesignParameters.'+HESname+'_Def_Par')


#basic model properties#
TRNSYS_data_dtSim =    model_dt
TRNSYS_data_dtSim = round((TRNSYS_data_dtSim / 3600)*100)/100  ##Osama--> rounding function brings 12.5 to 12 instead of 13, i.e not necessarily to the higher integer, that's a python thing


if DYESOPT.runMode == 'single':
    TRNSYS_data_pltMode =  0

else:
    TRNSYS_data_pltMode =  -1

#store simlation duration#
TRNSYS_data_hrSim = model_hrSim

