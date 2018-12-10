def preheater(Xcold_o,Xcold,Xsat):

    from iapws import IAPWS97
    import DesignParameters.EEG1_2_Def_Par
    import numpy
    EFF = (Xcold_o[0] - Xcold[0])/(Xsat[0] - Xcold[0])
    Thermo_point= IAPWS97(P= Xcold[1]/10, T= Xcold[0]+273.15)
    UA = -(Thermo_point.cp0)*numpy.log(1-DesignParameters.EEG1_2_Def_Par.PC_PHeffCOEFF*EFF)*Xcold[7]
    CPC = Thermo_point.cp0
    FRcold = Xcold[7]


    return [EFF, UA, FRcold, CPC]
