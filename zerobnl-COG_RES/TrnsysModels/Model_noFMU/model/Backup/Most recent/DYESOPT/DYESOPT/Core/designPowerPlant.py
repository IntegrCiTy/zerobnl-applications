# Here the sizing of the chosen power plant model starts

from Core.setDefaultParameters import *
from Core.setModelLabel import *
import numpy as np
import importlib
import datetime
import pvlib as pv

# Here maybe you should check some general inputs.. and then continue only
# if success turns to be equal to 1.

## Design Conditions for selected location ...............................#    
# change design mode to 1 and design DNI to zero when you finish

if design_mode == 1 and design_DNI <= 0:
# Design Conditions based on input date (location, day & time)
    weatherFile     = 'C:' + '\DYESOPT\DYESOPT\Data\ClimateData' + '\\' + model_wFile + '.txt'
    wData           = np.loadtxt(weatherFile, comments='#', delimiter=',', converters=None, skiprows=4, usecols=None, unpack=False, ndmin=0)
# Inputs should be available in CSP HES default parameters for design day and time
    designrow_n     = 1 + np.round((design_day-1) * 24 * (1 / (wData[2,1] - wData[1,1])) + (design_tsolar * (1 / (wData[2,1] - wData[1,1]))))
    Ib              = wData[int(designrow_n-1),4]               # To adapt the start from zero in Python
    Tamb            = wData[int(designrow_n-1),2] - 273.15
    design_DNI      = Ib
    design_Tamb     = Tamb
    design_coord    = np.genfromtxt(weatherFile, comments='#', delimiter=',', skip_header=0, skip_footer=8762, converters=None, missing_values=None, filling_values=0, usecols=None, names=None, excludelist=None, deletechars=None, replace_space='_', autostrip=False, case_sensitive=True, defaultfmt='f%i', unpack=None, usemask=False, loose=True, invalid_raise=True, max_rows=None, encoding='bytes')
    design_lat      = np.radians(design_coord[1,0])
    design_long     = np.radians(design_coord[1,1])
# Solar position is not matching values from original DYESOPT - To be checked later --> Osama
    design_date     = datetime.date(int(datetime.date.today().strftime('%Y')), 1, 1) + datetime.timedelta(design_day - 1)
    design_Sol_pos  = pv.solarposition.get_solarposition(design_date + ' ' + str(design_tsolar)+':00:00', design_coord[1,0], design_coord[1,1], altitude=None, pressure=None, method='nrel_numpy', temperature=12)
    design_Sol_pos  = np.array(design_Sol_pos)
    print(design_Sol_pos)
    success         = 1

elif design_mode == 2 and design_DNI <= 0:
# Design Conditions based on summer solstice at noon
    weatherFile     = 'C:' + '\DYESOPT\DYESOPT\Data\ClimateData' + '\\' + model_wFile + '.txt'
    wData           = np.loadtxt(weatherFile, comments='#', delimiter=',', converters=None, skiprows=4, usecols=None, unpack=False, ndmin=0)
    design_day      = 173
    design_tsolar   = 12
    designrow_n     = 1 + np.round((design_day-1) * 24 * (1 / (wData[2,1] - wData[1,1])) + (design_tsolar * (1 / (wData[2,1] - wData[1,1]))))
    Ib              = wData[int(designrow_n-1),4]               # To adapt the start from zero in Python
    Tamb            = wData[int(designrow_n-1),2] - 273.15
    design_DNI      = Ib
    design_Tamb     = Tamb
    design_coord    = np.genfromtxt(weatherFile, comments='#', delimiter=',', skip_header=0, skip_footer=8762, converters=None, missing_values=None, filling_values=0, usecols=None, names=None, excludelist=None, deletechars=None, replace_space='_', autostrip=False, case_sensitive=True, defaultfmt='f%i', unpack=None, usemask=False, loose=True, invalid_raise=True, max_rows=None, encoding='bytes')
    design_lat      = np.radians(design_coord[1,0])
    design_long     = np.radians(design_coord[1,1])
# Solar position is not matching values from original DYESOPT - To be checked later --> Osama
    design_date     = datetime.date(int(datetime.date.today().strftime('%Y')), 1, 1) + datetime.timedelta(design_day - 1)
    design_Sol_pos  = pv.solarposition.get_solarposition(str(design_date) + ' ' + str(design_tsolar)+':00:00', design_coord[1,0], design_coord[1,1], altitude=None, pressure=None, method='nrel_numpy', temperature=12)
    design_Sol_pos  = np.array(design_Sol_pos)
    print(str(design_date) + ' ' + str(design_tsolar)+':00:00')
    print(design_Sol_pos)
    success         = 1

