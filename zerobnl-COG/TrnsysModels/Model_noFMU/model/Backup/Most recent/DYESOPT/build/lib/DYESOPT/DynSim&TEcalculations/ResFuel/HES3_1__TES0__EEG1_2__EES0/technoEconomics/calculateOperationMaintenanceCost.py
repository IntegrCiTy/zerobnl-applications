import importlib

from DesignParameters.HES3_1_Def_Par import *
from DesignParameters.ECON_Def_Par import *
from CostFunctions.CHP_CAPEX import *
CompPower = importlib.import_module('DynSim&TEcalculations.ResFuel.HES3_1__TES0__EEG1_2__EES0.output.calculateComponentPower')

# O&M costs are already considered in OPEX
#NonFuel_O&M = 0.033 $/kWh;

result_cost_OPEXtot = CompPower.result_plant_FUEL_tot*Fuel_Cost+0.035*CompPower.result_plant_Etot*1000

