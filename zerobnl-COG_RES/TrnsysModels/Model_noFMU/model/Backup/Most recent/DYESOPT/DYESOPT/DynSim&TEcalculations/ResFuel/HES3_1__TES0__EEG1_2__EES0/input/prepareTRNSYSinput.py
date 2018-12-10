import numpy as np
from PPSteadyStateDesign.EEG.EEG1_2.PowerBlock import *

## -------------------------- Steam Turbine ------------------------------#

#HPT1
TRNSYS_HPT1_Pi_dsgn     = PC_st[PC_keyst_HPTin_n_st-1,1]
TRNSYS_HPT1_Po_dsgn     = PC_st[PC_keyst_HPTin_n_st-1,1]/PC_HPT_pr[0]
TRNSYS_HPT1_FR_dsgn     = PC_st[PC_keyst_HPTin_n_st-1,7]*3600
TRNSYS_HPT1_ETA_dsgn    = PC_HPT_ETA[0,0]
TRNSYS_HPT1_bypass      = 1

TRNSYS_HPT1_Po          = PC_st[PC_keyst_HPTin_n_st+1-1,1]
TRNSYS_HPT1_FR          = PC_st[PC_keyst_HPTin_n_st-1,7]*3600
TRNSYS_HPT1_h           = PC_st[PC_keyst_HPTin_n_st-1,2]

if PC_n_hotPH > 1 or (PC_n_hotPH == 1 and PC_DeaLocatHP == 1):
    #HPT2 yes
    TRNSYS_HPT2_Pi_dsgn     = PC_st[PC_keyst_HPTin_n_st+2-1,1]
    TRNSYS_HPT2_Po_dsgn     = PC_st[PC_keyst_HPTin_n_st+2-1,1]/PC_HPT_pr[1]
    TRNSYS_HPT2_FR_dsgn     = PC_st[PC_keyst_HPTin_n_st+2-1,7]*3600
    TRNSYS_HPT2_ETA_dsgn    = PC_HPT_ETA[0,1]
    TRNSYS_HPT2_bypass      = 1

    TRNSYS_HPT2_Po          = PC_st[PC_keyst_HPTin_n_st+3-1,1]
    TRNSYS_HPT2_FR          = PC_st[PC_keyst_HPTin_n_st+2-1,7]*3600
    TRNSYS_HPT2_h           = PC_st[PC_keyst_HPTin_n_st+2-1,2]

if PC_DeaLocatHP == 0:
    #LPT1 (IPT]
    TRNSYS_IPT_Pi_dsgn     = PC_st[PC_keyst_IPTin_n_st-1,1]
    TRNSYS_IPT_Po_dsgn     = PC_st[PC_keyst_IPTin_n_st+1-1,1]
    TRNSYS_IPT_FR_dsgn     = PC_st[PC_keyst_IPTin_n_st-1,7]*3600
    TRNSYS_IPT_ETA_dsgn    = PC_IPT_ETA
    TRNSYS_IPT_bypass      = 1

    TRNSYS_IPT_Po          = PC_st[PC_keyst_IPTin_n_st+1-1,1]
    TRNSYS_IPT_FR          = PC_st[PC_keyst_IPTin_n_st-1,7]*3600
    TRNSYS_IPT_h           = PC_st[PC_keyst_IPTin_n_st-1,2]



#LPT1
TRNSYS_LPT1_Pi_dsgn     = PC_st[PC_keyst_LPTin_n_st-1,1]
TRNSYS_LPT1_Po_dsgn     = PC_st[PC_keyst_LPTin_n_st+1-1,1]
TRNSYS_LPT1_FR_dsgn     = PC_st[PC_keyst_LPTin_n_st-1,7]*3600
TRNSYS_LPT1_ETA_dsgn    = PC_LPT_ETA[0,0]
TRNSYS_LPT1_bypass      = 1

TRNSYS_LPT1_Po          = PC_st[PC_keyst_LPTin_n_st+1-1,1]
TRNSYS_LPT1_FR          = PC_st[PC_keyst_LPTin_n_st-1,7]*3600
TRNSYS_LPT1_h           = PC_st[PC_keyst_LPTin_n_st-1,1]

