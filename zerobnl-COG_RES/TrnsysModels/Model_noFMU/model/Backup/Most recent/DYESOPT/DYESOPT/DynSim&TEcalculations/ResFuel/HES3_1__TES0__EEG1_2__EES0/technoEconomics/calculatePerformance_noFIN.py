import numpy as np
import importlib

from PPSteadyStateDesign.EEG.EEG1_2.PowerBlock import *
from DesignParameters.HES3_1_Def_Par import *
from DesignParameters.ECON_Def_Par import *
CompPower = importlib.import_module('DynSim&TEcalculations.ResFuel.HES3_1__TES0__EEG1_2__EES0.output.calculateComponentPower')
IC        = importlib.import_module('DynSim&TEcalculations.' + HESTech + '.' + model_plant + '.technoEconomics.calculateInvestmentCost' )
OMC       = importlib.import_module('DynSim&TEcalculations.' + HESTech + '.' + model_plant + '.technoEconomics.calculateOperationMaintenanceCost' )

#calculate capacity factor#
result_plant_fCap = np.minimum(.99,CompPower.result_plant_Etot/(PC_Wset * 24 * 365))

# result_plant_dispatch_f = o.STO.dispatch_f;
#
# if result_plant_Etot > eps && result_plant_fCap > 0.02
#
#     #determine number of hot, warm and cold start ups#
#     nstart = 0; nhstarts = 0; ncstarts = 0;
#     for i = 2:length(result_plant_fLoad)
#         if result_plant_fLoad(i-1) == result_plant_fLoad(i)
#             aux = 0; aux1 = 0; aux2 = 0;
#         else
#             if result_plant_fLoad(i-1) == 0
#                 aux = 1;
#                 if i > PC_turb_TBHWS/(o.model.dt/3600) && (result_plant_fLoad((i-5/(o.model.dt/3600))) - result_plant_fLoad(i-1)) == 1
#                     aux1 = 1; aux2 = 0;
#                 else
#                     if i > (PC_turb_TBHWS + PC_turb_TBWCS)/(o.model.dt/3600)
#                         auxsum = 0;
#                         for j = i-(PC_turb_TBHWS + PC_turb_TBWCS)/(o.model.dt/3600):i-1
#                             auxsum = auxsum + result_plant_fLoad(j);
#                         end
#                         if auxsum == 0;
#                             aux2 = 1;
#                         else
#                             aux2 = 0;
#                         end
#                     end
#                     aux1 = 0; aux2 = 0;
#                 end
#             else
#                 aux = 0; aux1 = 0; aux2 = 0;
#             end
#         end
#         nstart   = nstart + aux;
#         nhstarts = nhstarts + aux1;
#         ncstarts = ncstarts + aux2;
#     end
#     result_plant_nstart = nstart;
#     result_plant_nhstarts = nhstarts;
#     result_plant_ncstarts = ncstarts;
#     result_plant_nwstarts = nstart - result_plant_nhstarts - result_plant_ncstarts;
#
#
#     #determine EOH#
#     result_plant_EOHs = result_plant_nhstarts*10 + (result_plant_nstart - result_plant_nhstarts - result_plant_ncstarts)*20 + result_plant_ncstarts*30;
#     result_plant_EOH = result_plant_NOH + result_plant_EOHs;
#     result_plant_EOHfrac = result_plant_NOH/result_plant_EOH*100;
#
#     #determine availability factor based on maintenance requirements#
#     result_plant_favail = 1 - ((3+3+6+3+6)/52)*(result_plant_EOH/100000);
#
#     # Correcting OPEX
#     result_cost_OPEXtot = result_cost_OPEXtot - result_cost_OPEX.Service;
#     result_cost_OPEX.Service = result_cost_OPEX.Service*(result_plant_EOHs/(365*20))^.8;
#     result_cost_OPEXtot = result_cost_OPEXtot + result_cost_OPEX.Service;

    # Lifetime OPEX


#No sense since I did one week simulation, so no sense to have LCOE
result_cost_CHP_OPEXtot     = OMC.result_cost_OPEXtot;