elif design_mode == 3 and design_DNI <= 0:
# Design Conditions based on winter solstice at noon
    weatherFile     = 'C:' + '\DYESOPT\DYESOPT\Data\ClimateData' + '\\' + model_wFile + '.txt'
    wData           = np.loadtxt(weatherFile, comments='#', delimiter=',', converters=None, skiprows=4, usecols=None, unpack=False, ndmin=0)
    design_day      = 351
    design_tsolar   = 12
    designrow_n     = 1 + np.round((design_day-1) * 24 * (1 / (wData[2,1] - wData[1,1])) + (design_tsolar * (1 / (wData[2,1] - wData[1,1]))))
    Ib              = wData[int(designrow_n-1),4]               # To adapt the start from zero in Python
    Tamb            = wData[int(designrow_n-1),2] - 273.15
    design_DNI      = Ib
    design_Tamb     = Tamb
    design_coord    = np.genfromtxt(weatherFile, comments='#', delimiter=',', skip_header=0, skip_footer=8762, converters=None, missing_values=None, filling_values=0, usecols=None, names=None, excludelist=None, deletechars=None, replace_space='_', autostrip=False, case_sensitive=True, defaultfmt='f%i', unpack=None, usemask=False, loose=True, invalid_raise=True, max_rows=None, encoding='bytes')
    design_lat      = np.radians(design_coord[1,0])
    design_long     = np.radians(design_coord[1,1])
# Solar position is not matching values from original DYESOPT - To be checked later --> Osama
    design_date     = datetime.date(int(datetime.date.today().strftime('%Y')), 1, 1) + datetime.timedelta(design_day - 1)
    design_Sol_pos  = pv.solarposition.get_solarposition(str(design_date) + ' ' + str(design_tsolar)+':00:00', design_coord[1,0], design_coord[1,1], altitude=None, pressure=None, method='nrel_numpy', temperature=12)
    design_Sol_pos  = np.array(design_Sol_pos)
    print(str(design_date) + ' ' + str(design_tsolar)+':00:00')
    print(design_Sol_pos)
    success         = 1

elif design_mode == 4 and design_DNI <= 0:
# Design Conditions based on Spring Equinox
    weatherFile     = 'C:' + '\DYESOPT\DYESOPT\Data\ClimateData' + '\\' + model_wFile + '.txt'
    wData           = np.loadtxt(weatherFile, comments='#', delimiter=',', converters=None, skiprows=4, usecols=None, unpack=False, ndmin=0)
    design_day      = 79
    design_tsolar   = 12
    designrow_n     = 1 + np.round((design_day-1) * 24 * (1 / (wData[2,1] - wData[1,1])) + (design_tsolar * (1 / (wData[2,1] - wData[1,1]))))
    Ib              = wData[int(designrow_n-1),4]               # To adapt the start from zero in Python
    Tamb            = wData[int(designrow_n-1),2] - 273.15
    design_DNI      = Ib
    design_Tamb     = Tamb
    design_coord    = np.genfromtxt(weatherFile, comments='#', delimiter=',', skip_header=0, skip_footer=8762, converters=None, missing_values=None, filling_values=0, usecols=None, names=None, excludelist=None, deletechars=None, replace_space='_', autostrip=False, case_sensitive=True, defaultfmt='f%i', unpack=None, usemask=False, loose=True, invalid_raise=True, max_rows=None, encoding='bytes')
    design_lat      = np.radians(design_coord[1,0])
    design_long     = np.radians(design_coord[1,1])
# Solar position is not matching values from original DYESOPT - To be checked later --> Osama
    design_date     = datetime.date(int(datetime.date.today().strftime('%Y')), 1, 1) + datetime.timedelta(design_day - 1)
    design_Sol_pos  = pv.solarposition.get_solarposition(str(design_date) + ' ' + str(design_tsolar)+':00:00', design_coord[1,0], design_coord[1,1], altitude=None, pressure=None, method='nrel_numpy', temperature=12)
    design_Sol_pos  = np.array(design_Sol_pos)

    success         = 1

