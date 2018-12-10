import os
import numpy as np
import importlib
#import datetime
#import pandas as pd
#import pvlib as pv

from Core.setModelLabel import *
from Core.setDefaultParameters import *
from model_Choice import *
EEG_DP_module= importlib.import_module('DesignParameters.'+EEGname+'_Def_Par')
HES_DP_module= importlib.import_module('DesignParameters.'+HESname+'_Def_Par')


#determine full input file name#
wthFile = os.path.join('C:\DYESOPT\DYESOPT\DynSim&TEcalculations' , HESTech , model_plant  ,'input\weatherData.txt')
simFile = os.path.join('C:\DYESOPT\DYESOPT\DynSim&TEcalculations' , HESTech , model_plant  ,'input\simData.txt')

#load weather data from standard file#
weatherFile     = os.path.join('C:\DYESOPT\DYESOPT\Data\ClimateData' + '\\' + HES_DP_module.model_wFile + '.txt')
wData           = np.loadtxt(weatherFile, comments='#', delimiter=',', converters=None, skiprows=4, usecols=None, unpack=False, ndmin=0)

#get site latitude from file#
coord    = np.genfromtxt(weatherFile, comments='#', delimiter=',', skip_header=0, skip_footer=8762, converters=None, missing_values=None, filling_values=0, usecols=None, names=None, excludelist=None, deletechars=None, replace_space='_', autostrip=False, case_sensitive=True, defaultfmt='f%i', unpack=None, usemask=False, loose=True, invalid_raise=True, max_rows=None, encoding='bytes')
lat      = coord[1,0]
long     = coord[1,1]
#read day and hour data#
n = wData[:,0]
h = wData[:,1]

#total data length#
hTot = 24*len(np.unique(n))

#determine data size#
nPoints = len(h)

#create new time vectors#
hOrg = np.linspace(0, hTot, nPoints);
hNew = np.arange(0, hTot+model_dt/3600,model_dt/3600) #Fix this to be only from HES def Par like the commented example and the above importlib ---->Osama
# hNew = np.arange(0, hTot+HES_DP_module.model_dt/3600,HES_DP_module.model_dt/3600)

#new weather data properties#
model_hrSim = max(hNew)
nNew = len(hNew)

#reduce time data to daily basis#
nDay = np.floor(np.interp(np.minimum(hNew + model_dt/216000, hTot),hOrg,n))
hDay = np.remainder(hNew, 24)

hDay= hDay.tolist()

#####OSAMA###Commented part below already working but takes a very long time for computing, to be fixed later on, currently az and el set as arrays of zeros###################
#######################################################################################################################

# for i in range (0,len(hDay)):
#     x= hDay[i]
#     hour = int(x)
#     minute = int((x - int(x))*60.0)
#     second = int(((x - int(x))*60 - int((x - int(x))*60.0))*60.0)
#     hDay[i]=((datetime.time(hour, minute, second)).strftime('%H:%M:%S'))
#
# #calculate solar positions#
# nDay_to_date= np.zeros(shape =(len(nDay),),dtype='datetime64[D]')
#
# for i in range(0,len(nDay)):
#     nDay_to_date[i]   = datetime.date(int(datetime.date.today().strftime('%Y')), 1, 1) + datetime.timedelta(nDay[i] - 1)
#
# design_Sol_pos  = pv.solarposition.get_solarposition(str(nDay_to_date[0]) + ' ' + str(hDay[0]), coord[1,0], coord[1,1], altitude=None, pressure=None, method='nrel_numpy', temperature=12)
#
# for i in range(0,len(nDay)):  # to b fixed before closing this file --> OSAMA
#     design_Sol_pos_new  = pv.solarposition.get_solarposition(str(nDay_to_date[i]) + ' ' + str(hDay[i]), coord[1,0], coord[1,1], altitude=None, pressure=None, method='nrel_numpy', temperature=12)
#     design_Sol_pos  = design_Sol_pos.append(design_Sol_pos_new)
#
# design_Sol_pos  = np.array(design_Sol_pos)
#
# az= design_Sol_pos[:,2]
# el= design_Sol_pos[:,3]

#######################################################################################################################
######### Till we fix the az and el:
az= np.zeros(shape =(len(nDay),))
el= np.zeros(shape =(len(nDay),))

# # To be checked, couldn't find a trace for it so far --> OSAMA
# if isfield(o, 'field')
#     field.az = az;
#     field.el = el; ### !!!!!!!!!!!!!!! only for luis case. it will be changed ATTENTION!!!!!!!!!!!!!!!!!
# end

#calculate integrated values#
Icum = np.cumsum(wData[:,4])

#interpolated integrated values#
IcumNew = np.interp(hNew, hOrg, Icum)
add=0
IcumNew= np.append(add,IcumNew)

#determine new insolation and wind-speed values#
Ib = (IcumNew[1 : nNew+2] - IcumNew[0 : nNew]) * (nNew/nPoints)

#new ambient values#
Ta = np.interp(hNew, hOrg, wData[:,2])
Pa = np.interp(hNew, hOrg, wData[:,3])

#open/create input files#
fidW = open(wthFile, 'w+')
fidS = open(simFile, 'w+')



for i in range (0,len(hNew)):
    # write new weather data to input file#
    fidW.write(" %i %12.5f %12.5f %12.5f %12.5f %12.5f %12.5f\n" % (hNew[i], nDay[i],az[i], np.maximum(0,el[i]), np.maximum(0,Ib[i])*3.6, Ta[i]-273.15, Pa[i]/1e5))

#write sim information to file#
fidS.write("%0.8f\n" % model_hrSim)

#close all files#
fidW.close()
fidS.close()

