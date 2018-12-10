import importlib
import numpy as np
import os
from Core.setModelLabel import *


TRNinp = importlib.import_module('DynSim&TEcalculations.ResFuel.HES3_1__TES0__EEG1_2__EES0.input.prepareTRNSYSinput')
TRNstd = importlib.import_module('Core.Interface.standardTRNSYSdata')

prepTRNSYSinp_attr   = dir(importlib.import_module('DynSim&TEcalculations.ResFuel.HES3_1__TES0__EEG1_2__EES0.input.prepareTRNSYSinput'))
standTRNSYSdata_attr = dir(importlib.import_module('Core.Interface.standardTRNSYSdata'))

prepTRNSYSinp_list   = [s for s in prepTRNSYSinp_attr if "TRNSYS_" in s]
standTRNSYSdata_list = [s for s in standTRNSYSdata_attr if "TRNSYS_" in s]

TRNSYSinp_ar         = np.array(prepTRNSYSinp_list)
TRNSYSdata_ar        = np.array(standTRNSYSdata_list)

#determine full input file name#
fileName = os.path.join('C:\DYESOPT\DYESOPT\DynSim&TEcalculations' , HESTech , model_plant  ,'input\caseData.txt')

#load input structure fields#
inVars1 = TRNSYSinp_ar
inVars2 = TRNSYSdata_ar

nVars1 = len(inVars1)
nVars2 = len(inVars2)

#open/create input file#
fid = open(fileName, 'w+')

#print number of input variables#
fid.write('CONSTANTS %s\n' % (len(inVars1)+ len(inVars2)))

for i in range (0,nVars2):
    #print input variable values#
    fid.write(" %10s = %35.8f " % (inVars2[i],getattr(TRNstd,inVars2[i])))
    if i < nVars2:
        fid.write('\n')
for i in range (0,nVars1):
    #print input variable values#
    fid.write(" %10s = %35.8f" % (inVars1[i],getattr(TRNinp,inVars1[i])))
    if i < nVars1-1:
        fid.write('\n')

fid.close()

# remove TRNSYS_ from all lines
f = open(fileName)
lines = f.readlines()
f.close()
f = open(fileName, 'w')
for line in lines[0]:
        f.write(line)
for line in lines[1:]:
        f.write(line[8:])
f.close()
