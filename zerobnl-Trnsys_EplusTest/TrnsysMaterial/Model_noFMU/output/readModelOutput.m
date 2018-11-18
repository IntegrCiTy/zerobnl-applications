function result = readModelOutput(o, result)


%paths to TRNSYS output files%
powerFile = strcat(o.paths.TRNSYSoutput, filesep, 'Power.txt');

%read data from output files%
powerData   = dlmread(powerFile, '\t', 1, 0);


%extract field power values%
result.plant.P_HPT       = max(0, powerData(:,2)');
result.plant.P_LPT       = max(0, powerData(:,3)');
result.plant.H_CondTesFgc      = max(0, powerData(:,4)');
result.plant.Load_kJ      = max(0, powerData(:,5)');
result.plant.H_FGC_kJ      = max(0, powerData(:,6)');
result.plant.H_TES_kJ      = max(0, powerData(:,7)');
result.plant.DeaPumps      = max(0, powerData(:,8)');
result.plant.CondPump      = max(0, powerData(:,9)');
result.plant.FUEL        = max(0, powerData(:,10)');
result.plant.toTES        = max(0, powerData(:,11)');

result.plant.EpNet = (result.plant.P_HPT + result.plant.P_LPT)/3600/1000; % [MW] Net with respect to the off-design eff.
result.plant.Eparas = (result.plant.DeaPumps + result.plant.CondPump)/3600/1000; % [MW] % Net with respect to the off-design eff.
result.plant.H_CondTesFgc = (result.plant.H_CondTesFgc)/3600/1000; % [MW] 
result.plant.Load = (result.plant.Load_kJ)/3600/1000; % [MW] 
result.plant.H_Boilers = result.plant.Load-result.plant.H_CondTesFgc; % [MW] 
result.plant.H_FGC      = result.plant.H_FGC_kJ/3600/1000;% [MW] 
result.plant.H_TES      = result.plant.H_TES_kJ/3600/1000;% [MW] 
result.plant.H_toTES    = result.plant.toTES/3600/1000;% [MW] 
result.plant.H_Cond = result.plant.H_CondTesFgc-result.plant.H_FGC-result.plant.H_TES; % [MW]

end