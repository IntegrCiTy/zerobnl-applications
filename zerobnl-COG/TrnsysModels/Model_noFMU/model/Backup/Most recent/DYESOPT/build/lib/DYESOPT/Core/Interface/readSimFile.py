import os
import numpy as np
from Core.setModelLabel import *
from Core.setDefaultParameters import *
from model_Choice import *
HES_DP_module= importlib.import_module('DesignParameters.'+HESname+'_Def_Par')


#simulation data file#
simFile = os.path.join('C:\DYESOPT\DYESOPT\DynSim&TEcalculations' , HESTech , model_plant  ,'input\simData.txt')

#load data from file#
sim= np.loadtxt(simFile, comments='#', delimiter=',', converters=None, skiprows=4, usecols=None, unpack=False, ndmin=0)
model_hrSim=sim[0,0]
