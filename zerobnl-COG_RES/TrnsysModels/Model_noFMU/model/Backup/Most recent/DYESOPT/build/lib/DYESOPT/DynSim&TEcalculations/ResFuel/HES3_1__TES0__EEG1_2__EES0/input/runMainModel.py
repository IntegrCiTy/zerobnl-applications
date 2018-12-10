# Here an annual dynamic simulation is run. Input data are prepared, the
# plant performance is simulated and the results are collected to be used
# for techno-economic post-process evaluation.

import DYESOPT
import importlib
import numpy as np
from Core.setModelLabel import*
##

# #inform of current operation#
# if strcmpi(model.runMode, 'single');
#     disp('>> TRNSYS: Preparing input data... ');
# end

# #add TRNSYS paths#
# o = addModelPaths(o);

#if single run or first optimisation run#
if DYESOPT.runMode == 'single' or DYESOPT.runMode== 'firstOptim':
    #extract weather data and get simulation duration#
    import Core.Interface.writeWeatherFile
    
else:
    #extract simulation duration from file#
    import Core.Interface.readSimFile

#create structure with standard data#
import Core.Interface.standardTRNSYSdata


#load TRNSYS data and correct units#
### This is to avoid the problem of importing a file including "&" in the name --> Osama
importlib.import_module('DynSim&TEcalculations.ResFuel.HES3_1__TES0__EEG1_2__EES0.input.prepareTRNSYSinput')

# importlib.import_module('DynSim&TEcalculations.ResFuel.HES3_1__TES0__EEG1_2__EES0.adjustTRNSYSunits') ----> removed and merged with standardTRNSYSdata, no need for a separate file

#write TRNSYS input files#
import Core.Interface.writeTRNSYSinput

# To be amended with CSP integration --> OSAMA
# if isfield(o, 'field'):
#     writeFieldMatrix(o);
# end

# To be amended with CSP integration or when required --> OSAMA
# if isfield(model, 'priceFile');
#     write_prfile(o);
# end

#create output structure#
result = np.zeros(shape=(1,1))


if model_plant == 'PV-CSP_baseload':
    ## TO BE AMENDED LATER ON ----> OSAMA
    #Run annual performance of PV model in Matlab
    disp('')
    disp('>> Now launching PV Performance Model in Matlab')
    disp('>> Waiting for PV model to converge... ')
    [o, result] = PVperformance(o)
    disp('')
    [result,o] = write_CSPloadfile(o, result)


#inform of current operation#
if DYESOPT.runMode == 'single':
    print('>>  TRNSYS : Launching TRNEXE with file: ', model_plant, '.dck')
    print(' ')
    print('>>  Waiting for TRNSYS to end... ')


#run TRNSYS model#
import Core.Interface.runTRNSYSmodel
if Core.Interface.runTRNSYSmodel.success == 1:

    #read results of TRNSYS simulation#
    importlib.import_module('DynSim&TEcalculations.ResFuel.HES3_1__TES0__EEG1_2__EES0.output.readModelOutput')



    #calculate model-component powers#
    importlib.import_module('DynSim&TEcalculations.ResFuel.HES3_1__TES0__EEG1_2__EES0.output.calculateComponentPower')
