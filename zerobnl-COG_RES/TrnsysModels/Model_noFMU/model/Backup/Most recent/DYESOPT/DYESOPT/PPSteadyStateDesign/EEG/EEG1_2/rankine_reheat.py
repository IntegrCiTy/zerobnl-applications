

# Here all the thermodynamic properties of the Rankine cycle are evaluated.

from Core.setDefaultParameters import*
from Core.setModelLabel import*
from Core.designPowerPlant import*
from PPSteadyStateDesign.EEG.EEG1_2.PowerBlock import *

#Valid as long as we are already in the dedicated rankine reheat file
from DesignParameters.EEG1_2_Def_Par import *
from DesignParameters.HES3_1_Def_Par import *
from PPSteadyStateDesign.EEG.EEG1_2.STurb import *
from PPSteadyStateDesign.EEG.EEG1_2.subcooler import *
from PPSteadyStateDesign.EEG.EEG1_2.preheater import *
from PPSteadyStateDesign.EEG.EEG1_2.economizer import *
from PPSteadyStateDesign.EEG.EEG1_2.evaporator import *
from PPSteadyStateDesign.EEG.EEG1_2.completestates import *



def rankine_reheat(PC_mdot):
    from DesignParameters.EEG1_2_Def_Par import PC_LPT_pr
    from DesignParameters.EEG1_2_Def_Par import PC_HPT_pr
    # Needed libraries
    import numpy as np

    # Python implementation of standards from The InternationalAssociation for the Properties of Water and Steam
    from iapws import IAPWS97

    ##
    if PC_PCONDset   == 1:

        PC_COND_Tcout = design_Tdrycond + PC_COND_dTapp
    # TO be fixed --> Osama
    #     PROP(9) = 0 PROP(1) = PC_COND.Tcout [PROP] = steamprop(PROP,7)
    #     PC_COND.P = PROP(2)

    elif PC_PCONDset == 2:

        T_air_in           = design_Tamb
        T_air_out          = T_air_in + PC_COND_air_dT
        PC_COND_Tcout      = PC_COND_dTapp + T_air_out
        PC_COND            = IAPWS97(T=PC_COND_Tcout+273.15, x=0) # x is the steam quality. 0 = liquid
        PC_COND_P          = PC_COND.P*10                         # the MPa to bar due to the steam library

    elif PC_PCONDset == 3:                                 #DH

        if PC_DoubleCond   == 0:

           PC_COND_Tcout   = PC_dT_wtr_out_condensing + PC_DH_T_supply
           PC_COND         = IAPWS97(T=PC_COND_Tcout+273.15, x=0)            #saturated liquid with known T
           PC_COND_P       = PC_COND.P*10                                    # the MPa to bar due to the steam library
           PC_COND_h_cout  = PC_COND.h

        elif PC_DoubleCond == 1:

           PC_DH_T_return  = PC_DH_T_supply - (PC_Heat_demand*1000/(PC_DH_massflow*4.186))+PC_DtFGC
           APPROACH_COND1  = (PC_DH_T_supply - PC_DH_T_return)*PC_Double_approach # 30 * 0.45
           PC_COND1_Tcout  = PC_DH_T_return + APPROACH_COND1 + PC_dT_wtr_out_condensing # 40 + 13.5 + 2
           PC_COND1        = IAPWS97(T=PC_COND1_Tcout+273.15, x=0)
           PC_COND1_P      = PC_COND1.P*10                                  # the MPa to bar due to the steam library  		   
           PC_COND1_h_cout = PC_COND1.h
           PC_COND_Tcout   = 0 ##Osama --> To assign a value for returning the object
           # EXTRA CONDENSER

           # For the backup condenser the traditional pinch point technique is
           # used.
           PC_COND2_Tcout  = PC_dT_wtr_out_condensing + PC_DH_T_supply # 2 + 75
           PC_COND2        = IAPWS97(T=PC_COND2_Tcout+273.15, x=0)
           PC_COND2_P      = PC_COND2.P*10                                  # the MPa to bar due to the steam library
           PC_COND2_h_cout = PC_COND2.h

           #the condensers could introduce a small pressure drop. Now I'm
           #considering just the pressures outside the condensers.


    if PC_DoubleCond == 0:
        PC_HPT_f = (PC_PinHPT - PC_COND_P)/(PC_Pcrit - PC_COND_P)

        if PC_COND_P >= 1.05:
            print('Pcond cannot exceed atmospheric pressure')
            success = 0
        elif PC_HPT_f >= 0.9:
            print('HPT pressure factor cannot exceed 0.8')
            success = 0

    # Defining number of states in the cycle

    PC_n_states   =    (1 +                                                  # Out Cond 1
                          PC_DoubleCond +                                    # Out Cond 2
                          PC_ValveCond_2 +                                   # Out Valve Cond 2
                          PC_PumpBeforeMix +                                 # Out pump (after cond1) before mixing the fluxes
                          PC_DoubleCond +                                    # After the fluxes out from the conds mix
                          (1-PC_PumpBeforeMix) +                             # Out cold pump (always exists, except in Vattenfall case where there is the pump before mix)
                          PC_DeaLP +                                         # Out DeaLP
                          PC_DeaLP +                                         # Out DeaLP pump
                          2*PC_n_coldPH +                                    # feedwater inlet DeaHP
                          1 +                                                # Out DeaHP
                          1 +                                                # Out DeaHP pump
                          2*PC_n_hotPH +                                     # In boiler
                          PC_BackPrValve +                                   # In boiler where extracted steam returns into the main circuit
                          PC_BoilerValve +                                   # In boiler if there is the valve (Vattenfall)
                          PC_BoilerMode +                                    # Out ECO (if present)
                          1 +                                                # Out EVA
                          1 +                                                # Out SH (HPT inlet)
                          PC_BackPrValve +                                   # In HPT (if live steam extraction if present)
                          max(1,PC_n_hotPH*2) + 2*PC_DeaLocatHP +            # Out HPT
                          PC_RHpresence +                                    # Out RH (in IPT or LPT)
                          (1-PC_DeaLocatHP) +                                # Out IPT (simple case)
                          (1-PC_DeaLocatHP) +                                # In LPT (simple case)
                          2*PC_n_coldPH + 2*PC_DeaLP + 2*PC_DoubleCond + (1-PC_DeaLP) +  # Out LPT
                          PC_n_hotPH +                                       # Extraction lines to hot PH
                          1 +                                                # Extraction line to deaHP
                          PC_n_coldPH +                                      # Extraction lines to cold PH
                          PC_DeaLP +                                         # Extraction line to deaLP
                          PC_DoubleCond +                                    # Extraction line to Cond 2
                          2*(PC_n_hotPH + PC_n_coldPH) +                     # Steams from PH --> SC and from SC --> PH
                          PC_BackPrValve +                                   # live steam extraction before the valve
                          PC_BackPrValve +                                   # live steam extr after the valve
                          PC_BackPrValve)                                    # flux after the additional HX



    PC_st = np.zeros(shape=(PC_n_states,9))                                  # St prop Matrix [T  P  h  s  q  v  u  FR  cp0]

    PC_nT_stages = max(1,PC_n_hotPH) + PC_n_coldPH + 2 + PC_DoubleCond       # Number of turbine stages (the extraction for the Cond 2 and for the DeaLP is the same in Vattenfall)

    # ---------------------------------------------------------------------- #
    ## Identifying key states
    DEAin_n_st          =  (1 +                                              # Out Cond 1
                          PC_DoubleCond +                                    # Out Cond 2
                          PC_ValveCond_2 +                                   # Out Valve Cond 2
                          PC_PumpBeforeMix +                                 # Out pump (after cond1) before mixing the fluxes
                          PC_DoubleCond +                                    # After the fluxes out from the conds mix
                          1*(1-PC_PumpBeforeMix) +                           # Out cold pump (always exists, except in Vattenfall case where there is the pump before mix)
                          PC_DeaLP +                                         # Out DeaLP
                          PC_DeaLP +                                         # Out DeaLP pump
                          2*PC_n_coldPH )                                    # cold stream at HPdeaerator inlet


    PUMP2out_n_st       =  (DEAin_n_st +                                     # cold stream at deaerator inlet
                            1 +                                              # At deaerator outlet
                            1)                                               # At PUMP 2 outlet


    HPTin_n_st          =  (PUMP2out_n_st +                                  # At PUMP 2 outlet
                            PC_n_hotPH*2 +                                   # after the last hot PH
                            PC_BackPrValve +                                 # after steam extraction mixing
                            PC_BoilerValve +                                 # In boiler if there is the valve [Vattenfall]
                            PC_BoilerMode +                                  # At Economizer outlet (0 if not ECO)
                            1 +                                              # At Evaporator outlet
                            1 +                                              # At Superheater outlet / Live steam
                            PC_BackPrValve)                                  # In HPT if Backpressure valve is considered

    IPTin_n_st          =  (HPTin_n_st +
                            max(1,PC_n_hotPH*2) +                            # At HPT outlet
                            + 2*PC_DeaLocatHP +                              # At HPT outlet [Vattenfall]
                            PC_RHpresence)                                   # At Reheater outlet


    LPTin_n_st          =   IPTin_n_st+2*(1-PC_DeaLocatHP)                  # LPT inlet (for DC and Vattenfall coincides with IPTin)


    LPTout_n_st         =   (LPTin_n_st +
                            2*PC_n_coldPH +
                            2*PC_DeaLP + 2*PC_DoubleCond + (1-PC_DeaLP))    # At LPT outlet

    # Indexing this into structure:
    PC_keyst_DEAin_n_st     = DEAin_n_st
    PC_keyst_PUMP2out_n_st  = PUMP2out_n_st
    PC_keyst_HPTin_n_st     = HPTin_n_st
    PC_keyst_IPTin_n_st     = IPTin_n_st
    PC_keyst_LPTin_n_st     = LPTin_n_st
    PC_keyst_LPTout_n_st    = LPTout_n_st

    # T:1 , P:2 , h:3 , 4:s , 5:x , 6:v , 7:my , 8:mf , 9:Cp , 10:tc

    ## Here is where FRnom is input:

    if PC_BackPrValve       == 0:
        for i in range ((PUMP2out_n_st-2),(HPTin_n_st+1),1):                             # nominal mass flow rate between DeaHP outlet and HPT (inlet or outlet of the first stage)
            PC_st[i,7]      = PC_mdot                                                    # Change made for accommodating the zero start in python

    elif PC_BackPrValve     == 1:
        for i in range ((PUMP2out_n_st + PC_n_hotPH*1 + PC_BackPrValve), (HPTin_n_st-PC_BackPrValve), 1):  # Change made for accommodating the zero start in python
            PC_st[i,7]      = PC_mdot                                                                      # Change made for accommodating the zero start in python

    # ----------------------------------------------------------------------- #
    ## Defining Pressure lines

    if PC_DoubleCond == 0:                                                                                 # Rankine cycle simple with IPT

        PC_st[(LPTout_n_st-1),1] = (PC_COND_P*(1+PC_COND_Pdrop))                                             #Pressure at the outlet of LPT / # Change made for accommodating the zero start in python

        if PC_PinIPT <= 0:
            PC_IPT_f  = 0.8
            PC_HPT_PR = 1
            PC_IPT_PR = 2
            while (abs(PC_HPT_PR - PC_IPT_PR)*100/PC_HPT_PR) > 5:
                PC_IPT_f = PC_IPT_f - 0.005
                if PC_IPT_f <= 0.005:
                    print('Limit in PC_IPT_f iteration reached')
                    success = 0
                    break

                PC_st[HPTin_n_st-1,1]   = PC_COND_P + PC_HPT_f*(PC_Pcrit - PC_COND_P)                          # steam pressure at HPT inlet / # Change made for accommodating the zero start in python
                PC_st[IPTin_n_st-1,1]   = (PC_COND_P + PC_IPT_f*(PC_st[HPTin_n_st,2] - PC_RH_dP - PC_COND_P))  # steam pressure at IPT inlet / # Change made for accommodating the zero start in python

        elif PC_PinIPT > PC_COND_P and PC_PinIPT < PC_PinHPT:                                                  # Check if the IPT pressure is higher than pCOND and HPT pressure is higher that IPT one
            PC_st[HPTin_n_st-1,1]   = PC_COND_P + PC_HPT_f*(PC_Pcrit - PC_COND_P)                              # steam pressure at HPT inlet (by defaultParameters)
            PC_IPT_f = (PC_PinIPT - PC_COND_P)/(PC_st[HPTin_n_st-1,1] - PC_RH_dP - PC_COND_P)
            PC_st[IPTin_n_st-1,1] = PC_COND_P + PC_IPT_f*(PC_st[HPTin_n_st-1,1] - PC_RH_dP - PC_COND_P)        # steam pressure at IPT inlet (by defaultParameters)/ # Change made for accommodating the zero start in python

        else:
            print('PinIPT cannot be less than Pcond')
            success = 0

    elif PC_DoubleCond == 1:                                                                                    # Change made for accommodating the zero start in python


        PC_st[LPTout_n_st-1,1] = PC_COND1_P*(1+PC_COND_Pdrop)   #25          #pressure at the LPT outlet and at the previous LP-stage outlet

        PC_st[LPTout_n_st-2,1] = PC_COND2_P*(1+PC_COND2_Pdrop) #24

        PC_st[LPTout_n_st-3,1] = PC_COND2_P*(1+PC_COND2_Pdrop) #23

        PC_st[LPTout_n_st-3-PC_DeaLP,1] = PC_COND2_P*(1+PC_COND2_Pdrop) # 22

        PC_st[(LPTout_n_st+PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond)-1,1]= PC_COND2_P*(1+PC_COND2_Pdrop) #30



    PC_st[HPTin_n_st-1,1]     = PC_PinHPT #15

    PC_st[IPTin_n_st-1,1]     = PC_PinIPT

    if PC_DeaLocatHP == 1:
        PC_st[LPTin_n_st-1,1] = PC_PinIPT # 19                                   # if the Dea is located before the RH, the IPT stage doesn't really exist

    # Pressure ratios definition.

    # HPT

    if PC_HPT_pr_mod == 0:
        PC_HPT_PR=PC_st[HPTin_n_st-1,1]/((1+PC_HPTout_dp)*PC_st[IPTin_n_st-1,1] + PC_RH_dP)              # Pressure ratio HPT
        PC_HPT_pr[0:(PC_n_hotPH+PC_DeaLocatHP)]=PC_HPT_PR**(1/(max(1,(PC_n_hotPH+PC_DeaLocatHP))))              # simple: 2 PH - 0 DeaHP --> 2 stages;

    elif PC_HPT_pr_mod ==1:
        # PC_HPT_pr is as input                                                                           # Double Condenser: 2 PH - 1 DeaHP --> 3 stages;
        PC_HPT_pr = PC_HPT_pr                                                                                                         # Vattenfall: 1 PH - 1 DeaHP --> 2 stages
    # LPT

    if PC_LPT_pr_mod == 0:
        if PC_DoubleCond == 0:

            PC_LPT_PR    =  PC_st[IPTin_n_st-1,1]/PC_st[LPTout_n_st-1,1]

            PC_LPT_pr = np.zeros(shape=(1,PC_n_coldPH+(1-PC_DeaLocatHP)))
            PC_LPT_pr [0:PC_n_coldPH+(1-PC_DeaLocatHP)]   =  PC_LPT_PR**(1/(max(1,PC_n_coldPH+(1-PC_DeaLocatHP)+1)))


            if PC_DeaLocatHP == 0:
                PC_IPT_PR = np.array(PC_LPT_pr[0,0])

        elif PC_DoubleCond == 1:
            PC_LPT_PR      = PC_st[IPTin_n_st-1,1]/PC_st[LPTout_n_st-3-PC_DeaLP,1]

            PC_LPT_pr = np.zeros(shape=(1,PC_n_coldPH+(1-PC_DeaLocatHP)))
            PC_LPT_pr [0:PC_n_coldPH+(1-PC_DeaLocatHP)]     = PC_LPT_PR**(1/(max(1,PC_n_coldPH+(1-PC_DeaLocatHP)+1)))

            if PC_DeaLocatHP == 0:
                PC_IPT_PR = np.array(PC_LPT_pr[0,0])

    elif PC_LPT_pr_mod ==1:
        # PC_LPT_pr is as input
        PC_LPT_pr = PC_LPT_pr
    # Boiler pressures definition.

    if PC_BackPrValve == 1:
        PC_st[HPTin_n_st-PC_BackPrValve-1,1] = PC_st[HPTin_n_st-1,1]

    PC_st[(HPTin_n_st-PC_BackPrValve-2),1] = PC_st[HPTin_n_st-1,1] + PC_SH_dP                          # saturated steam pressure at superheater inlet
    PC_st[(HPTin_n_st-PC_BackPrValve-3),1] = PC_st[(HPTin_n_st-PC_BackPrValve-2),1] + PC_EV_dP         # condensing pressure at evaporator inlet

    if PC_BoilerMode > 0:                                                                              # if there is an EC take into account
        PC_st[(HPTin_n_st-PC_BackPrValve-4),1] = PC_st[(HPTin_n_st-PC_BackPrValve-3),1] + PC_ECO_dP    # water pressure at economizer inlet
        B=3

    else:
        B=2

    if PC_BoilerValve == 1:
        PC_st[(HPTin_n_st-PC_BackPrValve-B-PC_BoilerValve-PC_BackPrValve-1),1]= PC_st[(HPTin_n_st-PC_BackPrValve-B-1),1] + PC_BValve_dP

    #Defining Pressures between the boiler inlet and the Pump2 outlet

    jj=1

    for i in range ((HPTin_n_st-2*PC_BackPrValve-B-PC_BoilerValve)-2,(PUMP2out_n_st-1),-2):                        #pressures at the HPT_SC outlet = hotPH inlet
        PC_st[i,1] = PC_st[(HPTin_n_st-2*PC_BackPrValve-B-PC_BoilerValve)-1,1]+PC_PdropPHhot*jj+PC_PdropSChot*(jj-1)
        jj=jj+1

    jj=1
    for i in range ((HPTin_n_st-2*PC_BackPrValve-B-PC_BoilerValve)-3,(PUMP2out_n_st)-2,-2):                        #pressures at the HPT_SC inlet
        PC_st[i,1] = PC_st[(HPTin_n_st-2*PC_BackPrValve-B-PC_BoilerValve)-1,1]+PC_PdropPHhot*jj+PC_PdropSChot*jj
        jj=jj+1

    jj=1
    for i in range (0, max(1,PC_n_hotPH*2)+ 2*PC_DeaLocatHP-1, 2):                                                # Defining pressures at HPT stages
        PC_st[HPTin_n_st+i,1] = PC_st[HPTin_n_st+(i-1),1]/PC_HPT_pr[jj-1]
        jj=jj+1
        if PC_n_hotPH != 0 or PC_DeaLocatHP == 1:
            PC_st[HPTin_n_st+(i+1),1] = PC_st[HPTin_n_st+i,1]


    if PC_RHpresence == 0:                                 #takes into account that without RH the index at the HPT outlet coincides with the index at the IPT inlet, so the pressure in that point is the IPTinlet pressure
        PC_st[HPTin_n_st + max(1,PC_n_hotPH*2)+ 2*PC_DeaLocatHP-1,1] = PC_PinIPT

    if PC_n_hotPH != 0:                                                                                           # new states because of hot preheating (hot streams)
        for i in range (1,PC_n_hotPH+1):
            PC_st[LPTout_n_st+(i)-1,1] = (1-PC_HotExtr_dp)*PC_st[HPTin_n_st+(2*i-1)-1,1]                   #PC_HotExtr_dp treated as a single value not a list! Osama                                   # Extraction lines entering PHs at hot preheating
            PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DoubleCond+PC_DeaLP+(2*i-1)-1,1] = (1-PC_HotExtr_dp)*PC_st[HPTin_n_st+(2*i-1)-1,1]  #PC_HotExtr_dp treated as a single value not a list! Osama # lines from PH to SubCooler at hot preheating__NO PRESSURE LOSSES FOR THE STEAM/SAT LIQ LINE
            PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DoubleCond+PC_DeaLP+(2*i-1),1] = (1-PC_HotExtr_dp)*PC_st[HPTin_n_st+(2*i-2),1]     #PC_HotExtr_dp treated as a single value not a list! Osama  # lines from SubCooler to next PH/Deaerator at hot preheating____NO PRESSURE LOSSES FOR THE STEAM/SAT LIQ LINE


    if PC_DeaLocatHP == 1:
         PC_st[(LPTout_n_st+PC_n_hotPH+PC_DeaLocatHP)-1,1]=(1-PC_DeaHPextr_dp)*PC_st[(HPTin_n_st+2*PC_n_hotPH+PC_DeaLocatHP)-1,1]           #extraction line to DeaHP

         PC_st[DEAin_n_st-1,1]   = PC_st[(LPTout_n_st+PC_n_hotPH+PC_DeaLocatHP)-1,1]                                        #Dea Cold Inlet_same p
         PC_st[DEAin_n_st+1-1,1] = PC_st[(LPTout_n_st+PC_n_hotPH+PC_DeaLocatHP)-1,1]                                        #Dea main outlet_same p


    elif PC_DeaLocatHP == 0:
         if PC_IPT_PR == 0:
             PC_st[IPTin_n_st,1] = float('inf')
         else:
            PC_st[IPTin_n_st,1] = PC_st[IPTin_n_st-1,1]/PC_IPT_PR                                                              # Pressure at IPT outlet
         PC_st[IPTin_n_st+1,1] = PC_st[IPTin_n_st,1]                                                                        # Pressure at LPT inlet
         PC_st[LPTout_n_st + PC_n_hotPH,1] = PC_st[IPTin_n_st,1]                                                            # Extraction line to Deaerator

         PC_st[DEAin_n_st-1,1]   = PC_st[IPTin_n_st,1]
         PC_st[DEAin_n_st,1] = PC_st[DEAin_n_st-1,1]

    #LPTin_pressure is defined for all the cases

    if PC_n_coldPH != 0:                                                                                                     # States at LPT and cold preheating
        jj=1
        for i in range (1,((PC_n_coldPH)*2),2):                                                                              # Defining pressures at LPT stages
            PC_st[LPTin_n_st+i-1,1] = PC_st[LPTin_n_st+(i-1)-1,1]/PC_LPT_pr[jj-1]                                          # Pressure at outlet of LPT inner stages
            jj=jj+1
            PC_st[LPTin_n_st+i,1] = PC_st[LPTin_n_st+i-1,1]                                                                  # Pressure at inlet of LPT inner stages

        for i in range (1,PC_n_coldPH+1,1):                                                                                  # new states because of cold preheating (hot streams)
            PC_st[LPTout_n_st + PC_n_hotPH + 1 + (i)-1,1] = (1-PC_ColdExtr_dp[i-1])*PC_st[LPTin_n_st+(2*i-1)-1,1]            # Extraction lines entering PHs at cold preheating
            PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1)-1,1] = (1-PC_ColdExtr_dp[i-1])*PC_st[LPTin_n_st+(2*i-1)-1,1]# lines from PH to SubCooler at cold preheating
            PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,1] = (1-PC_ColdExtr_dp[i-1])*PC_st[LPTin_n_st+(2*i-1)-1,1]    # lines from SubCooler to next PH/Deaerator at cold preheating


    # Pressure at LPT outlet
    if PC_DoubleCond == 0:
        if abs(PC_st[LPTout_n_st-1,1] - PC_COND_P) > PC_COND_P*0.2:
            print('ERROR calculating pressure lines')

        PC_st[0,1] = PC_COND_P

    elif PC_DoubleCond == 1:
        if abs(PC_st[LPTout_n_st-1,1] - PC_COND1_P) > PC_COND1_P*0.2:
            print('ERROR calculating pressure lines')

        PC_st[0,1] = PC_COND1_P
        PC_st[(1+PC_DoubleCond)-1,1]=PC_COND2_P

    jj=1
    for i in range (DEAin_n_st-1,(1 + PC_DoubleCond + PC_ValveCond_2 + PC_PumpBeforeMix + PC_DoubleCond + 1*(1-PC_PumpBeforeMix) + 2*PC_DeaLP),-2): #pressures at LPT_SC outlet = coldPH inlet
        PC_st[i-1,1] = PC_st[DEAin_n_st-1,1]+PC_PdropPHcold*jj+PC_PdropSCcold*(jj-1)
        jj=jj+1

    jj=1

    for i in range (DEAin_n_st-2,(1 + PC_DoubleCond + PC_ValveCond_2 + PC_PumpBeforeMix + PC_DoubleCond + 1*(1-PC_PumpBeforeMix) + 2*PC_DeaLP)-1,-2): #pressures at the LPT_SC inlet # -1 added to create a difference between start and end for running the for loop
        PC_st[i-1,1] = PC_st[DEAin_n_st-1,1]+PC_PdropPHcold*jj+PC_PdropSCcold*jj
        jj=jj+1

    #Here basic Rankine cycle is defined in terms of pressures

    if PC_DeaLP == 1:
        PC_st[(LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP)-1,1]=(1-PC_DeaLPextr_dp)*PC_st[LPTout_n_st-2-PC_DeaLP-1,1] #Extr to DeaLP
        PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix))-1,1]=PC_st[(LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP)-1,1] #DeaLP Cold inlet_ same p
        PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+PC_DeaLP)-1,1]=PC_st[(LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP)-1,1] #DeaLP main outlet_same p
        # p3 = p4 = p5 (HP)_ stages valid only for  Vattenfall case
        PC_st[(1+PC_DoubleCond+PC_ValveCond_2)-1,1]=PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix))-1,1]
        PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix)-1,1]=PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix))-1,1]

    # inlet to HPT (live steam conditions)...
    if design_TinHPTset == 1:
        PC_st[(HPTin_n_st)-1,0] = rec_Tset - STTloss_dsgn - PC_SH_Pinch      #Usually in MS you fix the temperature at the outlet of the receiver and you evaluate the inlet to the HPT # To be fixed later , Receivre related not CHP! --> Osama

    elif design_TinHPTset == 2:
        PC_st[(HPTin_n_st)-1,0] = PC_TinHPT                                  # Usually in DSG and in CHP you fix the temperature at HPT inlet
        HPT_inlet_point = IAPWS97(P=PC_st[(HPTin_n_st)-1,1]/10, T=PC_st[(HPTin_n_st)-1,0]+273.15) # Table with p and T
        PC_st[(HPTin_n_st)-1,2:] = [HPT_inlet_point.h, HPT_inlet_point.s, HPT_inlet_point.x, HPT_inlet_point.v, HPT_inlet_point.u, PC_mdot, HPT_inlet_point.cp0]

        if PC_BackPrValve == 1:
            PC_st[(HPTin_n_st-PC_BackPrValve)-1,0]    = PC_TinHPT
            WithBackPr_point= IAPWS97(P=PC_st[(HPTin_n_st-PC_BackPrValve)-1,1]/10, T=PC_st[(HPTin_n_st-PC_BackPrValve)-1,0]+273.15)
            PC_st[(HPTin_n_st-PC_BackPrValve)-1,2:]  = [WithBackPr_point.h, WithBackPr_point.s, WithBackPr_point.x, WithBackPr_point.v, WithBackPr_point.u, PC_mdot, WithBackPr_point.cp0]

    # inlet to Superheater...
    PC_st[(HPTin_n_st-PC_BackPrValve-1)-1,4]   = 1
    SHeatInlet_point= IAPWS97(P=PC_st[(HPTin_n_st-PC_BackPrValve-1)-1,1]/10, x= 1) # Table with p and x
    PC_st[(HPTin_n_st-PC_BackPrValve-1)-1,:]   = [SHeatInlet_point.T-273.15, PC_st[(HPTin_n_st-PC_BackPrValve-1)-1,1], SHeatInlet_point.h, SHeatInlet_point.s, 1, SHeatInlet_point.v, SHeatInlet_point.u, PC_mdot, SHeatInlet_point.cp0]

    if PC_BoilerMode >0:                                         # If the economizer is included, the EVA inlet conditions need still to be defined

        # inlet to Evaporator...
        PC_st[(HPTin_n_st-PC_BackPrValve-2)-1,4] = 0
        EvapInlet_point= IAPWS97(P=PC_st[(HPTin_n_st-PC_BackPrValve-2)-1,1]/10, x= 0) # Table with p and x
        PC_st[(HPTin_n_st-PC_BackPrValve-2)-1,:]= [EvapInlet_point.T-273.15, PC_st[(HPTin_n_st-PC_BackPrValve-2)-1,1], EvapInlet_point.h, EvapInlet_point.s, 0, EvapInlet_point.v, EvapInlet_point.u, PC_mdot, EvapInlet_point.cp0]

    # Reheater outlet / IPT inlet
    if design_ToutRHset == 1:
        PC_st[(IPTin_n_st)-1,0]     = rec_Tset - STTloss_dsgn - PC_RH_TTD                                                   #In MS you fix the reheat from the the Tset

    elif design_ToutRHset == 2:
        PC_st[(IPTin_n_st)-1,0]     = PC_TinHPT*(1-PC_TdropRH/100)                                                          # In DSG you know the # reheat

    elif design_ToutRHset == 3:
        PC_st[(IPTin_n_st)-1,0]     = PC_TinIPT

    IPTinlet_point= IAPWS97(P=(PC_st[IPTin_n_st-1,1])/10, T= (PC_st[IPTin_n_st-1,0]+273.15))

    PC_st[(IPTin_n_st)-1,2:]= [IPTinlet_point.h, IPTinlet_point.s, IPTinlet_point.x, IPTinlet_point.v, IPTinlet_point.u, 0, IPTinlet_point.cp0]
    
    ## Defining Outlets from Condenser, Deaerator(s), Pump 1 and Pump 2 (and PumpBeforeMix)

    # Condenser outlet (state 1)

    PC_st[0,4]   = 0
    CondOutlet_point= IAPWS97(P=PC_st[0,1]/10, x= 0)
    PC_st[0,:]   = [CondOutlet_point.T-273.15,PC_st[0,1],CondOutlet_point.h, CondOutlet_point.s, CondOutlet_point.x, CondOutlet_point.v, CondOutlet_point.u, 0, CondOutlet_point.cp0]# FR fraction is unknown at the moment

    # Condenser 2 outlet
    if PC_DoubleCond == 1:
        PC_st[(1+PC_DoubleCond)-1,4] = 0
        CondOutlet2_point= IAPWS97(P=PC_st[1+PC_DoubleCond-1,1]/10, x= PC_st[1+PC_DoubleCond-1,4])
        PC_st[1+PC_DoubleCond-1,:]   = [CondOutlet2_point.T-273.15,CondOutlet2_point.P*10,CondOutlet2_point.h, CondOutlet2_point.s, CondOutlet2_point.x, CondOutlet2_point.v, CondOutlet2_point.u, 0, CondOutlet2_point.cp0]# FR fraction is unknown at the moment


    # Deaerator outlet
    PC_st[(DEAin_n_st+1)-1,4]   = 0

    if PC_st[(DEAin_n_st+1)-1,1]== float('inf'):                            # To fix the temporary NaN output
        PC_st[(DEAin_n_st+1)-1,:] = [float('NaN'),float('inf'),float('NaN'), float('NaN'), 0, float('NaN'), float('NaN'), PC_mdot, float('NaN')]

    else:
        DeaOutlet_point= IAPWS97(P=PC_st[(DEAin_n_st+1)-1,1]/10, x= PC_st[(DEAin_n_st+1)-1,4])
        PC_st[(DEAin_n_st+1)-1,:]   = [DeaOutlet_point.T-273.15,DeaOutlet_point.P*10,DeaOutlet_point.h, DeaOutlet_point.s, DeaOutlet_point.x, DeaOutlet_point.v, DeaOutlet_point.u, PC_mdot, DeaOutlet_point.cp0]

    # DeaLP outlet
    if PC_DeaLP == 1:
        PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+PC_DeaLP)-1,4] = 0
        if PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+PC_DeaLP)-1,1] == float('inf'):
            PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+PC_DeaLP)-1,:]= [float('NaN'),float('inf'),float('NaN'), float('NaN'), 0, float('NaN'), float('NaN'), 0, float('NaN')]

        else:
            DeaLPOutlet_point= IAPWS97(P=PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+PC_DeaLP)-1,1]/10, x= PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+PC_DeaLP)-1,4])
            PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+PC_DeaLP)-1,:] = [DeaLPOutlet_point.T-273.15,DeaLPOutlet_point.P*10,DeaLPOutlet_point.h, DeaLPOutlet_point.s, 0, DeaLPOutlet_point.v, DeaLPOutlet_point.u, 0, DeaLPOutlet_point.cp0]

    # PUMP 2 outlet
    if np.isnan(PC_st[(DEAin_n_st+1)-1,0])== True:                            # to fix the NaN issue --> Osama
        PC_st[(PUMP2out_n_st)-1,0]     =float('NaN')
        PC_st[(PUMP2out_n_st)-1,2:]    = [float('NaN'), float('NaN'), 1, float('NaN'), float('NaN'), PC_mdot, float('NaN')] # slight difference in enthalpy in addition to the Cp issue
    else:
        PC_st[(PUMP2out_n_st)-1,0]     = PC_st[(DEAin_n_st+1)-1,0]+PC_TdropPUMP*(PC_st[PUMP2out_n_st-1,1]-PC_st[PUMP2out_n_st-1-1,1])
        PUMP2Outlet_point              = IAPWS97(P=PC_st[(PUMP2out_n_st)-1,1]/10,T= PC_st[(PUMP2out_n_st)-1,0]+273.15)
        PC_st[(PUMP2out_n_st)-1,2:]    = [PUMP2Outlet_point.h, PUMP2Outlet_point.s, PUMP2Outlet_point.x, PUMP2Outlet_point.v, PUMP2Outlet_point.u, PC_mdot, PUMP2Outlet_point.cp0] # slight difference in enthalpy in addition to the Cp issue

    # PUMP DeaLP outlet

    if PC_DeaLP == 1:
        PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+2*PC_DeaLP)-1,0] = (
        PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+PC_DeaLP)-1,0] +
        PC_TdropPUMP*(PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+2*PC_DeaLP)-1,1]-
        PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+PC_DeaLP)-1,1]))

        if PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+2*PC_DeaLP)-1,1]== float('inf'):                            # To fix the temporary NaN output
            PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+2*PC_DeaLP)-1,2:] = [float('NaN'), float('NaN'), 1, float('NaN'), float('NaN'), 0, float('NaN')]

        else:

            DeaLP_point= IAPWS97(P= PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+2*PC_DeaLP)-1,1]/10, T=PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+2*PC_DeaLP)-1,0]+273.15)
            PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)+2*PC_DeaLP)-1,2:] = [DeaLP_point.h, DeaLP_point.s, DeaLP_point.x, DeaLP_point.v, DeaLP_point.u, 0, DeaLP_point.cp0]

    # PumpBeforeMix (at the cond 1 outlet) outlet
    if PC_PumpBeforeMix == 1:
        PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix)-1,0] = PC_st[0,0]+PC_TdropPUMP*(PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix-1,1]- PC_st[0,1])

        if PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix)-1,1] == float('inf'):
            PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix)-1,2:]= [float('NaN'), float('NaN'), 0, float('NaN'), float('NaN'), 0, float('NaN')]
        elif PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix)-1,1] == 0:
            PumpBeforeMix_point= IAPWS97(T= PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix)-1,0]+273.15, x=1)
            PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix)-1,2:] = [PumpBeforeMix_point.h, float('inf'), PumpBeforeMix_point.x, float('inf'), float('NaN'), 0, float('NaN')]

        else:

            PumpBeforeMix_point= IAPWS97(P=PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix)-1,1]/10, T= PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix)-1,0]+273.15)
            PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix)-1,2:] = [PumpBeforeMix_point.h, PumpBeforeMix_point.s, PumpBeforeMix_point.x, PumpBeforeMix_point.v, PumpBeforeMix_point.u, 0, PumpBeforeMix_point.cp0]

    # PUMP 1 outlet -----> temperature is significantly low, to be checked -----> Osama
    if PC_PumpBeforeMix == 0:
        PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)-1,0] = (
            PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond-1,0]+PC_TdropPUMP*
            (PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)-1,1]-
            PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond-1,1]))

        Pump1Outlet_point= IAPWS97(P= PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)-1,1]/10, T= PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)-1,0]+273.15)         # FR fraction is unknown at the moment
        PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+1*(1-PC_PumpBeforeMix)-1,2:] = [Pump1Outlet_point.h, Pump1Outlet_point.s, Pump1Outlet_point.x, Pump1Outlet_point.v, Pump1Outlet_point.u, 0, Pump1Outlet_point.cp0]

    	
    # # Nel caso semplice con DOUBLE COND non so ne la T ne la P prima della
    # # pompa; la T la posso supporre come media ponderata delle due T!!!!!!!!!! (T is asnp.sumed as weighted average of the two Ts)

    ## If preheating... Preheater outlets (cold and hot streams)
    # it is asnp.sumed that TCO preheater = TSAT
    if PC_n_coldPH != 0:                        #cold preheating

        for i in range(1,PC_n_coldPH+1):
    # Hot stream outlet from open preheater (saturated)

            PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1)-1,4] = 0
            if PC_st[(LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1))-1,1]== float('inf'):
                PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1)-1,:] = [float('NaN'),float('inf'),float('NaN'), float('NaN'), 0, float('NaN'), float('NaN'), 0, float('NaN')]

            else:
                HotOutletPH_point= IAPWS97(P=PC_st[(LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1))-1,1] /10, x= PC_st[(LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1))-1,4])
                PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1)-1,:] = [HotOutletPH_point.T-273.15,HotOutletPH_point.P*10,HotOutletPH_point.h, HotOutletPH_point.s, HotOutletPH_point.x, HotOutletPH_point.v, HotOutletPH_point.u, 0, HotOutletPH_point.cp0]

    # Cold stream outlet from open PH-state: COLDout = HOTout-TTD
            PC_st[DEAin_n_st - 2*(i-1)-1,0] = PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1)-1,0] - PC_TTDcoldPH
            if PC_st[DEAin_n_st - 2*(i-1)-1,1]== float('inf'):
                PC_st[DEAin_n_st - 2*(i-1)-1,:]= [float('NaN'),float('inf'),float('NaN'), float('NaN'), 1, float('NaN'), float('NaN'), 0, float('NaN')]

            else:
                ColdOutletPH_point= IAPWS97(P= PC_st[DEAin_n_st - 2*(i-1)-1,1]/10, T= PC_st[DEAin_n_st - 2*(i-1)-1,0]+273.15)
                PC_st[DEAin_n_st - 2*(i-1)-1,:] = [ColdOutletPH_point.T-273.15,ColdOutletPH_point.P*10,ColdOutletPH_point.h, ColdOutletPH_point.s, ColdOutletPH_point.x, ColdOutletPH_point.v, ColdOutletPH_point.u, 0, ColdOutletPH_point.cp0]

    if PC_n_hotPH != 0:                         # hot preheating
        for i in range (1,PC_n_hotPH+1):
            # Hot stream outlet from open preheater (saturated)
            PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1)-1,4] = 0
            HotOutletHotPH_point= IAPWS97(P=PC_st[(LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1))-1,1] /10, x= PC_st[(LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1))-1,4])
            PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1)-1,:] = [HotOutletHotPH_point.T-273.15,HotOutletHotPH_point.P*10,HotOutletHotPH_point.h, HotOutletHotPH_point.s, HotOutletHotPH_point.x, HotOutletHotPH_point.v, HotOutletHotPH_point.u, 0, HotOutletHotPH_point.cp0]

            # Cold stream outlet from open preheater - state:
            PC_st[PUMP2out_n_st + 2*PC_n_hotPH - 2*(i-1)-1,0] = PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1)-1,0] - PC_TTDhotPH
            ColdOutletHotPH_point= IAPWS97(P= PC_st[PUMP2out_n_st + 2*PC_n_hotPH - 2*(i-1)-1,1]/10, T= PC_st[PUMP2out_n_st + 2*PC_n_hotPH - 2*(i-1)-1,0]+273.15)
            PC_st[PUMP2out_n_st + 2*PC_n_hotPH - 2*(i-1)-1,:] = [ColdOutletHotPH_point.T-273.15,ColdOutletHotPH_point.P*10,ColdOutletHotPH_point.h, ColdOutletHotPH_point.s, ColdOutletHotPH_point.x, ColdOutletHotPH_point.v, ColdOutletHotPH_point.u, PC_mdot, ColdOutletHotPH_point.cp0]

    if PC_BackPrValve == 1:                          #if the live steam extraction line exists, I have to define the stage in which the extr steam mixes with the main flow and in the nominal case I consider that the extr line is not working so 13=14
        PC_st[PUMP2out_n_st + 2*PC_n_hotPH + PC_BackPrValve-1,:] = PC_st[PUMP2out_n_st + 2*PC_n_hotPH + PC_BackPrValve-1,:]

    if PC_BoilerValve == 1:                                              #isoenthalpic lamination

        PC_st[(PUMP2out_n_st+2*PC_n_hotPH+PC_BackPrValve+PC_BoilerValve)-1,2]=PC_st[(PUMP2out_n_st+2*PC_n_hotPH+PC_BackPrValve)-1,2]
        BoilerInlet_point= IAPWS97(P=PC_st[(PUMP2out_n_st+2*PC_n_hotPH+PC_BoilerValve)-1,1]/10, h= PC_st[(PUMP2out_n_st+2*PC_n_hotPH+PC_BoilerValve)-1,2])
        # To overcome any errors with zero values for enthalpy and pressure in row 14, to be checked later --> Osama
        if PC_st[(PUMP2out_n_st+2*PC_n_hotPH+PC_BoilerValve)-1,1]==0 and PC_st[(PUMP2out_n_st+2*PC_n_hotPH+PC_BoilerValve)-1,2]==0:
            PC_st[(PUMP2out_n_st+2*PC_n_hotPH+PC_BoilerValve)-1,:] =[0,0,0,0,1,0,0,PC_mdot,0]

        else:
            PC_st[(PUMP2out_n_st+2*PC_n_hotPH+PC_BoilerValve)-1,:] = [BoilerInlet_point.T-273.15,BoilerInlet_point.P*10,BoilerInlet_point.h, BoilerInlet_point.s, BoilerInlet_point.x, BoilerInlet_point.v, BoilerInlet_point.u, PC_mdot, BoilerInlet_point.cp0]

    if PC_DoubleCond == 1 and PC_ValveCond_2 == 1:                      #isoenthalpic lamination: h2=h3
         PC_st[(1+PC_DoubleCond+PC_ValveCond_2)-1,2] = PC_st[(1+PC_DoubleCond)-1,2]
         if PC_st[(1+PC_DoubleCond+PC_ValveCond_2)-1,1]==0:
             PC_st[(1+PC_DoubleCond+PC_ValveCond_2)-1,:]=[float('NaN'), PC_st[(1+PC_DoubleCond+PC_ValveCond_2)-1,1]/10,PC_st[(1+PC_DoubleCond+PC_ValveCond_2)-1,2],float('NaN'),1,float('NaN'),float('NaN'),0,float('NaN')]
         else:
             Row3_point= IAPWS97(P=PC_st[(1+PC_DoubleCond+PC_ValveCond_2)-1,1]/10, h= PC_st[(1+PC_DoubleCond+PC_ValveCond_2)-1,2])
             PC_st[(1+PC_DoubleCond+PC_ValveCond_2)-1,:] = [Row3_point.T-273.15,Row3_point.P*10,Row3_point.h, Row3_point.s, Row3_point.x, Row3_point.v, Row3_point.u, 0, Row3_point.cp0]

    ## If preheating... Subcooler outlets

    #Here you define the hot side outlets of the SC by mean of TTD by design
    # SC_hot_out = SC_cold_in + TTD
    if PC_n_coldPH != 0:                         #cold preheating
        for i in range (1,PC_n_coldPH+1):
            # states in SC:
            PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,0] = PC_st[DEAin_n_st - 2*(i-1)-3,0]+PC_TTDcold #hot side outlet temperature SC
            if PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,1]== float('inf'):
                PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,:]= [float('inf'),float('inf'),float('NaN'),float('NaN'),1,float('NaN'),float('NaN'),0,float('NaN')]
            else:
                SubCoolerColdPH_point= IAPWS97(P=PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,1] /10, T= PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,0]+273.15)
                PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,:] = [SubCoolerColdPH_point.T-273.15,SubCoolerColdPH_point.P*10,SubCoolerColdPH_point.h, SubCoolerColdPH_point.s, SubCoolerColdPH_point.x, SubCoolerColdPH_point.v, SubCoolerColdPH_point.u, 0, SubCoolerColdPH_point.cp0]    #other conditions at hot side outlet SC

    if PC_n_hotPH != 0:                      # hot preheating - similar to before
        for i in range (1,PC_n_hotPH+1):

            PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,0] = PC_st[PUMP2out_n_st + 2*PC_n_hotPH - 2*(i-1)-2-1,0]+PC_TTDhot
            if np.isnan(PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,0])== True:
                PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,:]= [float('NaN'),PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,1],float('NaN'),float('NaN'),1,float('NaN'),float('NaN'),0,float('NaN') ]

            else:
                SubCoolerHotPH_point= IAPWS97(P=PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,1] /10, T= PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,0]+273.15)
                PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,:]= [SubCoolerHotPH_point.T-273.15,SubCoolerHotPH_point.P*10,SubCoolerHotPH_point.h, SubCoolerHotPH_point.s, SubCoolerHotPH_point.x, SubCoolerHotPH_point.v, SubCoolerHotPH_point.u, 0, SubCoolerHotPH_point.cp0]    #other conditions at hot side outlet SC

    ##THIS PART IS KEPT COMMENTED AS IT WAS FROM THE MATLAB SOURCE WITHOUT MODIFICATION
    ##STATES FOR VATTENFALL: BACKPRESSURE LINE (39,40,42); DeaLP inlet mf
    #
    #     if PC_BackPrValve == 1
    #         #39
    #         PC_st((LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + ...
    #             PC_DoubleCond + 2*(PC_n_hotPH + PC_n_coldPH) + PC_BackPrValve),:) = PC_st(HPTin_n_st,:);
    #         #40
    #         PC_st((LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + ...
    #             PC_DoubleCond + 2*(PC_n_hotPH + PC_n_coldPH) + 2*PC_BackPrValve),3) = ...
    #             PC_st((LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + ...
    #             PC_DoubleCond + 2*(PC_n_hotPH + PC_n_coldPH) + PC_BackPrValve),3);   #isoenthalpic lamination through the backpressure valve (h39 = h40)
    #
    # #         PC_st((LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + ...
    # #             PC_DoubleCond + 2*(PC_n_hotPH + PC_n_coldPH) + 2*PC_BackPrValve),:) = hP(...
    # #             PC_st((LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + ...
    # #             PC_DoubleCond + 2*(PC_n_hotPH + PC_n_coldPH) + 2*PC_BackPrValve),3),...
    # #             PC_st((LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + ...
    # #             PC_DoubleCond + 2*(PC_n_hotPH + PC_n_coldPH) + 2*PC_BackPrValve),2),...
    # #             PC_st((LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + ...
    # #             PC_DoubleCond + 2*(PC_n_hotPH + PC_n_coldPH) + 2*PC_BackPrValve),8)); #in realtà p40 non la conosco quindi qui non calcola
    #
    #         #41
    #         PC_st((LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + ...
    #             PC_DoubleCond + 2*(PC_n_hotPH + PC_n_coldPH) + 2*PC_BackPrValve + PC_LPextr),:) = PC_st(IPTin_n_st,:);
    #
    #         #42: per ora conosco solo la Pressione imposta da me
    #     end
    #     #p40 NON LA SAPRò MAI; CALCOLERò h40 =h39; h41 DA
    #     #T,p CHE SONO NOTE PERCHè UGUALI A IPT CONDITIONS E h42 COME BILANCIO
    #     #ENTALPICO DEI FLUSSI 40 E 41

    ## Final Mass flow balance and turbine stage calculations at Hot Preheating

    #check quali sono initial guess!!!!!!!!

    # if PC_BackPrValve == 1
    #
    # PC_st(HPTin_n_st,8) = PC_mdot - PC_st((LPTout_n_st+3*PC_n_hotPH+1+3*PC_n_coldPH+PC_DeaLP+PC_DoubleCond+PC_BackPrValve),8);
    #
    # PC_st((LPTout_n_st+3*PC_n_hotPH+1+3*PC_n_coldPH+PC_DeaLP+PC_DoubleCond+PC_BackPrValve),8) = 0; !!!!! BackPressure line non usata in nominal conditions
    #
    # end

    #creo un vettore con le perdite di carico lungo le linee di estrazione
    PC_ExtrLineHot_dp = [PC_HotExtr_dp, PC_DeaHPextr_dp]


    n = 0
    jj=1
    PC_HPT_ETA   = np.zeros(shape=(1,2))
    PC_HPT_W     = np.zeros(shape=(1,2))

    for i in range (1,max(1,PC_n_hotPH*2)+2*PC_DeaLocatHP+1,2):

        [state,ETA,W] = STurb(PC_st[HPTin_n_st+(i-1)-1,0],PC_st[HPTin_n_st+(i-1)-1,1],PC_st[HPTin_n_st+(i-1)-1,7],PC_HPT_pr[jj-1],n) #You evaluate stage by stage the HPT conditions
        jj=jj+1
        PC_st[HPTin_n_st+i-1,:] = state[1,:]

        n = n+1
        PC_HPT_ETA[0,n-1] = ETA
        PC_HPT_W[0,n-1]  = W


        if PC_n_hotPH != 0:
            PC_st[HPTin_n_st+(i+1)-1,:] = PC_st[HPTin_n_st+i-1,:]                               # FR is unknown at this point - here you go to the main exit from the turbine stage you are considering
            PC_st[LPTout_n_st+(n)-1,0]  = PC_st[HPTin_n_st+i-1,0]                                  # FR is unknown at this point - here you go to the extraction exit from the turbine stage you are considering
            PC_st[LPTout_n_st+(n)-1,2:]  = PC_st[HPTin_n_st+i-1,2:]
            PC_st[LPTout_n_st+(n)-1,1] = (1-PC_ExtrLineHot_dp[n-1])*PC_st[HPTin_n_st+i-1,1]  # l'extraction line ha tutto uguale all'uscita della turbina eccetto la pressione per via della perdita di carico

            if n == 1: #Concerning the first stage of the HPT
                PC_st[LPTout_n_st+(n)-1,7] = PC_st[PUMP2out_n_st-1,7]*(PC_st[PUMP2out_n_st + 2*PC_n_hotPH - i + 1-1,2] - PC_st[PUMP2out_n_st + 2*PC_n_hotPH - (i+2) + 1-1,2])/(PC_st[LPTout_n_st+(n)-1,2] - PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n)-1,2]) # evaluate the extraction mass flow rate
                PC_st[HPTin_n_st+(i+1)-1,7] = PC_st[HPTin_n_st+i-1,7] - PC_st[LPTout_n_st+(n)-1,7]                                           # evaluate the mass flow rate which continues through the stages
                PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n) - 1-1,7] = PC_st[LPTout_n_st+(n)-1,7]    # fix the mass flow rate also in hot inlet SC1
                PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n)-1,7] = PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n) - 1-1,7] # fix the mass flow rate also in hot outlet SC1

            else: #Concerning the further stages of the HPT (the balance for the extraction calculation is more elaborated)

                if PC_n_hotPH == n:
                    PC_st[LPTout_n_st+(n)-1,7] = (PC_st[PUMP2out_n_st-1,7]*(PC_st[PUMP2out_n_st + 2*PC_n_hotPH - i + 1-1,2] - PC_st[PUMP2out_n_st + 2*PC_n_hotPH - (i+2) + 1-1,2]) - PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*(n-1))-1,7]*(PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*(n-1))-1,2] - PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n)-1,2]))/(PC_st[LPTout_n_st+(n)-1,2] - PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n)-1,2]) # evaluate the extraction mass flow rate

                    PC_st[HPTin_n_st+(i+1)-1,7] = PC_st[HPTin_n_st+i-1,7] - PC_st[LPTout_n_st+(n)-1,7]
                    PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n) - 1-1,7] = PC_st[LPTout_n_st+(n)-1,7] +  PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*(n-1))-1,7] #from PH to SC
                    PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n)-1,7] = PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n) - 1-1,7]          #out SC

                elif PC_DeaLocatHP == 1:
                #balance to find extraction to DeaHP

                    PC_st[(LPTout_n_st + PC_n_hotPH + PC_DeaLocatHP)-1,7]= (PC_st[(DEAin_n_st+1)-1,7]*PC_st[DEAin_n_st+1-1,2] -PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond-1,7]*PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond -1,2] -PC_st[IPTin_n_st-PC_RHpresence-1-1,7]*PC_st[DEAin_n_st-1,2])/(PC_st[LPTout_n_st + PC_n_hotPH + PC_DeaLocatHP-1,2] - PC_st[DEAin_n_st-1,2])
                    PC_IPT_ETA = 0
                    PC_IPT_W   = 0

                    PC_st[HPTin_n_st+(i+1)-1,7] = PC_st[HPTin_n_st+i-1,7] - PC_st[LPTout_n_st+(n)-1,7]


        elif PC_n_hotPH == 0:
            if PC_DeaLocatHP == 1:

                PC_st[(LPTout_n_st + PC_n_hotPH + PC_DeaLocatHP)-1,7]= (PC_st[(DEAin_n_st+1)-1,7]*PC_st[DEAin_n_st+1-1,2] - PC_st[IPTin_n_st-PC_RHpresence-1-1,7]*PC_st[DEAin_n_st-1,2])/(PC_st[LPTout_n_st + PC_n_hotPH + PC_DeaLocatHP-1,2] - PC_st[DEAin_n_st-1,2])
                PC_st[HPTin_n_st+(i+1)-1,7] = PC_st[HPTin_n_st+i-1,7] - PC_st[LPTout_n_st+(n)-1,7]


    n=0
    for i in range (1, max(1,PC_n_hotPH*2), 2):
        n=n+1
        if np.isnan(PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n) - 1-1,7]) == True:
            PC_st[PUMP2out_n_st + 2*PC_n_hotPH - i-1,2] = float('NaN')
            ColdInletPHhot_point= IAPWS97(P=PC_st[PUMP2out_n_st + 2*PC_n_hotPH - i-1,1]/10, x= 1)         # No clue why was the process rerouted to calculate at saturated liquid through the steam function in matlab, however calculated here through IAPWS with P and X =1
            PC_st[PUMP2out_n_st + 2*PC_n_hotPH - i-1,:] = [ColdInletPHhot_point.T-273.15,ColdInletPHhot_point.P*10,float('NaN'), ColdInletPHhot_point.s, ColdInletPHhot_point.x, ColdInletPHhot_point.v, float('NaN'), PC_st[PUMP2out_n_st + 2*PC_n_hotPH - i-1,7], ColdInletPHhot_point.cp0]   # other properties for cold inlet to PHshot

        else:
            PC_st[PUMP2out_n_st + 2*PC_n_hotPH - i-1,2] = PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n) - 1-1,7]*(PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n) - 1-1,2] - PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n)-1,2])/PC_st[PUMP2out_n_st-1,7] + PC_st[PUMP2out_n_st + 2*PC_n_hotPH - (i+2) + 1-1,2]      #mass balance for cold inlet to PHshot

            ColdInletPHhot_point= IAPWS97(P=PC_st[PUMP2out_n_st + 2*PC_n_hotPH - i-1,1]/10, h= PC_st[PUMP2out_n_st + 2*PC_n_hotPH - i-1,2])         # No clue why was the process rerouted to calculate at saturated liquid through the steam function in matlab, however calculated here through IAPWS with P and X =1
            PC_st[PUMP2out_n_st + 2*PC_n_hotPH - i-1,:] = [ColdInletPHhot_point.T-273.15,ColdInletPHhot_point.P*10,ColdInletPHhot_point.h, ColdInletPHhot_point.s, ColdInletPHhot_point.x, ColdInletPHhot_point.v, ColdInletPHhot_point.u, PC_st[PUMP2out_n_st + 2*PC_n_hotPH - i-1,7], ColdInletPHhot_point.cp0]   # other properties for cold inlet to PHshot

    ## Mass flow balance on Reheater, IPT and deaerator:
    if PC_RHpresence == 1:
        PC_st[IPTin_n_st-1,7]=PC_st[IPTin_n_st-PC_RHpresence-1,7]

    PC_st[IPTin_n_st-1,7] = (1-0.04)*PC_st[IPTin_n_st-1,7]

    #per i casi con DeaLocatHP IPTin coincide con LPTin

    if PC_DeaLocatHP == 0: #così esiste IPT stage

        [state,ETA,W] = STurb(PC_st[IPTin_n_st-1,0],PC_st[IPTin_n_st-1,1],PC_st[IPTin_n_st-1,7],PC_IPT_PR,n)  #You evaluate the conditions thorugh the IPT stage
        PC_st[(IPTin_n_st+1)-1,:] = state[1,:]
        PC_IPT_ETA = ETA
        PC_IPT_W = W
        PC_st[LPTout_n_st + PC_n_hotPH + 1-1,:] = PC_st[IPTin_n_st+1-1,:]  # Extraction line to Deaerator - mass flow is unknown at this point

        if PC_n_hotPH > 0:                  #If you  have hot pre-heating
            PC_st[LPTout_n_st + PC_n_hotPH + 1-1,7] = (PC_st[DEAin_n_st+1-1,7]*PC_st[DEAin_n_st+1-1,2] - PC_st[(LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond)-1,7]*PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond-1,2] -PC_st[IPTin_n_st+1-1,7]*PC_st[DEAin_n_st-1,2])/(PC_st[LPTout_n_st + PC_n_hotPH + 1-1,2] - PC_st[DEAin_n_st-1,2]) #Balance to find out the mass flow rate extraction to Dea
        else:
            PC_st[LPTout_n_st + PC_n_hotPH + 1-1,7] = (PC_st[DEAin_n_st+1-1,7]*PC_st[DEAin_n_st+1-1,2] - PC_st[IPTin_n_st+1-1,7]*PC_st[DEAin_n_st-1,2])/(PC_st[LPTout_n_st + PC_n_hotPH + 1-1,2] - PC_st[DEAin_n_st-1,2])

        PC_st[LPTin_n_st-1,:] = PC_st[LPTin_n_st - 1-1,:]            #Conditions at LPT inlet
        PC_st[LPTin_n_st-1,7] = PC_st[IPTin_n_st+1-1,7] - PC_st[LPTout_n_st + PC_n_hotPH + 1-1,7]    #Mass flow rate at LPT inlet as difference between previous and Dea extraction

    ## Final Mass flow balance and turbine stage calculations at Cold Preheating
    for i in range((1 + PC_DoubleCond + PC_ValveCond_2 + PC_PumpBeforeMix + PC_DoubleCond + PC_DeaLP),(DEAin_n_st)+1,1):

        PC_st[i-1,7] = PC_st[LPTin_n_st-1,7]

    PC_ExtrLineCold_dp = [PC_ColdExtr_dp, PC_DeaLPextr_dp]

    n = 0
    jj= 1
    PC_LPT_ETA   = np.zeros(shape=(1,3))
    PC_LPT_W     = np.zeros(shape=(1,3))
    for i in range (1,(PC_n_coldPH*2)+1,2):

        [state,ETA,W] = STurb(PC_st[LPTin_n_st+(i-1)-1,0],PC_st[LPTin_n_st+(i-1)-1,1],PC_st[LPTin_n_st+(i-1)-1,7],PC_LPT_pr[jj-1],n)     #Conditions stage by stage in LPT
        jj=jj+1
        PC_st[LPTin_n_st+i-1,:] = state[1,:]
        n = n+1
        PC_LPT_ETA[0,n-1] = ETA

        PC_LPT_W[0,n-1] = W

        if PC_n_coldPH != 0:
            PC_st[LPTin_n_st+(i+1)-1,:] = PC_st[LPTin_n_st+i-1,:]                           # FR is unknown at this point - Equal conditions in the line which continues to the next stage
            PC_st[LPTout_n_st+ PC_n_hotPH + 1 + (n)-1,0]  = PC_st[LPTin_n_st+i-1,0]         # FR is unknown at this point - Equal conditions in the line which is the extraction
            PC_st[LPTout_n_st+ PC_n_hotPH + 1 + (n)-1,2:] = PC_st[LPTin_n_st+i-1,2:]        # FR is unknown at this point - Equal conditions in the line which is the extraction
            PC_st[LPTout_n_st+ PC_n_hotPH + 1 + (n)-1,1] = (1-float(str(PC_ExtrLineCold_dp[n-1])[1:5]))*PC_st[LPTin_n_st+i-1,1]           # to get a float instead of list, to be optimized later --> Osama

            if n == 1:
                PC_st[LPTout_n_st+ PC_n_hotPH + 1 + (n)-1,7] = PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)+PC_DeaLP)-1,7]*(PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)+2*PC_DeaLP + 2*PC_n_coldPH - i + 1)-1,2] -PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)+2*PC_DeaLP + 2*PC_n_coldPH - (i+2) + 1)-1,2])/(PC_st[LPTout_n_st+ PC_n_hotPH + 1 + (n)-1,2] - PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n)-1,2])            #Balance to find out the mass flow rate into the extraction line from the first stage of LPT
                PC_st[LPTin_n_st+(i+1)-1,7] = PC_st[LPTin_n_st+i-1,7] - PC_st[LPTout_n_st+ PC_n_hotPH + 1 + (n)-1,7]                                             #Difference to find out the mass flow rate which continues to next stages
                PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n) - 1-1,7] = PC_st[LPTout_n_st+ PC_n_hotPH + 1 + (n)-1,7]    #The same mass flow rate  goes into the PH on the hot side
                PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n)-1,7] = PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n) - 1-1,7]      #The same mass flow rate  goes into the SC on the hot side

            else:
                PC_st[LPTout_n_st+ PC_n_hotPH + 1 + (n)-1,7] = (PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+PC_DeaLP)-1,7]*(PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)+2*PC_DeaLP + 2*PC_n_coldPH - i + 1-1,2] - PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)+2*PC_DeaLP + 2*PC_n_coldPH - (i+2) + 1-1,2]) - PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*(n-1))-1,7]*(PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*(n-1))-1,2] -  PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n)-1,2]))/(PC_st[LPTout_n_st+ PC_n_hotPH + 1 + (n)-1,2] - PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n)-1,2])     #Balance to find out the mass flow rate into the extraction line from the later stages of LPT

                PC_st[LPTin_n_st+(i+1)-1,7] = PC_st[LPTin_n_st+i-1,7] - PC_st[LPTout_n_st+ PC_n_hotPH + 1 + (n)-1,7]            #Difference to find out the mass flow rate which continues to next stages
                PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n) - 1-1,7] = PC_st[LPTout_n_st+ PC_n_hotPH + 1 + (n)-1,7] + PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*(n-1))-1,7]                  #Balance to find out the mass flow rate  which goes into the PH on the hot side
                PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n)-1,7] = PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n) - 1-1,7]         #The same mass flow rate  goes into the SC on the hot side


            PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)+2*PC_DeaLP + 2*PC_n_coldPH - i-1,2] = PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n) - 1-1,7]*(PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n) - 1-1,2] - PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*n)-1,2])/PC_st[1 + PC_DoubleCond + PC_ValveCond_2 + PC_PumpBeforeMix + PC_DoubleCond + PC_DeaLP-1,7] +  PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)+2*PC_DeaLP + 2*PC_n_coldPH - (i+2) + 1-1,2] #Balance to find out the enthalpy at the outlet of SC cold side

            Cold_Preheating_point= IAPWS97(P=PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)+2*PC_DeaLP + 2*PC_n_coldPH - i-1,1]/10, h= PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)+2*PC_DeaLP + 2*PC_n_coldPH - i-1,2])
            PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)+2*PC_DeaLP + 2*PC_n_coldPH - i-1,:] = [Cold_Preheating_point.T-273.15,Cold_Preheating_point.P*10,Cold_Preheating_point.h, Cold_Preheating_point.s, Cold_Preheating_point.x, Cold_Preheating_point.v, Cold_Preheating_point.u, PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)+2*PC_DeaLP + 2*PC_n_coldPH - i-1,7], Cold_Preheating_point.cp0]

    if PC_DoubleCond == 0:
        n = n+1

        [state,ETA,W] = STurb(PC_st[LPTout_n_st-1-1,0],PC_st[LPTout_n_st-1-1,1],PC_st[LPTout_n_st-1-1,7],PC_LPT_pr[-1],n) #Conditions through the last stage of the LPT
        PC_st[LPTout_n_st-1,:] = state[2-1,:]
        PC_LPT_ETA[0,n-1]= ETA

        PC_LPT_W[0,n-1]  = W


    #Here the basic Rankine cycle is completely defined
    elif PC_DoubleCond == 1:

        n = n+1
        PC_LPT_DC_pr    = np.zeros(shape=(1,2))
        PC_LPT_DC_pr[0,0] = PC_st[LPTin_n_st+2*PC_n_coldPH-1,1]/PC_st[LPTout_n_st-2-PC_DeaLP-1,1]
        PC_LPT_DC_pr[0,1] = PC_st[LPTout_n_st-1-1,1]/PC_st[LPTout_n_st-1,1]

        [state,ETA,W]    = STurb(PC_st[LPTin_n_st+2*PC_n_coldPH-1,0],PC_st[LPTin_n_st+2*PC_n_coldPH-1,1],PC_st[LPTin_n_st+2*PC_n_coldPH-1,7],PC_LPT_DC_pr[0,0],n)
        PC_st[LPTout_n_st-2-PC_DeaLP-1,:] = state[1,:]

        # PC_LPT_ETA       = np.zeros(shape=(1,2))
        PC_LPT_ETA[0,n-1]= ETA
        # PC_LPT_W         = np.zeros(shape=(1,2))
        PC_LPT_W[0,n-1]  = W

        if PC_DeaLP == 1:             #casoVattenfall
            PC_st[LPTout_n_st-1-PC_DeaLP-1,:] = PC_st[LPTout_n_st-2-PC_DeaLP-1,:]            #   FR is unknown at this point - Equal conditions in the line which continues to the next stage
            PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP-1,0]  = PC_st[LPTout_n_st-1-PC_DeaLP-1,0] #   FR is unknown at this point - Equal conditions in the line which is the extraction
            PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP-1,2:]  = PC_st[LPTout_n_st-1-PC_DeaLP-1,2:] #   FR is unknown at this point - Equal conditions in the line which is the extraction
            PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP-1,1] = (1-PC_ExtrLineCold_dp[-1])*PC_st[LPTout_n_st-1-PC_DeaLP-1,1]

            PC_st[LPTout_n_st-1-1,:]=PC_st[LPTout_n_st-1-PC_DeaLP-1,:]                                                #  FR is unknown
            PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,:]=PC_st[LPTout_n_st-1-PC_DeaLP-1,:]  #FR is unknown

            #calculation of M_EXTR TO DEA_LP. For the DeaLP balance I need h5, but it is unknown, so I need a while to find h5 !!!!!
            err     = 1
            toll    = 0.01
    #
            h5 = PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond-1,2]

            while err >= toll:
                PC_st[LPTout_n_st+ PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP-1,7] = (PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+PC_DeaLP-1,7]*PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+PC_DeaLP-1,2]-PC_st[LPTout_n_st+3*PC_n_hotPH+1+3*PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,7]*PC_st[LPTout_n_st+3*PC_n_hotPH+1+3*PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,2]-PC_st[LPTin_n_st+2*PC_n_coldPH+1-1,7]*h5)/(PC_st[LPTout_n_st+ PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP-1,2]-h5)  #m_extrDeaLP

                PC_st[LPTout_n_st-1-PC_DeaLP-1,7] = PC_st[LPTout_n_st-2-PC_DeaLP-1,7]-PC_st[LPTout_n_st+ PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP-1,7]

    #                 #mass flow rate in the HTcondenser is given by the balance which
    #                 #includes the heat demand, knowing condenser parameters
    #                 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
                PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,7] = (PC_DH_massflow*4.186*(PC_DH_T_supply-PC_DH_T_return-APPROACH_COND1))/(PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,2]-PC_st[1+PC_DoubleCond-1,2])

                PC_st[1+PC_DoubleCond-1,7]=PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,7]

                if PC_ValveCond_2 == 1:
                    PC_st[1+PC_DoubleCond+PC_ValveCond_2-1,7]=PC_st[1+PC_DoubleCond-1,7]     #m2=m3

                PC_st[LPTout_n_st-1-1,7]=PC_st[LPTout_n_st-1-PC_DeaLP-1,7]-PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,7]

                PC_st[LPTout_n_st-1,7]=PC_st[LPTout_n_st-1-1,7]
                PC_st[0,7]            =PC_st[LPTout_n_st-1,7]                   #1

                if PC_PumpBeforeMix == 1:
                    PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix-1,7]=PC_st[LPTout_n_st-1,7]      #4

    # #                 PC_st((LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + 2*(PC_n_hotPH + PC_n_coldPH) + 2*PC_BackPrValve),8)=...
    # #                     PC_st((LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + 2*(PC_n_hotPH + PC_n_coldPH) + PC_BackPrValve),8);41=40
    # #
    # #                 PC_st((LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + 2*(PC_n_hotPH + PC_n_coldPH) + 3*PC_BackPrValve),8)=...
    # #                     PC_st((LPTout_n_st + PC_n_hotPH + 1 +PC_n_coldPH + PC_DeaLP + PC_DoubleCond +2*(PC_n_hotPH + PC_n_coldPH) +PC_BackPrValve),8);42=41
    # #
    # #                 h41=h40 ecc ecc
    #
    #
                PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond)-1,7] = PC_st[1,7]+PC_st[(1+PC_DoubleCond)-1,7]

                h5_new = (PC_st[1+PC_DoubleCond+PC_ValveCond_2-1,7]*PC_st[1+PC_DoubleCond+PC_ValveCond_2-1,2] + PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix-(1-PC_PumpBeforeMix)-1,7]*PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix-(1-PC_PumpBeforeMix))-1,2]) / PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond)-1,7]          #h5

                err = abs(h5_new - h5)
                h5  = h5_new

                PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond-1,2] = h5_new

                if np.isnan(PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond)-1,2]) == True:
                    Thermo5_point = IAPWS97(P=PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond)-1,1]/10, x=1)           # To function as steam PROP function in matlab , asnp.suming saturated status
                    PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond)-1,:] = [Thermo5_point.T-273.15,Thermo5_point.P*10,float('NaN'), Thermo5_point.s, Thermo5_point.x, Thermo5_point.v, float('NaN'), PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond)-1,7], Thermo5_point.cp0]          #prop5

                else:
                    Thermo5_point = IAPWS97(P=PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond)-1,1]/10, h=PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond)-1,2])
                    PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond)-1,:] = [Thermo5_point.T-273.15,Thermo5_point.P*10,Thermo5_point.h, Thermo5_point.s, Thermo5_point.x, Thermo5_point.v, Thermo5_point.u, PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond)-1,7], Thermo5_point.cp0]          #prop5

    #
        elif PC_DeaLP == 0:          #casoDC   # CASE WAS NOT POSSIBLE TO CHECK, MATLAB MODEL DOES NOT WORK
           #TO BE ADJUSTED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            PC_st[LPTout_n_st-1-1,:]=PC_st[LPTout_n_st-2-1,:]                   #30come29 FR is unknown
            PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,:]=PC_st[LPTout_n_st-2-1,:]      #37come29 FR is unknown

            #mass flow rate in the HTcondenser is given by the balance which
            #includes the heat demand, knowing condenser parameters
    #
            PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,7] = (PC_DH_massflow*4.186*(PC_DH_T_supply-PC_DH_T_return-APPROACH_COND1)- PC_st[LPTout_n_st+3*PC_n_hotPH+1+3*PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,7]*(PC_st[LPTout_n_st+3*PC_n_hotPH+1+3*PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,2]-PC_st[1+PC_DoubleCond-1,2]))/(PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,2]-PC_st[1+PC_DoubleCond-1,2])       #m37
    #
            PC_st[1+PC_DoubleCond-1,7]=PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,7]+PC_st[LPTout_n_st+3*PC_n_hotPH+1+3*PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,7]     #m2=m37+m45
    #
            PC_st[LPTout_n_st-1-1,7]  =PC_st[LPTout_n_st-2-1,7]-PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,7]         #30
            PC_st[LPTout_n_st-1,7]    =PC_st[LPTout_n_st-1-1,7]           #31
            PC_st[0,7]                =PC_st[LPTout_n_st-1,7]        #1


        [state,ETA,W] = STurb(PC_st[LPTout_n_st-1-1,0],PC_st[LPTout_n_st-1-1,1],PC_st[LPTout_n_st-1-1,7],PC_LPT_DC_pr[0,1], n)    #Condions through the last stage of the LPT
        PC_st[LPTout_n_st-1,:] = state[2-1,:]
        # PC_LPT_ETA   = np.zeros(shape=(1,2))
        PC_LPT_ETA[0,n]= ETA
        # PC_LPT_W     = np.zeros(shape=(1,2))
        PC_LPT_W[0,n]  = W

    ## Preparing calculations for HTF cycle... #From DSG point of view, these are the Qin from which you later need to evaluate Qabs in DSGreceicer function
    PC_SH_mcold   = PC_st[HPTin_n_st-PC_BackPrValve-1,7]                                                             # Mass flow rate into the boiler is the same of the one at the inlet of HPT
    PC_SH_Q       = PC_SH_mcold*(PC_st[HPTin_n_st-PC_BackPrValve-1,2] - PC_st[HPTin_n_st-PC_BackPrValve-1-1,2])      # Heat power exchanged into the HX

    PC_EV_mcold   = PC_SH_mcold
    PC_EV_Q       = PC_EV_mcold*(PC_st[HPTin_n_st-PC_BackPrValve-1-1,2] - PC_st[HPTin_n_st-PC_BackPrValve-2-1,2])

    if PC_BoilerMode > 0:
        PC_ECO_mcold  = PC_EV_mcold
        PC_ECO_Q      = PC_ECO_mcold*(PC_st[HPTin_n_st-PC_BackPrValve-2-1,2] - PC_st[HPTin_n_st-PC_BackPrValve-3-1,2])

    else:
        PC_ECO_Q = 0

    if PC_RHpresence == 1:
        PC_RH_mcold   = PC_st[IPTin_n_st-1,7]                                                                         #Mass flow rate into the RH is the same of the one at the inlet of IPT
        PC_RH_Q       = PC_RH_mcold*(PC_st[IPTin_n_st-1,2] - PC_st[IPTin_n_st-PC_RHpresence-1,2])
    else:
        PC_RH_Q = 0
		
    mdotFG = 51
    cpFG = 1.3

    TinFG = 1800
    ToutFG_ev = TinFG - PC_EV_Q/cpFG/mdotFG
    ToutFG_sh = ToutFG_ev - PC_SH_Q/cpFG/mdotFG    
    ToutFG_ec = ToutFG_sh - PC_ECO_Q/cpFG/mdotFG	
    print("PC_SH_Q", PC_SH_Q)	
    print("PC_EV_Q", PC_EV_Q)
    print("ToutFG_sh",ToutFG_sh)
    print("ToutFG_ev",ToutFG_ev)
    print("ToutFG_ec",ToutFG_ec)

    FlueGasIN_ECO = [ToutFG_sh,cpFG,0,mdotFG] # T, cp, ..., mdot
    FlueGasIN_EV = [TinFG,cpFG,0,mdotFG]
    FlueGasOUT_EV = [ToutFG_ev,cpFG,0,mdotFG]
    FlueGasIN_SH = [ToutFG_ev,cpFG,0,mdotFG]

    ## Condenser calculations..
    #Condenser sizing & connp.sumption (fan and pump)
    if PC_PCONDset != 3:
        PC_COND_air_Cp    = 1                                                           # kJ/KgK
        PC_COND_air_R     = 0.287                                                       # kJ/KgK
        PC_COND_cnd_hin   = PC_st[PC_keyst_LPTout_n_st-1,2]
        PC_COND_cnd_hout  = PC_st[1-1,2]
        PC_COND_cnd_FR    = PC_st[PC_keyst_LPTout_n_st-1,7]
        PC_COND_Q         = PC_COND_cnd_FR*(PC_COND_cnd_hin - PC_COND_cnd_hout)
        PC_COND_air_FR    = PC_COND_Q/(PC_COND_air_Cp*PC_COND_air_dT)
        PC_COND_Eff       = PC_COND_Q/(PC_COND_air_FR*PC_COND_air_Cp*PC_COND_dTapp)     #From Conradie and Kröger 1995
        PC_COND_UA        = - (PC_COND_air_FR*np.log(1-PC_COND_Eff))/PC_COND_air_Cp     #From Conradie and Kröger 1995
        PC_COND_air_v     = PC_COND_air_R*(design_Tdrycond + 273.15)/(design_Pamb*100)  # [m3/kg]
        PC_COND_air_volFR = PC_COND_air_v*PC_COND_air_FR                                # [m3/s]
        PC_COND_fan_Power     = (PC_COND_fan_dP*100)*PC_COND_air_volFR/PC_COND_fan_EFF  # [kW]
        PC_COND_Pump_point    = IAPWS97(P=PC_st[0,1]/10, x= 0 )
        PC_COND_Pump_Power    = (PC_st[1,1] - PC_st[0,1])*100*PC_st[1,7] /((1/PC_COND_Pump_point.v) * PC_COND_Pump_EFF)            # [kW]
    #
        PC_COND_Ereq_design   = PC_COND_fan_Power                                       # This is not evaluated into DSG

    elif PC_PCONDset == 3:
        PC_COND_UA          = 0     ## OSAMA--> to assign a value to return the object
        PC_COND_fan_Power   = 0     ## OSAMA--> to assign a value to return the object
        PC_COND_air_FR      = 0     ## OSAMA--> to assign a value to return the object
        if PC_DoubleCond == 1:
            PC_COND1_Q=PC_st[LPTout_n_st-1,7]*(PC_st[LPTout_n_st-1,2]-PC_st[0,2])

            if PC_BackPrValve == 1:
                PC_CONDbp_Q = PC_st[(LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + 2*(PC_n_hotPH + PC_n_coldPH) + 3*PC_BackPrValve + PC_LPextr)-1,7]*(PC_st[(LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + 2*(PC_n_hotPH + PC_n_coldPH) + 3*PC_BackPrValve + PC_LPextr)-1,2]-PC_st[(LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + 2*(PC_n_hotPH + PC_n_coldPH) + 4*PC_BackPrValve + PC_LPextr)-1,2])
            else:
                PC_CONDbp_Q = 0

            if PC_DeaLP == 1:
                PC_COND2_Q=PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,7]*(PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,2]-PC_st[1+PC_DoubleCond-1,2])     #else....new balance for the second condenser to be implemented

            PC_CONDs_Q = PC_COND1_Q+PC_COND2_Q+PC_CONDbp_Q                   #in teoria uguale a Heat Demand

        if PC_PumpBeforeMix == 0:
            PC_COND_Pump2_point= IAPWS97(P=PC_st[1+2*PC_DoubleCond-1,1]/10, x=0)
            PC_COND_Pump_Power    = (PC_st[2+2*PC_DoubleCond-1,1] - PC_st[1+2*PC_DoubleCond-1,1])*100*PC_st[2+2*PC_DoubleCond-1,7] /((1/PC_COND_Pump2_point.v) * PC_Pump_Eff)      # [kW]

        else:
            PC_PumpBefMix2_point= IAPWS97(P=PC_st[0,1]/10, x=0)
            PC_PumpBefMix_Power    = (PC_st[(1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix)-1,1] - PC_st[0,1])*100*PC_st[0,7] /((1/PC_PumpBefMix2_point.v) * PC_Pump_Eff)           # [kW]
                                                           # To assign the variable 'PC_CONDS_Q' in single condenser case
        PC_COND_Ereq_design   = 0
        #elseif PC_DoubleCond == 0..........


    ## Pump work calculation
    if PC_PumpBeforeMix == 0:
        PC_PUMP_W1 = PC_COND_Pump_Power

    else:
        PC_PUMP_W1 = PC_PumpBefMix_Power

    if PC_DeaLP == 1:
        PUMP_W_DeaLP_point= IAPWS97(P=PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+PC_DeaLP-1,1]/10, x=0)
        PC_PUMP_W_DeaLP = (PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+2*PC_DeaLP-1,1] - PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+PC_DeaLP-1,1])*100*PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+2*PC_DeaLP-1,7] /((1/PUMP_W_DeaLP_point.v) * PC_Pump_Eff)           # [kW]

    PC_PUMP_W2_point= IAPWS97(P= PC_st[DEAin_n_st+1-1,1]/10, x=0)

    PC_PUMP_W2 = (PC_st[DEAin_n_st+2-1,1] - PC_st[DEAin_n_st+1-1,1])*100*PC_st[DEAin_n_st+2-1,7] /((1/PC_PUMP_W2_point.v) * PC_Pump_Eff)     #You asnp.sume that v = 1/1000 m3/kg, you take into account that you have to multiply *10^5(Pa) = 100!! The other /1000 is to go from W to kW

    ###

    if design_HTFloop_set ==1:

        from PPSteadyStateDesign.EEG.EEG1_2  import HTFcycle

    elif design_HTFloop_set == 0:

        HTF = []
    ## Cycle Efficiency and total Power
    PC_Q      = PC_ECO_Q + PC_EV_Q + PC_SH_Q + PC_RH_Q           #Total thermal power required by the Rankine cycle (not LHV)
    PC_HT     = PC_Q
    #PC_W  = np.sum(PC_HPT.W) + PC_IPT.W + np.sum(PC_LPT.W) - PC_PUMP.W1 - PC_PUMP.W2 - PC_PUMP.W_DeaLP - PC_COND.Ereq_design/PC_Gen_Eff;
		
    if design_HTFloop_set == 1:
        HTFpumpFRmax = (PC_Q*field_SM/rec_EFF)/HTF[6,2]/(rec_Tset - HTF[6,1])    #maximum flow rate accepted by the pump
        HTFpumpWmax = HTFpumpFRmax * 9.8 * rec_tower_h / 1e3                     #Maximum pump work on the basis of maxFlowRate and tower high
        PC_W  = np.sum(PC_HPT_W) + PC_IPT_W + np.sum(PC_LPT_W) - PC_COND_Ereq_design/PC_Gen_Eff - PC_PUMP_W1 - PC_PUMP_W2 - PC_PUMP_W_DeaLP - HTFpumpWmax  #Net power from Rankine cycle

    elif design_HTFloop_set == 0:

        PC_W  = np.sum(PC_HPT_W) + PC_IPT_W + np.sum(PC_LPT_W) - PC_PUMP_W1 - PC_PUMP_W2 - PC_PUMP_W_DeaLP - PC_COND_Ereq_design/PC_Gen_Eff

    PC_W_HPT = np.sum(PC_HPT_W)
    # print('PC_W_HPT=  ' +  str(PC_W_HPT))
    PC_W_LPT = np.sum(PC_LPT_W)
    # print('PC_W_LPT=  ' + str(PC_W_LPT)  )
    PC_W_el   = PC_W * PC_Gen_Eff * PC_Mec_Eff
    # print('PC_W_el=  ' + str(PC_W_el)  )
    PC_EFFth  = PC_W/PC_Q
    # print('PC_EFFth=  ' + str(PC_EFFth)  )
    PC_EFFel = PC_W_el/PC_Q
    # print('PC_EFFel=  ' + str(PC_EFFel)  )
    PC_Wgross = np.sum(PC_HPT_W) + PC_IPT_W + np.sum(PC_LPT_W)
    # print('PC_Wgross=  ' + str(PC_Wgross)  )
    PC_Wparas = PC_Wgross - PC_W
    # print('PC_Wparas=  ' + str(PC_Wparas)  )
    PC_Wgross_el = PC_Wgross * PC_Gen_Eff * PC_Mec_Eff
    # print('PC_Wgross_el=  ' + str(PC_Wgross_el)  )
    PC_Wparas_el = PC_Wparas * PC_Gen_Eff * PC_Mec_Eff
    # print('PC_Wparas_el=  ' + str(PC_Wparas_el)  )
    PC_EFFcog = (PC_W_el + PC_CONDs_Q)/PC_Q
    # print('PC_EFFcog=  ' + str(PC_EFFcog)  )

    ## Preparing for TRNSYS gemasolar model STILL DO NOT KNOW WHY THIS COULD BE USEFUL
    PC_turb_desiredSH = PC_st[HPTin_n_st-PC_BackPrValve-1,0] - PC_st[HPTin_n_st-PC_BackPrValve-1-1,0]    #Desired temperature gradient on steam in SH

    if PC_n_coldPH > 0:          #(2)
        PC_coldSC= np.zeros(shape=(PC_n_coldPH,5))
        PC_coldPH= np.zeros(shape=(PC_n_coldPH,4))
        PC_coldSC[PC_n_coldPH-1,4] = 0           #Quality
        PC_coldPH[PC_n_coldPH-1,2] = 0             #Enthalpy

    if PC_n_hotPH > 0:           #(3)
        PC_hotSC= np.zeros(shape=(PC_n_hotPH,5))
        PC_hotPH= np.zeros(shape=(PC_n_hotPH,4))
        PC_hotSC[PC_n_hotPH-1,4]   = 0
        PC_hotPH[PC_n_hotPH-1,2]   = 0

    ## Sizing condensers for CHP (Luis Castillo models)

    if PC_DoubleCond == 0:

        PC_COND_DT_1 = PC_st[LPTout_n_st-1,0] - PC_DH_T_return

        PC_COND_DT_2 = PC_st[0,0] - PC_DH_T_supply

        PC_COND_log_mean_T_cond = (PC_COND_DT1 - PC_COND_DT2)/(np.log(PC_COND_DT1/PC_COND_DT2))

        PC_COND_Area  = (PC_Heat_demand*1000)/(2.2*PC_COND_log_mean_T_cond)

    else:

        PC_COND1_DT1 = PC_st[0,0] - PC_DH_T_return

        PC_COND1_DT2 = PC_st[LPTout_n_st-1,0] - (PC_DH_T_return + APPROACH_COND1)

        PC_COND1_log_mean_T_cond = (PC_COND1_DT1 - PC_COND1_DT2)/(np.log(PC_COND1_DT1/PC_COND1_DT2))

        PC_COND1_Area = (PC_COND1_Q)/(2.2*PC_COND1_log_mean_T_cond)

        PC_COND2_DT1 = PC_st[1+PC_DoubleCond-1,0] - (PC_DH_T_return + APPROACH_COND1)

        PC_COND2_DT2 = PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,0] - PC_DH_T_supply

        PC_COND2_log_mean_T_cond = (PC_COND2_DT1 - PC_COND2_DT2)/(np.log(PC_COND2_DT1/PC_COND2_DT2))

        PC_COND2_Area = (PC_COND2_Q)/(2.2*PC_COND2_log_mean_T_cond)
        # print('PC_COND2_Area= ' + str(PC_COND2_Area))
        PC_COND_Area = 0  # To pass on the variable to PowerBlock
        PC_COND2_DELTA_T_LOG = ((PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,0] - PC_DH_T_supply) - (PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,0]- PC_DH_T_return))/(np.log((PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,0] - PC_DH_T_supply)/(PC_st[LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP+PC_DoubleCond-1,0]- PC_DH_T_return)))

        #Q_COND2 = PC_STATES(o.Stg.FW_HOTin_LPT(LPT_EXT_P),6)*(PC_STATES(o.Stg.FW_HOTin_LPT(LPT_EXT_P),3) - PC_STATES(o.Stg.BckUp_Cond_out,3));

        PC_COND2_UA_DELTA = PC_COND2_Q/PC_COND2_DELTA_T_LOG
        # print('PC_COND2_UA_DELTA= ' + str(PC_COND2_UA_DELTA))

    ## Sizing Steam Generation Train
    if design_BoilerBD == 1:	
		
		#SteamIN_ECO = [225,125,0,0,0,0,0,35] # T, p, ..., mdot
		#SteamOUT_ECO = [292]		
        #FlueGasIN_ECO = [410,1.3,0,51] # T, , ..., mdot

		#SteamIN_EV = [292,125,0,0,0,0,0,35]
        #FlueGasIN_EV = [600,1.3,0,51]
        #FlueGasOUT_EV = [410,1.3,0,51]

		#SteamIN_SH = [292,125,0,0,0,0,0,35]
		#SteamOUT_SH = [535]
        #FlueGasIN_SH = [1150,1.3,0,51]

        [PC_EV_EFF,    PC_EV_UA]     = evaporator(FlueGasIN_EV,PC_st[HPTin_n_st-2-1,:],FlueGasOUT_EV)                     #You take inlet and outlet conditions of EV (HTF side) and inlet conditions of EV (steam side)
        [PC_ECO_EFF,   PC_ECO_UA]    = economizer(PC_st[HPTin_n_st-3-1,:],FlueGasIN_ECO ,PC_st[HPTin_n_st-2-1,:])      #You take inlet and outlet conditions of EC (steam side) and inlet conditions of EC(HTF side)
        [PC_SH_EFF,    PC_SH_UA]     = economizer(PC_st[HPTin_n_st-1-1,:],FlueGasIN_SH,PC_st[HPTin_n_st-1,:])        #You take inlet and outlet conditions of SH (steam side) and inlet conditions of SH(HTF side)
		#[PC_RH_EFF,    PC_RH_UA]     = economizer(PC_st[IPTin_n_st-1-1,:],HTF[6,:],PC_st[IPTin_n_st-1,:])          #You take inlet and outlet conditions of RH (steam side) and inlet conditions of RH(HTF side)
        print("PC_EV_EFF",PC_EV_EFF)
        print("PC_ECO_EFF",PC_ECO_EFF)
        print("PC_SH_EFF",PC_SH_EFF)
    # elif design_HTFloop_set == 0:
    #     The function DSG receiver is used in the DSG model
	
    print(PC_st)

    ## Sizing Preheaters and Subcoolers... I AM TRYING WITH RAFAEL FUNCTIONS, SEE WHAT HAPPENS
    if PC_n_coldPH != 0:         # cold preheating

        #In PC_coldSC you get [1EFF 2UA 3CPH 4CPC 5FRcold]
        #In PC_coldPH you get [1EFF 2UA 3FRcold 4cpC]
        for i in range (1,PC_n_coldPH+1):
            [PC_coldSC[i-1,0] , PC_coldSC[i-1,1], PC_coldSC[i-1,2], PC_coldSC[i-1,3], PC_coldSC[i-1,4]] = subcooler(PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1)-1,:],PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)+2*PC_DeaLP + 2*PC_n_coldPH - 2*(i)-1,:],PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,:])

            [PC_coldPH[i-1,0] , PC_coldPH[i-1,1], PC_coldPH[i-1,2], PC_coldPH[i-1,3]] = preheater(PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)+2*PC_DeaLP + 2*PC_n_coldPH - 2*(i-1)-1,:],PC_st[1+PC_DoubleCond+PC_ValveCond_2+PC_PumpBeforeMix+PC_DoubleCond+(1-PC_PumpBeforeMix)+2*PC_DeaLP + 2*PC_n_coldPH - 2*(i-1)-1-1,:],PC_st[LPTout_n_st + 3*PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1)-1,:])


    if PC_n_hotPH != 0:         # hot preheating
        for i in range (1,PC_n_hotPH+1):
            PC_hotSC[i-1,0]     = 1 - 7/(PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + (2*i - 1)-1,0] - PC_st[PUMP2out_n_st + 2*PC_n_hotPH - 2*(i)-1,0])            #It does not make sense and then you overwrite it :/
            [PC_hotSC[i-1,0], PC_hotSC[i-1,1], PC_hotSC[i-1,2], PC_hotSC[i-1,3], PC_hotSC[i-1,4]] = subcooler(PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1)-1,:],PC_st[PUMP2out_n_st + 2*PC_n_hotPH - 2*(i)-1,:],PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i)-1,:])

            [PC_hotPH[i-1,0], PC_hotPH[i-1,1], PC_hotPH[i-1,2], PC_hotPH[i-1,3]] = preheater(PC_st[PUMP2out_n_st + 2*PC_n_hotPH - 2*(i-1)-1,:],PC_st[PUMP2out_n_st + 2*PC_n_hotPH - 2*(i-1)-1-1,:],PC_st[LPTout_n_st + PC_n_hotPH + 1 + PC_n_coldPH + PC_DeaLP + PC_DoubleCond + (2*i - 1)-1,:])

    ## Complete Thermodynamic states-----------------------------------------##
    [PC_st]= completestates(PC_st, PC_n_states)

    PC_Boiler_Pdrop = 0.0079*PC_mdot**2+0.0277*PC_mdot+5.8316                 #empiric correlation between p drop and the mass flow rate
    PC_Boiler_Pdrop_IIeq = 0.0074*PC_mdot**2+0.0012*PC_mdot+6.5675            #empiric correlation between p drop and the mass flow rate_Excel-based

    ## --------------------------------------------------------------------- ##

    return [PC_COND1_P, PC_COND2_P,PC_EV_UA, PC_ECO_UA, PC_SH_UA, PC_COND_Area, PC_COND2_Area, PC_COND1_Area, PC_W_HPT, PC_W_LPT, PC_Wparas, PC_W, APPROACH_COND1, PC_COND2_UA_DELTA, PC_COND_air_FR, PC_COND_fan_Power, PC_COND_Tcout, PC_COND_UA,PC_coldPH, PC_hotPH, PC_coldSC, PC_hotSC, PC_PUMP_W2, PC_PUMP_W_DeaLP, PC_PumpBefMix_Power,PC_ECO_Q, PC_EV_Q ,PC_SH_Q,PC_Wgross_el,PC_W_el, PC_CONDs_Q, PC_st,PC_keyst_DEAin_n_st, PC_keyst_PUMP2out_n_st, PC_keyst_HPTin_n_st, PC_keyst_IPTin_n_st, PC_keyst_LPTin_n_st, PC_keyst_LPTout_n_st, PC_LPT_ETA, PC_IPT_ETA, PC_HPT_ETA]

