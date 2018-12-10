
# You are using the MS STTP combined with PV template.
import numpy as np
## -----------------------POWER CYCLE------------------------------------##
PC_Plant_output_mode               = 2                                  # 1: el  2:heat

PC_convmode                        = 2                                  # [1] == Gross [2] == Net               [-]
PC_Wset_plant                      = 34.815                                 # Installed power capacity              [MW]
PC_units_num                       = 1
PC_Gen_Eff                         = 0.98                               # Electricity generator efficiency      [-]
PC_Mec_Eff                         = 1                                  # Mechanical efficiency                 [-]
PC_Pump_Eff                        = 0.85                               # Pump efficiency                       [-]
##-----------------------------------------------------------------------##
# Power Output Variances (this was only in KEVIN's model)
PC_autumnload =           1 #0.803;                                      # Autumn load as a percentage of summer load MINIMUM 70#
PC_winterload =           1 #0.739;                                      # Winter load as a percentage of summer load
PC_springload =           1 #0.974;                                      # Spring load as a percentage of summer load
# The following daily tiers are created for the PG&E tariff scheme:
PC_dailyloadtier1 =       1 #0.869;                                      # Tier 1 daily variance
PC_dailyloadtier2 =       1 #0.980;                                      # Tier 2 daily variance   MINIMUM 85#
PC_dailyloadtier3 =       1                                              # Tier 3 daily variance (peak period, set to 1)
PC_dailyloadtier4 = PC_dailyloadtier1                                  # Tier 4 daily variance

## SET PARAMETERS THERMODYNAMIC CYCLE_ BOOLE VARIABLES

PC_DoubleCond                      = 1                                  # 0 = just one DH HX 1 = two DH HX
PC_ValveCond_2                     = 1                                  # Vattenfall Case
PC_PumpBeforeMix                   = 1                                  # Vattenfall Case
PC_DeaLP                           = 1                                  # if there is a low-pressure dearator, besides the normal one
PC_BoilerValve                     = 1                                  # if there is a valve before ECO (Vattenfall case)
PC_BoilerMode                      = 1                                  # Components boiler: 0(EV,SH,RH), 1(1+EC)     [-]
PC_BackPrValve                     = 0                                  # if there is an extraction line of live steam
PC_DeaLocatHP                      = 1                                  # if the high-pressure dearator uses HP steam (Vattenfall and DoubleCond case)
PC_RHpresence                      = 0                                  # if RH is present

##
PC_PCONDset                        = 3                                  # 1: fixed, based on Tdrycond and dTapp
                                                                           # 2: location dependent (if mode 1,2,3,4,6 are applied), based on Tamb and air.dT and dTapp;
                                                                           # 3: based on DH network
PC_Pcrit                           = 220.65                             # Working fluid critical pressure      [bar]
PC_PinHPT                          = 140                                # Inlet pressure to HPT                 [bar]
PC_TinHPT                          = 540                                # HPT inlet temperature                 [°C]
##------------IPT exists only for Simple Rankine Cycle only--------------##

PC_PinIPT                          = 8.160                              # Inlet Pressure to IPT (which coincides with LPT in DC and Vattenfall cases)                [bar]
PC_TinIPT                          = 190.6                                # if o.design.ToutRHset == 3; Inlet Temperature to IPT
##
PC_TdropRH                         = 0                                  # if o.design.ToutRHset == 2; Percent of Reheat drop                [#]
PC_TdropPUMP                       = 0.03                               # Temperature drop in the pumps_Percentage of DeltaP         [-]
##-----------------------------------------------------------------------##
PC_n_hotPH                         = 1                                  # Extractions form HPT (to hot PHs)           [-]
PC_n_coldPH                        = 1                                  # Extractions form LPT (to cold PHs)          [-]
#PC_deaerLoc                       = 1                                  # Location of deaereator (Cold RH is 0 or 1)  [-]
#PC_n_deaHP                        = 1                                  # Number of dearators HP
##-----------------------------------------------------------------------##
PC_HPT_pr_mod                      = 1                                  # pressure ratio mode 0=equal 1=input         [-]
PC_LPT_pr_mod                      = 1                                  # pressure ratio mode 0=equal 1=input         [-]
PC_HPT_pr                          = [4.6197,3.5465]                    # pressure ratios in turbine sections         [-]
PC_HPT_pr                          = np.array(PC_HPT_pr)
PC_IPT_PR                          = 0                                  # pressure ratios in turbine sections         [-] #only in simple Rankine case it has a value
PC_LPT_pr                          = [2.678]                            # pressure ratios in turbine sections         [-]
PC_LPT_pr                          = np.array(PC_LPT_pr)
##-----------------------------------------------------------------------##
PC_TTDhot                          = 4                                  # TTD for high pressure hot side SC outlet    [°C]
PC_TTDcold                         = 2                                  # TTD for low p.  hot side SC outlet          [°C]
                                                                           # Those are defined as PP difference between 
                                                                           # hot outlet and cold inlet of the SC                                                              
