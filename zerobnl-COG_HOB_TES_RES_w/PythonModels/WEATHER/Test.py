import numpy as np
#from pyepw.epw import EPW
import pyepw.epw as pe

# epw = EPW()
epwi = pe.EPW()
epwi.read(r"SWE_Stockholm.Arlanda.024600_IWEC.epw")
VdryBulb = np.empty([8760])
jj=0
for wd in epwi.weatherdata:
	VdryBulb[jj] = wd.dry_bulb_temperature
	jj=jj+1

TdryBulb = 0.		
ii = 24 * 27

TdryBulb = VdryBulb[ii]		

print(TdryBulb)


TsetMatrix = np.loadtxt("TS_set.txt", comments='#', delimiter='\t', converters=None, skiprows=2, usecols=(0,1), unpack=False, ndmin=0)   

TsetP = np.interp(10,TsetMatrix[:,0],TsetMatrix[:,1])

print(TsetP)