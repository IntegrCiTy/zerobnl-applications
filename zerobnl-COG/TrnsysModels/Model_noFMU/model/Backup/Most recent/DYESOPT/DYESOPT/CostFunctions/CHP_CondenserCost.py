import numpy as np
def CHP_CondenserCost(Qcond, Tcond, Tin, Tout, mcool,c1,c2,f_ms,CT,Tamb,Acond,Acond_2):
    # EXPLANATION
    #Cost of a wet condenser. Taken from Pelster (red thesis with falling pages)
    #
    #In order of appearance:
    #
    #Qcond       rejected heat in the condenser [MW]
    #
    #Tcond        saturated temperature of the condensate    
    #
    #Tin          water inlet temperature to the condenser
    #             
    #              
    #Tout         water outlet temperature to the condenser
    #             
    #              
    #mcool        cooling water mass flow
    #
    #f_ms       actualization factor (page 77 of the thesis)
    #
    # CT      if 0=no cooling tower; if 1=yes cooling tower
    #
    # f_tt    temperature correction factor
    #
    # Tamb    ambient temperature
    #
    # Twetbulb  Wet bulb temperature
    #
    # f_tcw   factor of the coling tower
    #
    #  Tcw    temperature reduction in the cooling tower
    
    
    ## EQUATIONS
    
    To=Tcond-Tout
    
    Ti=Tcond-Tin
    
    Tlm=(To-Ti)/(np.log(To/Ti))
    
    k=2200 #W/(m2*K)
    
    #Acond=Qcond/(k*Tlm);
    
    # c1=248; #usd/m2
    
    # c2=659; #usd/m2
    
    C_cond   =(c1*Acond+c2*mcool)*f_ms
    
    C_cond_2 =(c1*Acond_2+c2*mcool)*f_ms
    
    if CT == 1:
        Tcool=(Tin+Tout)/2

        Twetbulb=0.8474*Tamb+1.7895

        f_tt=-0.69*np.log(Tcool-Twetbulb)+2.1898

        Tcw=Tout-Tin

        f_tcw=-0.0013*Tcw**3+0.0144*Tcw**2+0.0929*Tcw+0.501

        C_tower=72*(10**3)*((Qcond/1e3)/(3.6*(10**6)))*f_tt*f_tcw*2.35*f_ms
    
    else:
        
        C_tower = 0
    
    cost=C_cond + C_cond_2 + C_tower;

    return cost