PC_PdropPHhot                      = 2                                  # pressure drop in hot pre heaters            [bar]
PC_PdropPHcold                     = 2                                  # pressure drop in cold pre heaters           [bar]
PC_PdropSChot                      = 1                                  # pressure drop in hot subcoolers             [bar]
PC_PdropSCcold                     = 1                                  # pressure drop in cold subcoolers            [bar]
PC_TTDhotPH                        = 9                                  # PP difference for high p. PH state          [°C]
PC_TTDcoldPH                       = 2                                  # PP difference for low p. PH state           [°C]
PC_PHeffCOEFF                      = 0.95                               # Coefficient for UA evaluation in PH         [-]

## only Vattenfall Case ##
PC_HotExtr_dp                      = 0.045                               # percentage; p loss from the splitter to the PH #it could be a vector in case of more than 1 PH_hot
PC_DeaHPextr_dp                    = 0.05                                # percentage; p loss from the splitter to the DeaHP
PC_ColdExtr_dp                     = [0.03]                              # percentage; p loss from the splitter to the cold PH #it could be a vector in case of more than 1 PH_hot
PC_DeaLPextr_dp                    = 0.03                                # percentage; p loss from the splitter to the DeaLP
PC_BPValve_dp                      = 0                                   # p loss across the backpressure valve
PC_HPTout_dp                       = 0.045                               # percentage; p loss from the HPT outlet to the LPT(or IPT) inlet
## IF PC_PCONDset=3 --> DH network
PC_DH_T_return                     = 0
PC_DH_T_supply                     = 82                                  # [°C]
PC_DH_Pressure                     = 10                                  # [bar]
PC_DH_massflow                     = 400.15                              # [kg/s] Vattenfall
PC_Double_approach                 = 0.45                                #(percentuale di quanto riscalda il primo cond(COLD) rispetto al secondo)
PC_Heat_demand                     = 60                                  # [MW] Vattenfall
PC_dT_wtr_out_condensing           = 2                                   # Liquid side approach dT           [C]
PC_dt_wtr_out_condensing_bp        = 0                                   # only in case of extra HX if there is the BackPressureValve
## IF air condenser
PC_COND_dTapp                      = 25                                 #                                             [°C]
PC_COND_air_dT                     = 31                                 #                                             [°C]                            #
PC_COND_Pump_EFF                   = 0.85                               # Pump 1 efficiency                           [-]
PC_COND_fan_dP                     = 0.01                               # Fan pressure drop                           [bar]
PC_COND_fan_EFF                    = 0.85                               # Fan efficency                               [-]
##
PC_COND_Pdrop                      = 0                                  # Pressure drop through the cond.             [-]
PC_COND2_Pdrop                     = 0                                  # Pressure drop through the second condenser if DoubleCondenser = 1
PC_CONDbp_Pdrop                    = 0                                  # Pressure drop through the BackPr condenser (Vattenfall)
PC_COND_UAexp                      = 0.8                                # UA exp factor
## -----------------------STEAM GENERATION COMPONENTS--------------------##

PC_EV_dP                           = 0                                  # Pressure drop in EV                         [bar]
PC_ECO_dP                          = 5                                  # Pressure drop in ECO                        [bar]
PC_SH_dP                           = 8                                  # Pressure drop in SH                         [bar]
PC_RH_dP                           = 0                                  # Pressure drop in RH                         [bar]
PC_BValve_dP                       = 8                                  # Pressure drop across the boiler valve       [bar]
##only MS----------------------------------------------------------------##
PC_ECO_Pinch                       = 8                                  # Pinch Point Economizer                    [°C]
PC_ECO_dP_exp                      = 0.5                                # dP power law exponent                     [-]
PC_ECO_UA_exp                      = 0.2                                # UA power law exponent                     [-]
PC_EV_UA_exp                       = 0.2                                # UA power law exponent                     [-]
PC_SH_Pinch                        = 10                                 # Pinch Point Superheater                   [°C]
PC_SH_dP_exp                       = 0.5                                # dP power law exponent                     [-]
PC_SH_UA_exp                       = 0.2                                # UA power law exponent                     [-]
PC_RH_TTD                          = 16                                 # TTD Reheater                              [°C]

## -----------------------TURBOCONTROLLER--------------------------------##
##only MS----------------------------------------------------------------##
PC_turb_SDH                        = 0.25                                  # Turbine sync. delay for hot start          [h]
PC_turb_SDW                        = 0.75                                  # Turbine sync. delay for warm start         [h]
PC_turb_SDC                        = 1.5                                  # Turbine sync. delay for cold start         [h]
PC_turb_RDH                        = 0.25                                # Turbine ramp delay for hot                 [h]
PC_turb_RDW                        = 1                                # Turbine ramp delay for warm                [h]
PC_turb_RDC                        = 1.5                                  # Turbine ramp delay for cold                [h]
PC_turb_TBHWS                      = 8                                  # Time between hot and warm start            [h]
PC_turb_TBWCS                      = 60                                 # Time between warm and cold start           [h]
PC_turb_rampdown                   = 1                                  # Ramp delay to turn off Turbine system

## ----------------------------STARTUPS----------------------------------##
StartupsMode = 'off'                                                    # off --> no statups
                                                                           # startupsVs1 --> Ibrahim's startups
if StartupsMode != 'off':
    o = setModelLabel(o,2,StartupsMode)  # ---> to be fixed --> OSAMA

