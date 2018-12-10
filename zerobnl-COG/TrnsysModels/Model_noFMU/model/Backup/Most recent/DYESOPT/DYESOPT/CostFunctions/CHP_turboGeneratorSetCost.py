import math

def CHP_turboGeneratorSetCost(E_elec_ts,eff,REHEAT,E_mech_sect,T_sec_in,f_case,extractions,c_ref,E_ref,scaling_f):

    # EXPLANATION
    #Cost of the whole turbogenerator including the alterator as a function of
    #its power output. Taken from Pelster (red thesis with falling pages)
    #
    #In order of appearance:
    #
    #E_elec_ts    is the power of the investigated turboset (HP+LP) [kW].
    #
    #eff          if the electrical to mechanical efficieny of the turboset
    #
    #REHEAT       'reheat' in order to estimate the cost of a turboset with
    #             reheat
    #
    #E_mech_sect  VECTOR containing the Mechanical power of the INLET section
    #             on each turbine (HP/LP) [kW].
    #
    #T_sec_in     Inlet temperature to the turbo set [oC]
    #
    #f_case       is the cost increase due to a separate high pressure
    #             casing. a) Reheat f_case=1.2, b) Gearbox HP f_case=1.15, a)
    #             and b) f_case=1.3
    #
    #c_ref        is the specific cost of A turboset in [USD/kW] with a reference
    #             power E_ref [kW].
    #             From the thesis values for c_ref and E_ref are obtained.
    #
    #c_ts         is the specific cost of the turboset [USD/kW]
    #
    #f_temp       is the temperature correction factor.
    #
    #f_exposure   turbine exposure factor (related to temp factor)
    #
    #C_ts         is the total invetment cost of the turbogenerator [USD].
    #
    #C_ext        Extraction costs [Hendriks 1994]
    ########################################################################################################################
    ## EQUATIONS

    # E_ref=80*10^3; #kW

    # c_ref=110; #USD/kW

    #specific const of the turboset#
    c_ts=c_ref*(E_elec_ts/E_ref)**scaling_f  # scaling_f originally fixed to 0.67

    E_mech_ts=E_elec_ts/eff

    if REHEAT == 'reheat':

        f_exposure=sum(E_mech_sect)/E_mech_ts

    #     f_case=1.3;

    else:

        f_exposure=E_mech_sect(1)/E_mech_ts

    #     f_case=1.15;

    T_sec_in=T_sec_in+273.15

    f_temp=1+f_exposure*5*math.exp((T_sec_in-866)/10.42)

    C_ts=E_elec_ts*c_ts*f_temp*f_case

    C_ext=0.5*10**6*(E_elec_ts/600000)        #additional cost due to extractions

    cost=C_ts+C_ext*extractions

    return cost