# result_cost_CHP_OPEXtot_WOT = OMC.result_cost_OPEXtot; ---> OSAMA: Doesn't make any sense, same value

i = 1
result_cost_CHP_OPEXtot_lifespan        = np.zeros(shape=[F_Lifespan,])
result_cost_CHP_OPEXtot_lifespan_WTD    = np.zeros(shape=[F_Lifespan,])

while i <= F_Lifespan:

    result_cost_CHP_OPEXtot_lifespan[i-1]     =  ((result_cost_CHP_OPEXtot)/((1 + econ_Discount_rate)**i));

    # result_cost_CHP_OPEXtot_lifespan_WTD[i-1] =  ((result_cost_CHP_OPEXtot_WOT)/((1 + econ_Discount_rate)**i));  ---> OSAMA: Doesn't make any sense, same value

    i = i + 1

# Calculate CHP lifetime electricity production

i=1
result_cost_CHP_El_lifespan        = np.zeros(shape=[F_Lifespan,])
while i <= F_Lifespan:

    result_cost_CHP_El_lifespan[i-1] = (CompPower.result_plant_Etot)/((1 + econ_Discount_rate)**i)

    i = i + 1

# Calculate LCOE

result_econ_CHP_LCOE      = (IC.result_cost_CAPEXtot*0.7 + np.sum(result_cost_CHP_OPEXtot_lifespan_WTD))/(np.sum(result_cost_CHP_El_lifespan))

# Calculate capacity factor

result_econ_cf_el         = (CompPower.result_plant_Etot)/(PC_W*8760/1000)



    #specific power cost#
    #result_cost_Cspec = result_cost_CAPEXtot/result_plant_Etot;


#     #total plant net revenue#
#     result_econ_Rev = result_plant_EpGen*130*(o.model.dt/3600) ;#  10000000;  .*result_econ_price         [USD]
#     result_econ_Revtot = sum(result_econ_Rev)*result_plant_favail - result_cost_OPEXtot;#   [USD]
#
#     #Net present value
#     result_econ_NPV = ErrIRR(o,result,econ_i*100);
#
#     #Plant Equivalent Operating Hours
#     result_plant_EOHplant = result_plant_Etot/PC_Wset;
#
#     #Internal Rate of Return
#     result_econ_IRR = fzero(@(IRR)ErrIRR(o,result,IRR), 5);


#     #For MOO:
#     result.IRR          = result_econ_IRR;#         [#]
#     result.LEC          = result_econ_LEC;#         [USD/MWh-e]
#     result.CAPEX        = result_cost_CAPEXtot;#    [USD]
#     result.CAPEX_total  = result_cost_CAPEXtot;#    [USD]
#     result.Cspec        = result_cost_Cspec;#       [USD/kWe]
result_OPEX         = OMC.result_cost_OPEXtot      #     [USD/y]
#     result.OPEX_total   = result_cost_OPEXtot;#     [USD/y]
#     result.NOH          = result_plant_NOH;#        [h/y]
#
#     result.EOH          = result_plant_EOH;#        [h/y]
#     result.T_EOH        = result_plant_EOH;#        [h/y]
#
#     result.EOHs         = result_plant_EOHs;#       [h/y]
#     result.EOHfrac      = result_plant_EOHfrac;#    [#]
#     result.fCap         = result_plant_fCap;#       [#]
#     result.nStart       = result_plant_nstart;#     [-]
#     result.hotStart     = result_plant_nhstarts;#   [-]
#     result.coldStart    = result_plant_ncstarts;#   [-]
#
#     result.EFFth_avg    = result_plant_EFFth_avg;
#     result.EFFsf_avg    = result_plant_EFFsf_avg;
#     result.EFFs_el_avg  = result_plant_EFFs2el_avg;
#
#     result.Egen         = result_plant_Etot;#       [MWh-e]
#     result.Annual_Enet  = result_plant_Etot/1000;
#
#     result.Egross           = result_plant_Egross_tot;# [MWh-e]
#     result.Annual_Egross    = result_plant_Egross_tot/1000;
#
#     result.Eparas           = result_plant_Epar_tot;#   [MWh-e]
#     result.Annual_Eparas    = result_plant_Epar_tot/1000;
#
#     result.Parfrac          = result_plant_Epar_tot/result_plant_Egross_tot;# [#]
#     result.Annualparfrac    = result_plant_Epar_tot/result_plant_Egross_tot;
#
#     result.NPV          = result_econ_NPV;#         [USD]
#
#     result.EOHplant     = result_plant_EOHplant;#        [h/y]
#     result.P_EOH        = result_plant_EOHplant;#        [h/y]
#
#     result.field_Aland  = o.field.Aland;



