from PPSteadyStateDesign.EEG.EEG1_2.PowerBlock import *
from DesignParameters.EEG1_2_Def_Par import *
from PPSteadyStateDesign.EEG.EEG1_2 import rankine_reheat

def errorW(FR):

    PC_mdot= FR
    # import PPSteadyStateDesign.EEG.EEG1_2.rankine_reheat
    # from PPSteadyStateDesign.EEG.EEG1_2.rankine_reheat import *

    [PC_Wgross_el, PC_W_el, PC_CONDs_Q]= rankine_reheat.rankine_reheat(PC_mdot)
    if PC_Plant_output_mode == 1:
        if PC_convmode == 1:
            ErrW = (PC_Wset - PC_Wgross_el/1000)/(PC_Wset)*100
        else:
            ErrW = (PC_Wset - PC_W_el/1000)/(PC_Wset)*100
    else:
        ErrW = (PC_Heat_demand - PC_CONDs_Q/1000)/PC_Heat_demand*100

    return [ErrW]
