def subcooler(Xhot,Xcold,Xhot_o):
    import numpy as np
    EFF = (Xhot[0] - Xhot_o[0])/(Xhot[0] - Xcold[0])
    CPH = Xhot[8]
    CPC = Xcold[8]
    CH = Xhot[7]*CPH
    CC = Xcold[7]*CPC
    FRcold = Xcold[7]
    CMAX = max(CH,CC)
    CMIN = min(CH,CC)
    RAT = CMIN/CMAX

    if RAT <1:
        NTU=(np.log((EFF - 1.0)/(EFF*RAT - 1.0)))/(RAT - 1.0)
    elif RAT ==1:
        NTU=EFF/(1-EFF)
    else:
        print('Non feasible counterflow HE, problem with Cr')
        
    UA=NTU*CMIN

    return[EFF, UA, CPH, CPC, FRcold]
#         if strcmp(o.HEStechnology,'DSG_STTP')==1
#
#                     CPH = CH;
#                     CPC = CC;
#
#         end
