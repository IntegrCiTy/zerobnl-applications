import importlib
import numpy as np

# Calculate UA
# --> PowerBlock
# Save UA in TRNSYS format
# --> prepareTRNSYSinput
# Print in CaseData
# --> here

TRNinp = importlib.import_module('prepareTRNSYSinput')

prepTRNSYSinp_attr   = dir(importlib.import_module('prepareTRNSYSinput'))

prepTRNSYSinp_list   = [s for s in prepTRNSYSinp_attr if "TRNSYS_" in s]

TRNSYSinp_ar         = np.array(prepTRNSYSinp_list)

#determine full input file name#
fileName = 'caseData.txt'

#load input structure fields#
inVars1 = TRNSYSinp_ar

nVars1 = len(inVars1)

#open/create input file#
fid = open(fileName, 'w+')

#print number of input variables#
fid.write('CONSTANTS %s\n' % (len(inVars1)))

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