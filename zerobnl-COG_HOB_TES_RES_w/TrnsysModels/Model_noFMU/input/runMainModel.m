function result = runMainModel(o)

% Here an annual dynamic simulation is run. Input data are prepared, the
% plant performance is simulated and the results are collected to be used
% for techno-economic post-process evaluation.

%%  

%inform of current operation%
if strcmpi(o.model.runMode, 'single');
    disp('>> TRNSYS: Preparing input data... ');
end

%add TRNSYS paths%
o = addModelPaths(o);

%if single run or first optimisation run%
if strcmpi(o.model.runMode, 'single') || strcmpi(o.model.runMode, 'firstOptim')

    %extract weather data and get simulation duration%
    o = writeWeatherFile(o);
    
else
    
    %extract simulation duration from file%
    o = readSimFile(o);
    
end

%create structure with standard data%
TRNSYSdata = standardTRNSYSdata(o);

%load TRNSYS data and correct units%
TRNSYSdata = prepareTRNSYSinput(o, TRNSYSdata);
TRNSYSdata = adjustTRNSYSunits(TRNSYSdata);

%write TRNSYS input files%
writeTRNSYSinput(o, TRNSYSdata);

if isfield(o, 'field')
    writeFieldMatrix(o);
end
   
% if isfield(o.model, 'priceFile');
%     write_prfile(o);
% end
   
%create output structure%
result = struct;

if strcmp(o.model.plant,'PV-CSP_baseload') == 1;
    %Run annual performance of PV model in Matlab
    disp('');
    disp('>> Now launching PV Performance Model in Matlab');
    disp('>> Waiting for PV model to converge... ');
    [o, result] = PVperformance(o);
    disp('');
    [result,o] = write_CSPloadfile(o, result);
end

%inform of current operation%
if strcmpi(o.model.runMode, 'single')
    disp(['>> TRNSYS: Launching TRNEXE with file: ', o.model.plant, '.dck']); disp(' ');
    disp('>> Waiting for TRNSYS to end... ');
end

%run TRNSYS model%
result.success = runTRNSYSmodel(o);

if result.success == 1

    %read results of TRNSYS simulation%
    result = readModelOutput(o, result);
    
    if result.success == 1
    
        %calculate model-component powers%
        result = calculateComponentPower(o, result);
        
    end

end