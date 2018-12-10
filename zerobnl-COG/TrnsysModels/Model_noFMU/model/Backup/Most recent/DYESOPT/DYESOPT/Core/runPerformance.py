import importlib
from Core.setModelLabel import *
from model_Choice import *
EEG_DP_module= importlib.import_module('DesignParameters.'+EEGname+'_Def_Par')
HES_DP_module= importlib.import_module('DesignParameters.'+HESname+'_Def_Par')
import DYESOPT

# Here the annual dynamic simulation of the plant performance is run.


# Inform of current operation.

if DYESOPT.runMode=='single':
    print('>> ', HES_DP_module.model_tool.upper(), ': Loading ', model_plant, ' model...')

# Inform of current operation.
if DYESOPT.runMode=='single':
    print('>>  TRNSYS : Preparing input data... ')

# Executing the relevant runMainModel file
importlib.import_module('DynSim&TEcalculations.' + HESTech + '.' + model_plant + '.input.runMainModel' )

