import numpy as np
import math

from CostFunctions.CHP_turboGeneratorSetCost import *
from CostFunctions.CHP_CondenserCost import *
from PPSteadyStateDesign.EEG.EEG1_2.PowerBlock import *
from DesignParameters.EEG1_2_Def_Par import *
from DesignParameters.HES3_1_Def_Par import *


## -------------------------   Direct Costs   --------------------------- #


# Steam turbo generator cost
result_cost_CAPEX_STG_Cost = CHP_turboGeneratorSetCost(PC_W_el,PC_Gen_Eff,'reheat',[PC_W_HPT,PC_W_LPT],PC_TinHPT,1.15,(PC_n_hotPH + PC_n_coldPH + PC_DeaLP + PC_DeaLocatHP),econ_STG_Cost_ref,econ_STG_Size_ref,econ_STG_Scale_ref)

# Condenser and cooling tower

if PC_DoubleCond == 1:
  PC_Area_cond = PC_COND1_Area
  PC_Area_cond_2 = PC_COND2_Area

else:
  PC_Area_cond = PC_COND_Area
  PC_Area_cond_2 = 0

result_cost_CAPEX_Condenser_Cost = CHP_CondenserCost(PC_Heat_demand*1e6, PC_DH_T_supply+5, PC_DH_T_return, PC_DH_T_supply, PC_DH_massflow, econ_Cond_Cost_ref, econ_mf_Cost_ref, econ_Cond_MS_index, 0, 25, PC_Area_cond, PC_Area_cond_2)


#FW preheaters

## Hot Preheaters

UAhotPH= np.zeros(shape = [PC_n_hotPH,])
A_PHhot= np.zeros(shape = [PC_n_hotPH,])

for i in range (0,PC_n_hotPH):
    UAhotPH[i] = PC_hotPH[i,1]
    A_PHhot[i]=UAhotPH[i]/2.2        #m2

A_PHhot_ft2 = A_PHhot * 10.7639      #ft2

Cost_PHhot = math.exp(11.147-0.9186*np.log(A_PHhot_ft2)+0.09790*(np.log(A_PHhot_ft2))**2)*econ_Cond_MS_index     #$

## Cold Preheaters
UAcoldPH= np.zeros(shape = [PC_n_coldPH,])
A_PHcold= np.zeros(shape = [PC_n_coldPH,])

for i in range (0,PC_n_coldPH):
    UAcoldPH[i] = PC_coldPH[i,1]
    A_PHcold[i] = UAcoldPH[i]/2.2          #m2

A_PHcold_ft2 = A_PHcold * 10.7639          #ft2

Cost_PHcold = math.exp(11.147-0.9186*np.log(A_PHcold_ft2)+0.09790*(np.log(A_PHcold_ft2))**2)*econ_Cond_MS_index  #$

result_cost_CAPEX_PH = np.sum(Cost_PHhot)+np.sum(Cost_PHcold)            #$

#Dearators

if PC_DeaLP == 1:
    Cost_DeaLP = 67*(PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+PC_DeaLP)-1,7]*3600)**0.78*econ_Cond_MS_index

Cost_DeaHP = 67*(PC_st[PC_keyst_DEAin_n_st+1-1,7]*3600)**0.78*econ_Cond_MS_index

result_cost_CAPEX_Dea = Cost_DeaLP + Cost_DeaHP

#Pumps

econ_factor_EtaIsPump = 1 + (0.2/(1-PC_Pump_Eff))

if PC_PumpBeforeMix == 1:

    Cost_PumpBefMix = 632.22*PC_PumpBefMix_Power**0.71*econ_factor_EtaIsPump*econ_Cond_MS_index
    Cost_CondPump = 0

else:

    Cost_CondPump = 632.22*PC_COND.Pump.Power**0.71*econ_factor_EtaIsPump*econ_Cond_MS_index
    Cost_PumpBefMix = 0

if PC_DeaLP == 1:

    Cost_PumpDeaLP = 632.22*PC_PUMP_W_DeaLP**0.71*econ_factor_EtaIsPump*econ_Cond_MS_index

Cost_PumpDeaHP = 632.22*PC_PUMP_W2**0.71*econ_factor_EtaIsPump*econ_Cond_MS_index

result_cost_CAPEX_Pump = Cost_PumpDeaHP + Cost_PumpDeaLP + Cost_PumpBefMix + Cost_CondPump

# BOILER (function of BiomassFeedstock_litarature)
result_cost_CAPEX_Boiler = (-11.6*(Fuel_BiomassFeedstock)**2+43200*(Fuel_BiomassFeedstock)+3000000)*econ_Boiler_corr_factor

# Prep-Yard (function of BiomassFeedstock)

#if BiomassFeedstock > 680 ton/day
    #C_ref = 5748040 $
    #BF_ref = 680 ton/day
    #scale_fact = 0.85

result_cost_CAPEX_PrepYard = Fuel_BiomassFeedstock*(0.0562*(Fuel_BiomassFeedstock**2)-74.761*Fuel_BiomassFeedstock+33311)

# direct CAPEX sub-total
directCAPEX_st = (result_cost_CAPEX_STG_Cost + result_cost_CAPEX_Condenser_Cost + result_cost_CAPEX_PH + result_cost_CAPEX_Dea + result_cost_CAPEX_Pump +result_cost_CAPEX_Boiler + result_cost_CAPEX_PrepYard)/0.67 #the 33# of CAPEX is about engineering,construction and so on

# directCAPEX_st = (result_cost_CAPEX_STG_Cost + result_cost_CAPEX_Condenser_Cost +...
#  result_cost_CAPEX_Boiler + result_cost_CAPEX_PrepYard)/0.6; #the 33# of CAPEX is about engineering,construction and so on

if model_location == 3:
    directCAPEX_st = directCAPEX_st*1.10

# Total direct CAPEX
result_cost_CAPEX_directTot = directCAPEX_st

## ---------------------    Indirect Costs     -------------------------- #

# Total indirect CAPEX
result_cost_CAPEX_indirectTot = 0

## -----------------------     Total CAPEX      ------------------------- #
result_cost_CAPEXtot = result_cost_CAPEX_directTot + result_cost_CAPEX_indirectTot

result_cost_Cspec = result_cost_CAPEXtot/(PC_Wset*1000)# [USD/kWe]
# ---------------------------- depreciation ------------------------------#