#     #report failure#
#     result.success = 0;











# Redefine for moo:

result_LEC          = result_econ_CHP_LCOE ;#    [USD/MWh-e]
#     result.CAPEX        = result_cost_PVCSP_CAPEX_WOT;#    [USD]
#     result.CAPEX_total  = result_cost_PVCSP_CAPEX_WOT;#    [USD]
result_fCap         = result_econ_cf_el;#       [#]
result_FUEL         = CompPower.result_plant_FUEL_tot;#
#
aa=2+2
#
#
## Additional required functions ------------------------------------------OSAMA-------> To be fixed in future amendments
# function NPVfinal = ErrIRR(o,result,IRR)
#     result_econ_IRR = IRR;
#     result_cost_CAPEXtot_ITC = (result_cost_CAPEXtot/1e6)*(1 - econ_ITC/100);
#     NPV(1) = 0;
#     for t = 0:1
#         NPV(t+1) = NPV(1) - result_cost_CAPEXtot_ITC/(2*(1+result_econ_IRR/100)^t);
#     end
#     for t = 2:(econ_n + 2)
#         NPV(t+1) = NPV(t) + (result_econ_Revtot/1e6)/((1+result_econ_IRR/100)^t);
#     end
#     for t = (econ_n + 3):(econ_n + 4)
#         NPV(t+1) = NPV(t) - econ_decom*(result_cost_CAPEXtot_ITC/1e6)/((1+result_econ_IRR/100)^t);
#     end
#     NPVfinal    = NPV(econ_n + 5);
#
# end
#
# # Combined PV-CSP
#
# def ErrIRR_PVCSP(result_cost_PVCSP_CAPEX,IRR, result_econ_Revtot, econ_decom, econ_n):
#     result_econ_IRR_PVCSP = IRR;
#     result_cost_CAPEXtot_ITC = (result_cost_PVCSP_CAPEX/1e6)
#     NPV[0] = 0
#     for t in range (0,1):
#         NPV[t] = NPV[0] - result_cost_CAPEXtot_ITC/(2*(1+result_econ_IRR_PVCSP/100)**t)
#
#     for t in range(2,(econ_n + 2)):
#         NPV[t] = NPV[t-1] + (result_econ_Revtot/1e6)/((1+result_econ_IRR_PVCSP/100)**t)
#
#     for t in range ((econ_n + 3),(econ_n + 4)):
#         NPV[t] = NPV[t-1] - econ_decom*(result_cost_CAPEXtot_ITC/1e6)/((1+result_econ_IRR_PVCSP/100)**t)
#
#     NPVfinal    = NPV[econ_n + 5]
#     return NPVfinal
#
#
# # Combined PV
#
# function NPVfinal = ErrIRR_PV(o,result,PV_IRR)
#     result_econ_PV_IRR = PV_IRR;
#     result_cost_CAPEXtot_ITC = (result_cost_PV_CAPEX.TOTAL/1e6);
#     NPV(1) = 0;
#     for t = 0:1
#         NPV(t+1) = NPV(1) - result_cost_CAPEXtot_ITC/(2*(1+result_econ_PV_IRR/100)^t);
#     end
#     for t = 2:(econ_n + 2)
#         NPV(t+1) = NPV(t) + (result_econ_PV_Revtot/1e6)/((1+result_econ_PV_IRR/100)^t);
#     end
#     for t = (econ_n + 3):(econ_n + 4)
#         NPV(t+1) = NPV(t) - econ_decom*(result_cost_CAPEXtot_ITC/1e6)/((1+result_econ_PV_IRR/100)^t);
#     end
#     NPVfinal    = NPV(econ_n + 5);
#
# end
#
# end
