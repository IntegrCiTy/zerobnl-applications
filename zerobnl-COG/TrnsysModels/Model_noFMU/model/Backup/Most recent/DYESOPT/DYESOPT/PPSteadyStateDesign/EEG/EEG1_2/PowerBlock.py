##################################################errorW#######################################################

# Convergence Functions ----------------------------------------------- ##

def errorW(FR):
    PC_mdot= FR
    # import PPSteadyStateDesign.EEG.EEG1_2.rankine_reheat
    [PC_COND1_P, PC_COND2_P,PC_EV_UA, PC_ECO_UA, PC_SH_UA, PC_COND_Area, PC_COND2_Area, PC_COND1_Area,PC_W_HPT, PC_W_LPT,PC_Wparas, PC_W, APPROACH_COND1, PC_COND2_UA_DELTA, PC_COND_air_FR, PC_COND_fan_Power, PC_COND_Tcout, PC_COND_UA,PC_coldPH, PC_hotPH, PC_coldSC, PC_hotSC, PC_PUMP_W2, PC_PUMP_W_DeaLP, PC_PumpBefMix_Power, PC_ECO_Q, PC_EV_Q ,PC_SH_Q,PC_Wgross_el,PC_W_el, PC_CONDs_Q, PC_st,PC_keyst_DEAin_n_st, PC_keyst_PUMP2out_n_st, PC_keyst_HPTin_n_st, PC_keyst_IPTin_n_st, PC_keyst_LPTin_n_st, PC_keyst_LPTout_n_st, PC_LPT_ETA, PC_IPT_ETA, PC_HPT_ETA] = rankine_reheat.rankine_reheat(PC_mdot)
    if PC_Plant_output_mode == 1:
        if PC_convmode == 1:

            ErrW = (PC_Wset - PC_Wgross_el/1000)/(PC_Wset)*100
        else:
            ErrW = (PC_Wset - PC_W_el/1000)/(PC_Wset)*100
    else:
        ErrW = (PC_Heat_demand - PC_CONDs_Q/1000)/PC_Heat_demand*100

    return [ErrW]
############################################################################################################################
############################################################################################################################


# Here the Rankine cycle sizing is run. This function performs
#the iterations to achieve the right mass flow in a Rankine cycle.

from Core.setDefaultParameters import*
from Core.setModelLabel import*

#Valid as long as we are already in the dedicated PowerBlock file
from DesignParameters.EEG1_2_Def_Par import *
from DesignParameters.HES3_1_Def_Par import *
from PPSteadyStateDesign.EEG.EEG1_2.rankine_reheat import *
from PPSteadyStateDesign.EEG.EEG1_2 import rankine_reheat

import numpy as np
import scipy.optimize as opt

PC_Wset = PC_Wset_plant/PC_units_num

##
# Check if the inputs are not crazy......................................#
if PC_DoubleCond == 0:                                                    # simple Rankine case with IPT stage
    if PC_PinIPT >= 0:
        if (((PC_PinHPT)/(PC_PinIPT+PC_RH_dP))**(1/max(PC_n_hotPH,1))) > 1.2 and  (((PC_PinIPT)/1)**(1/max(PC_n_coldPH,1))) > 1.2:
            success = 1

        else:
            print('PR at turbine stage is below 1.2 at design conditions')
            success = 0
    elif PC_PinIPT < 0 and PC_PinHPT > (PC_RH_dP*1.2):
        success = 1
    else:
        print('Pin at HPT is low')
        success = 0
elif PC_DoubleCond == 1:                                                 #vattenfall
    success = 1

if success == 1:


############################################################################################################################
############################################################################################################################
############################################################################################################################
###################################################     fsolve trial    ####################################################


    if PC_Plant_output_mode == 1:
        PC_mdot = opt.fsolve(errorW, PC_Wset, args=(), fprime=None, full_output=0, col_deriv=0, xtol=1.49012e-08, maxfev=0, band=None, epsfcn=None, factor=100, diag=None)

    elif PC_Plant_output_mode == 2:
        PC_mdot = opt.fsolve(errorW, PC_Heat_demand, args=(), fprime=None, full_output=0, col_deriv=0, xtol=1.49012e-08, maxfev=0, band=None, epsfcn=None, factor=100, diag=None)
    [PC_COND1_P, PC_COND2_P,PC_EV_UA, PC_ECO_UA, PC_SH_UA, PC_COND_Area, PC_COND2_Area, PC_COND1_Area,PC_W_HPT, PC_W_LPT,PC_Wparas, PC_W, APPROACH_COND1, PC_COND2_UA_DELTA, PC_COND_air_FR, PC_COND_fan_Power, PC_COND_Tcout, PC_COND_UA,PC_coldPH, PC_hotPH, PC_coldSC, PC_hotSC, PC_PUMP_W2, PC_PUMP_W_DeaLP, PC_PumpBefMix_Power, PC_ECO_Q, PC_EV_Q ,PC_SH_Q,PC_Wgross_el,PC_W_el, PC_CONDs_Q, PC_st,PC_keyst_DEAin_n_st, PC_keyst_PUMP2out_n_st, PC_keyst_HPTin_n_st, PC_keyst_IPTin_n_st, PC_keyst_LPTin_n_st, PC_keyst_LPTout_n_st, PC_LPT_ETA, PC_IPT_ETA, PC_HPT_ETA] = rankine_reheat.rankine_reheat(PC_mdot)


# Check success
if PC_mdot < np.spacing(1):
    #report occurance of negative mass flow rate#
    success = 0
else:
    #report success#
    success = 1

if design_HTFloop_set == 1:
    if HTF[0,3] < np.spacing(1):
                #report occurance of negative mass flow rate#
        success = 0
    elif HTF[5,0] < HTFloop_bottomFreezingT: # This is a double check..(not so useful I guess or it might be if you do not put it in an possible new HTF cycle)
        print(' Salts freezing temperature reached - consider water preheating')
        success = 0
    elif HTF[5,0] >= HTFloop_bottomFreezingT and HTF[5,0] < HTFloop_topFreezingT:
            #report success#
        print([' Cold salts T at design is close to freezing point: ',str(HTF[5,0]),''])
        success = 1
        for i in range (1,len(PC_st[:,7])+1):
            if PC_st[i-1,7] < np.spacing(1):
                success = 0

    elif HTF[0,0] > HTFloop_maxT:
            print(' Salts maximum temperature reached - consider lower Tset point at receiver outlet')
            success = 0

    else:
        success = 1
        for i in range (1,len(PC_st[:,7])+1):
            print(i)
            if PC_st[i-1,7] < np.spacing(1):
                success = 0


##--------------------Steam turbine - start-up data --------------------##
if StartupsMode == 'startupsVs1':
    from PPSteadyStateDesign.EEG.EEG1_2.turbcontrol_data import *                                                                                 # MOVE FROM HERE TO RANKINE CYCLE ASAP

