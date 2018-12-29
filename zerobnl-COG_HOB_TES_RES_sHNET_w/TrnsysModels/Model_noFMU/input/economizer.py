def economizer(Xcold,Xhot,Xcold_o):
	import numpy as np
	from iapws import IAPWS97
	CPH     = Xhot[1]
	Thermo_point= IAPWS97(P= Xcold[1]/10, T= Xcold[0]+273.15) # MPa and K
	CPC     = Thermo_point.cp
	CH      = Xhot[3]*CPH
	CC      = Xcold[7]*CPC
	CMAX    = max(CH,CC)
	CMIN    = min(CH,CC)
	RAT     = CMIN/CMAX
	EFF     = (Xcold_o[0] - Xcold[0])/(Xhot[0] - Xcold[0])	
	UA      = (np.log((EFF - 1.0)/(EFF*RAT - 1.0))/(RAT - 1.0))*CMIN	
	return [EFF, UA]