if PC_n_coldPH > 0:
    #LPT2 yes
    TRNSYS_LPT2_Pi_dsgn     = PC_st[PC_keyst_LPTin_n_st+2-1,1]
    TRNSYS_LPT2_Po_dsgn     = PC_st[PC_keyst_LPTin_n_st+3-1,1]
    TRNSYS_LPT2_FR_dsgn     = PC_st[PC_keyst_LPTin_n_st+2-1,7]*3600
    TRNSYS_LPT2_ETA_dsgn    = PC_LPT_ETA[0,1]
    TRNSYS_LPT2_bypass      = 1

    TRNSYS_LPT2_Po          = PC_st[PC_keyst_LPTin_n_st+3-1,1]
    TRNSYS_LPT2_FR          = PC_st[PC_keyst_LPTin_n_st+2-1,7]*3600
    TRNSYS_LPT2_h           = PC_st[PC_keyst_LPTin_n_st+2-1,2]

        #LPT2 yes
    if PC_DoubleCond == 1:
        #LPT3 yes
        TRNSYS_LPT3_Pi_dsgn     = PC_st[PC_keyst_LPTin_n_st+4+PC_DeaLP-1,1]
        TRNSYS_LPT3_Po_dsgn     = PC_st[PC_keyst_LPTin_n_st+5+PC_DeaLP-1,1]
        TRNSYS_LPT3_FR_dsgn     = PC_st[PC_keyst_LPTin_n_st+4+PC_DeaLP-1,7]*3600
        TRNSYS_LPT3_ETA_dsgn    = PC_LPT_ETA[0,2]
        TRNSYS_LPT3_bypass      = 1

        TRNSYS_LPT3_Po          = PC_st[PC_keyst_LPTin_n_st+5+PC_DeaLP-1,1]
        TRNSYS_LPT3_FR          = PC_st[PC_keyst_LPTin_n_st+4+PC_DeaLP-1,7]*3600
        TRNSYS_LPT3_h           = PC_st[PC_keyst_LPTin_n_st+4+PC_DeaLP-1,2]

## Boiler

TRNSYS_Boiler_Q     = PC_ECO_Q + PC_EV_Q + PC_SH_Q

TRNSYS_Boiler_h_out = PC_st[PC_keyst_HPTin_n_st-1,2]

TRNSYS_Boiler_Fuel  = Fuel_LHV

if PC_RHpresence == 1:

    TRNSYS_ReHeat_Q           = PC_RH_Q

    TRNSYS_ReHeat_h_out       = PC_st[PC_keyst_HPTin_n_st-1,2]

    TRNSYS_ReHeat_Pdrop       = PC_RH_dP


TRNSYS_ECO_UA            =   PC_ECO_UA   *3600           #o.PC.ECO.UA; %ok kW/K
TRNSYS_EV_UA            =     PC_EV_UA   *3600         #o.PC.EVA.UA; %ok
TRNSYS_SH_UA            =      PC_SH_UA  *3600         #o.PC.SH.UA; %ok
#
## ---------------------------- PUMPS ------------------------------------#
if PC_PumpBeforeMix == 0:
    #PUMP 1
    TRNSYS_PUMP1_mode       = 2
    TRNSYS_PUMP1_Pin        = PC_st[0,1]
    TRNSYS_PUMP1_ro         = 1000
    TRNSYS_PUMP1_ETA        = PC_COND_Pump_EFF
    TRNSYS_PUMP1_W          = PC_COND_Pump_Power*3600            #kJ/hr
else:
    TRNSYS_PUMP_befmix_mode       = 2
    TRNSYS_PUMP_befmix_Pin        = PC_st[0,1]
    TRNSYS_PUMP_befmix_ro         = 1000
    TRNSYS_PUMP_befmix_ETA        = PC_Pump_Eff
    TRNSYS_PUMP_befmix_W          = PC_PumpBefMix_Power*3600     #kJ/hr
    TRNSYS_PUMP_befmix_Pout          = PC_st[3-1,1]
	


if PC_DeaLP == 1:
    TRNSYS_PUMP_dealp_mode       = 2
    TRNSYS_PUMP_dealp_Pin        = PC_st[(PC_keyst_LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP)-1,1]
    TRNSYS_PUMP_dealp_ro         = 1000
    TRNSYS_PUMP_dealp_ETA        = PC_Pump_Eff
    TRNSYS_PUMP_dealp_W          = PC_PUMP_W_DeaLP*3600 #kJ/hr
    TRNSYS_PUMP_dealp_Pout          = PC_st[6-1,1]

