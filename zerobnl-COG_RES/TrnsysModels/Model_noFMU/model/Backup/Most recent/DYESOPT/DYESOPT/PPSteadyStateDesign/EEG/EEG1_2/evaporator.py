def evaporator(Xhot_i,Xcold_i,Xhot_o):
    import numpy as np
    EFF = (Xhot_i[0] - Xhot_o[0])/(Xhot_i[0] - Xcold_i[0])
    CH  = Xhot_i[1]*Xhot_i[3]
    UA  = -1.0*CH*np.log(1.0 - 1.0*EFF)
    return [EFF, UA]