elif design_mode == 5:
# Design Conditions based on input date, hour, Tamb and DNI)
    weatherFile     = 'C:' + '\DYESOPT\DYESOPT\Data\ClimateData' + '\\' + model_wFile + '.txt'
    wData           = np.loadtxt(weatherFile, comments='#', delimiter=',', converters=None, skiprows=4, usecols=None, unpack=False, ndmin=0)
    design_day      = design_day
    design_tsolar   = design_tsolar
    design_DNI      = design_DNI
    design_Tamb     = design_Tamb
    design_coord    = np.genfromtxt(weatherFile, comments='#', delimiter=',', skip_header=0, skip_footer=8762, converters=None, missing_values=None, filling_values=0, usecols=None, names=None, excludelist=None, deletechars=None, replace_space='_', autostrip=False, case_sensitive=True, defaultfmt='f%i', unpack=None, usemask=False, loose=True, invalid_raise=True, max_rows=None, encoding='bytes')
    design_lat      = np.radians(design_coord[1,0])
    design_long     = np.radians(design_coord[1,1])
    design_date     = datetime.date(int(datetime.date.today().strftime('%Y')), 1, 1) + datetime.timedelta(design_day - 1)
    design_Sol_pos  = pv.solarposition.get_solarposition(str(design_date) + ' ' + str(design_tsolar)+':00:00', design_coord[1,0], design_coord[1,1], altitude=None, pressure=None, method='nrel_numpy', temperature=12)
    design_Sol_pos  = np.array(design_Sol_pos)

    success         = 1

# Design Conditions based maximum irradiation and
# Has to be checked with Monica to understand the logic in the matlab version
elif design_mode == 6:
    weatherFile     = 'C:' + '\DYESOPT\DYESOPT\Data\ClimateData' + '\\' + model_wFile + '.txt'
    wData           = np.loadtxt(weatherFile, comments='#', delimiter=',', converters=None, skiprows=4, usecols=None, unpack=False, ndmin=0)
    Ib              = np.amax(wData[:,4])
    design_row      = wData[np.where(wData[:,4] == Ib)]

    if model_location == 7:
        Tamb        = design_row[0,2]
    else:
        Tamb        = design_row[0,2]-273.5

    design_DNI            = Ib*.85
    design_Tamb           = Tamb

    success = 1

else:
    success = 1


print('>>  Steady State design initiated...')

 ## ----------------------- Power Cycle Block --------------------------- ##
if success == 1 and EEGblock != 0:
    EEGpath= str('PPSteadyStateDesign.EEG.'+EEGname+'.PowerBlock')
    importlib.import_module(EEGpath)


#         addpath(genpath(strcat(paths.dyesoptRoot, filesep,'PPSteadyStateDesign', filesep,'ElectricalEnergyGenerationBlocks', filesep, 'Choice folder')));
#         o = Choice_EEGBlock(o);
#
# end
# ## ---------------------- Electrical Energy Storage Block --------------------- ##
# if success == 1 && strcmp(EESblock , 'off') == 0 #~
#
#         addpath(genpath(strcat(paths.dyesoptRoot, filesep,'PPSteadyStateDesign', filesep,'ElectricalEnergyStorageBlocks', filesep, 'Choice folder')));
#         o = Choice_EESBlock(o);
#
# end
# ## ---------------------- Heat Energy Source Block --------------------- ##
# if success == 1 && strcmp(HESblock , 'off') == 0 #~
#
#         addpath(genpath(strcat(paths.dyesoptRoot, filesep,'PPSteadyStateDesign', filesep,'HeatEnergySourceBlocks', filesep, 'Choice folder')));
#         o = Choice_HESBlock(o);
#
# end
# ## ---------------------- Thermal Energy Storage Block ----------------- ##
# if success == 1 && strcmp(TESblock , 'off') == 0 #~
#
#         addpath(genpath(strcat(paths.dyesoptRoot, filesep,'PPSteadyStateDesign', filesep,'ThermalEnergyStorageBlocks', filesep, 'Choice folder')));
#         o = Choice_TESBlock(o);
#
# end
#
# #Sun to Electricity Efficiency--------------------------------------------#
# if success == 1 && strcmp(HESblock , 'CSP') == 1 #Check also where to move this to have a better structure
#             PC.EFF_sun_to_MWe = field.effNom*rec.EFF*PC.EFFel;
# end
#
# end

if success == 1:

    print('>>  Steady state design accomplished successfully')
    print(' ')
