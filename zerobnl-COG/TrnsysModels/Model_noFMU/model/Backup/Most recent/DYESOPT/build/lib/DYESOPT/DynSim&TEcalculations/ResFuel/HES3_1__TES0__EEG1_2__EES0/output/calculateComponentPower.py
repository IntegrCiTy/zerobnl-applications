import importlib
import math
import numpy as np

from DesignParameters.EEG1_2_Def_Par import *
from DesignParameters.HES3_1_Def_Par import *
from PPSteadyStateDesign.EEG.EEG1_2.PowerBlock import *
import Core.setDefaultParameters as DF

ModelOutput = importlib.import_module('DynSim&TEcalculations.ResFuel.HES3_1__TES0__EEG1_2__EES0.output.readModelOutput')

#Generator Efficiency ---> Ask for explanation as it does not make much sense --- OSAMA
def generatorEfficiency(relPow, nmec, nelec):
    #calculate off-design generator efficiency#
    eff = np.maximum(0, (1 - (1 - nmec)/relPow) * (1 - (1 - nelec)*relPow))
    np.seterr(all='ignore')   #--> To ignore the error when dividing by zero --OSAMA
    return eff

#calculate generator output#
result_plant_EpGen   = ModelOutput.result_plant_EpNet*generatorEfficiency(ModelOutput.result_plant_EpNet/(PC_W/1e3),  math.sqrt(PC_Gen_Eff), math.sqrt(PC_Gen_Eff))
result_plant_EpParas = ModelOutput.result_plant_Eparas*generatorEfficiency(ModelOutput.result_plant_Eparas/(PC_Wparas/1e3),  math.sqrt(PC_Gen_Eff), math.sqrt(PC_Gen_Eff))
result_plant_EpGross = result_plant_EpGen + result_plant_EpParas

result_plant_Etot       = (np.sum(result_plant_EpGen))*(DF.model_dt/3600)  # [MWh]

# Parasitic consumption
result_plant_Epar_tot   = np.sum(result_plant_EpParas)*(DF.model_dt/3600) # [MWh]
# Gross power generation
result_plant_Egross_tot = np.sum(result_plant_EpGross)*(DF.model_dt/3600) # [MWh]
# Fuel needed in boiler
result_plant_FUEL_tot   = (np.sum(ModelOutput.result_plant_FUEL)/1e3)*(DF.model_dt/3600) # [tonne]

result_plant_Epar_P1    = np.sum(ModelOutput.result_plant_PARS_1)*(DF.model_dt/3600)

result_plant_Epar_P2    = np.sum(ModelOutput.result_plant_PARS_2)*(DF.model_dt/3600)

#determine when power plant is online#
result_plant_fLoad= np.zeros(shape=(len(result_plant_EpGen),))
for j in range (1,len(result_plant_EpGen)):
    if result_plant_EpGen[j] == 0:
        result_plant_fLoad[j] = 0
    else:
        result_plant_fLoad[j] = 1

# # checkdispatch vector is a 1-0 vector that is 1 if the time of production
# # corresponded/matched to that which was predefined in the PDS (predifined dispatch strategy)
#
# for j = 1:length(result_plant_fLoad)
#     if result_plant_fLoad(j) == abs(result.econ.signal(j)) && abs(result.econ.signal(j)) == 1;
#         result_plant_checkdispatch(j) = 1;
#     else
#         result_plant_checkdispatch(j) = 0;
#     end
# end
#
# for j = 1:length(result_plant_Qfield)
#     if result_plant_Qfield(j) == 0;
#         result_plant_sfLoad(j) = 0;
#     else
#         result_plant_sfLoad(j) = 1;
#     end
# end
#
# # Predefined dispatch strategy check factors
# result_plant_checkPDS1 = sum(result_plant_checkdispatch)/sum(result_plant_fLoad > 0);# ratio between matched and produced by model
# result_plant_checkPDS2 = sum(result_plant_checkdispatch)/sum(result.econ.signal > 0);# ratio between matched and predefined production
# result_plant_checkPDS3 = sum(result.econ.signal > 0)/sum(result_plant_fLoad > 0);# ratio between predefined and produced
#
# # Annual efficiency values #
# result_plant_EFFth_avg      = sum(result_plant_EFFth)/sum(result_plant_fLoad > 0);
# result_plant_EFFsf_avg      = sum(result_plant_EFFsf)/sum(result_plant_sfLoad > 0);
# result_plant_EFFs2el_avg    = result_plant_EFFth_avg * result_plant_EFFsf_avg * o.rec.EFF * PC_Gen_Eff;
#
# #calculate total operation hours#
# result_plant_NOH = sum(result_plant_fLoad > 0) * (o.model.dt/3600);
#
#
