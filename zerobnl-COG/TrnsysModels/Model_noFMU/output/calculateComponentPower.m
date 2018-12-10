function result = calculateComponentPower(o, result)

%calculate generator output%!!Moni is not sure about the function
%generatorEfficiency (Partial load eff.)
result.plant.EpGen   = result.plant.EpNet; %%.*generatorEfficiency(result.plant.EpNet/(o.PC.W/1e3),  sqrt(o.PC.Gen_Eff), sqrt(o.PC.Gen_Eff));
result.plant.EpParas = result.plant.Eparas; %%.*generatorEfficiency(result.plant.Eparas/(o.PC.Wparas/1e3),  sqrt(o.PC.Gen_Eff), sqrt(o.PC.Gen_Eff));
result.plant.EpSold = result.plant.EpGen - result.plant.EpParas;

result.plant.Etot       = (sum(result.plant.EpGen))*(o.model.dt/3600);% [MWh]
% Parasitic consumption
result.plant.Epar_tot   = sum(result.plant.EpParas)*(o.model.dt/3600);% [MWh]
% Gross power generation
result.plant.Esold_tot = sum(result.plant.EpSold)*(o.model.dt/3600);% [MWh]
% Fuel needed in boiler
result.plant.FUEL_tot   = (sum(result.plant.FUEL))*(o.model.dt/3600);% [MWh]

% Heat Power generated in the plant (condenser, TES, FGC)
result.plant.H_CondTesFgc_tot   = sum(result.plant.H_CondTesFgc)*(o.model.dt/3600)*1.05;% [MWh] Heat losses
% Load
result.plant.ReferenceLoad   = sum(result.plant.Load)*(o.model.dt/3600);% [MWh]
% Boiler use
result.plant.H_Boilers_tot   = sum(result.plant.H_Boilers)*(o.model.dt/3600)*1.05;% [MWh] hHeat losses
result.plant.H_Boilers_max   = max(result.plant.H_Boilers);% [MW]
% FGC use
result.plant.H_FGC_tot      = sum(result.plant.H_FGC)*(o.model.dt/3600);% [MWh]
result.plant.H_FGC_max   = max(result.plant.H_FGC);% [MW]
% TES use
result.plant.H_TES_tot      = sum(result.plant.H_TES)*(o.model.dt/3600);% [MWh]
result.plant.H_TES_max   = max(result.plant.H_TES);% [MW]
% Condenser use
result.plant.H_Cond_tot      = sum(result.plant.H_Cond)*(o.model.dt/3600);% [MWh]

result.plant.H_toTES_tot = sum(result.plant.H_toTES)*(o.model.dt/3600);% [MWh]

% Percentage over the year
result.plant.H_FGC_Perc = result.plant.H_FGC_tot/result.plant.ReferenceLoad*100;
result.plant.H_TES_Perc = result.plant.H_TES_tot/result.plant.ReferenceLoad*100;
result.plant.H_Cond_Perc = result.plant.H_Cond_tot/result.plant.ReferenceLoad*100;
result.plant.H_Boiler_Perc = result.plant.H_Boilers_tot/result.plant.ReferenceLoad*100;


%Plot

% PLOT
figure(1)
plot([0:24],result.plant.H_FGC(722:746), 'LineWidth',4)
hold on
plot([0:24],result.plant.H_FGC(722:746)+result.plant.H_Cond(722:746), 'LineWidth',4)
hold on
plot([0:24],result.plant.H_FGC(722:746)+result.plant.H_Cond(722:746)+result.plant.H_TES(722:746), 'LineWidth',4)
hold on
plot([0:24],result.plant.H_toTES(722:746), 'LineWidth',4)
hold on
plot([0:24],result.plant.H_FGC(722:746)+result.plant.H_Cond(722:746)+result.plant.H_TES(722:746)+result.plant.H_Boilers(722:746), 'LineWidth',4)
hold on
plot([0:24],result.plant.Load(722:1:746), '*', 'LineWidth',4)

grid on
axis([0 24 0 36])
ax = gca;
ax.XTick = [0:1:24];
xlabel('hours [h]','FontSize',20,'FontWeight','bold')
ylabel('Heat generation [MWh]','FontSize',20,'FontWeight','bold')
set(gca,'FontSize',20)
legend('FGC','Condenser', 'TES discharge','TES charge', 'Boilers', 'Load','FontSize',20,'FontWeight','bold','Location', 'North','Orientation','horizontal', 'boxon')

end