#PUMP 2
TRNSYS_PUMP2_mode       = 2
TRNSYS_PUMP2_Pin        = PC_st[PC_keyst_DEAin_n_st+1-1,1]
TRNSYS_PUMP2_ro         = 1000
TRNSYS_PUMP2_ETA        = PC_Pump_Eff
TRNSYS_PUMP2_W          = PC_PUMP_W2*3600 #kJ/hr
TRNSYS_PUMP2_Pout          = PC_st[10-1,1]


## -------------------------- SUBCOOLERS ---------------------------------#
#HE1
TRNSYS_HE1_UA           = PC_hotSC[0,1]*3600
TRNSYS_HE1_Cp_hot       = np.minimum(PC_hotSC[0,2],PC_hotSC[0,3])
TRNSYS_HE1_CP_cold      = np.maximum(PC_hotSC[0,2],PC_hotSC[0,3])
TRNSYS_HE1_FRref_cold   = PC_st[PC_keyst_DEAin_n_st+1-1,7]*3600

#---COLD-----#
#HE3
TRNSYS_HE3_UA           = PC_coldSC[0,1]*3600
TRNSYS_HE3_Cp_hot       = np.minimum(PC_coldSC[0,2],PC_coldSC[0,3])
TRNSYS_HE3_CP_cold      = np.maximum(PC_coldSC[0,2],PC_coldSC[0,3])
TRNSYS_HE3_FRref_cold   = PC_st[PC_keyst_DEAin_n_st-1,7]*3600

#
## -------------------------- PREHEATERS ---------------------------------#

#PH1
TRNSYS_PH1_Cp_cold      = PC_hotPH[0,3]
TRNSYS_PH1_UA           = PC_hotPH[0,1]*3600
TRNSYS_PH1_FRref_cold   = PC_st[PC_keyst_DEAin_n_st+1-1,7]*3600
TRNSYS_PH1_onoff        = 1

#---COLD----#
#PH3
TRNSYS_PH3_Cp_cold      = PC_coldPH[0,3]
TRNSYS_PH3_UA           = PC_coldPH[0,1]*3600
TRNSYS_PH3_FRref_cold   = PC_st[PC_keyst_DEAin_n_st-1,7]*3600
TRNSYS_PH3_onoff        = 1


## -------------------- Deaerator & Condenser ----------------------------#

#Deaerator

#Condenser

if PC_PCONDset != 3:
    TRNSYS_CND_UAref    =     PC_COND_UA*3600


    TRNSYS_CND_Ttarget   = PC_COND_Tcout
    TRNSYS_CND_Pmax       = PC_COND_fan_Power*3600
    TRNSYS_CND_TTDref    = PC_COND_dTapp
    TRNSYS_CND_UAexp        = 1
    TRNSYS_CND_FRamax       = PC_COND_air_FR*3600

    TRNSYS_CND_Hin=   PC_st[PC_keyst_LPTout_n_st-1,2]
    TRNSYS_CND_FRcond= PC_st[PC_keyst_LPTout_n_st-1,7]*3600
    TRNSYS_CND_Tair_in= design_Tamb   ###OSAMA--> Should be fixed in design power plant first, as it is avoided by having a 7th design mode
    TRNSYS_CND_Tin=  PC_st[PC_keyst_LPTout_n_st-1,0]

elif PC_PCONDset == 3:

    if PC_DoubleCond == 1:
	
        TRNSYS_PC_COND1_P = PC_COND1_P *100 # kPa
        TRNSYS_PC_COND2_P = PC_COND2_P * 100 # kPa


        TRNSYS_UA_COND2       = PC_COND2_UA_DELTA*3600

        TRNSYS_DH_massflow   = PC_DH_massflow

        TRNSYS_DH_T_out_COND1  = PC_DH_T_return + APPROACH_COND1

        TRNSYS_DH_T_in_COND1 = PC_DH_T_return



        TRNSYS_DH_T_out_COND2 = PC_DH_T_supply

        TRNSYS_DH_T_in_COND2 = PC_DH_T_return + APPROACH_COND1


    TRNSYS_DH_massflow  = PC_DH_massflow *3600

    TRNSYS_DH_T_supply  = PC_DH_T_supply

## -----------------------------------------------------------------------#
#-------------------------------------------------------------------------#
#-------------------------------------------------------------------------#


