def completestates(PC_st, PC_n_states):
    from iapws import IAPWS97
    import numpy as np

    sz=np.shape(PC_st)

    Add_column= np.zeros(shape=(PC_n_states,1))
    PC_st= np.concatenate((PC_st, Add_column), axis=1)

    for k in range (1,sz[0]+1):

        Thermo_point= IAPWS97(P=PC_st[k-1,1]/10,x= 1)
        hV=Thermo_point.h

        Thermo2_point= IAPWS97(P=PC_st[k-1,1]/10, x=0)
        hL=Thermo2_point.h
        if PC_st[k-1,2]>hV:      #super heated steam

#         PC_st(k,5)=1;
#
#         PC_st(k,1)=XSteam ('T_ph',PC_st(k,2),PC_st(k,3));
#
#         PC_st(k,6)=XSteam ('v_ph',PC_st(k,2),PC_st(k,3));
#
#         PC_st(k,4)=XSteam ('s_ph',PC_st(k,2),PC_st(k,3));
#
#         PC_st(k,9)=XSteam ('Cp_ph',PC_st(k,2),PC_st(k,3));
#
#          PC_st(k,7)=XSteam('my_ph',PC_st(k,2),PC_st(k,3));
            Thermo3_point= IAPWS97(P= PC_st[k-1,1] /10, h= PC_st[k-1,2] +273.15)
            PC_st[k-1,9]=   Thermo3_point.k


        elif PC_st[k-1,2]<hL:               #  compressed liquid

# #         PC_st(k,5)=0;
# #
# #         PC_st(k,1)=XSteam ('T_ph',PC_st(k,2),PC_st(k,3));
# #
# #         PC_st(k,6)=XSteam ('v_ph',PC_st(k,2),PC_st(k,3));
# #
# #         PC_st(k,4)=XSteam ('s_ph',PC_st(k,2),PC_st(k,3));
# #
# #         PC_st(k,9)=XSteam ('Cp_ph',PC_st(k,2),PC_st(k,3));
# #
# #          PC_st(k,7)=XSteam('my_ph',PC_st(k,2),PC_st(k,3));
            Thermo4_point= IAPWS97(P=PC_st[k-1,1] /10, h=PC_st[k-1,2] )
            PC_st[k-1,9]= Thermo4_point.k

        else:        #saturation#
#
# #         PC_st(k,5)=(PC_st(k,3)-hL)/(hV-hL);
# #
# #         PC_st(k,1)=XSteam ('Tsat_p',PC_st(k,2));
# #
# #         PC_st(k,6)=PC_st(k,5)*XSteam('vV_p',PC_st(k,2))...
# #             +(1-PC_st(k,5))*XSteam('vL_p',PC_st(k,2));
# #
# #         PC_st(k,4)=PC_st(k,5)*XSteam('sV_p',PC_st(k,2))...
# #             +(1-PC_st(k,5))*XSteam('sL_p',PC_st(k,2));
# #
# #         PC_st(k,9)=PC_st(k,5)*XSteam('CpV_p',PC_st(k,2))...
# #             +(1-PC_st(k,5))*XSteam('CpL_p',PC_st(k,2));
# #
# #         PC_st(k,7)=PC_st(k,5)*XSteam('my_ph',PC_st(k,2),PC_st(k,3))...
# #             +(1-PC_st(k,5))*XSteam('my_ph',PC_st(k,2),PC_st(k,3));
#
            PC_st[k-1,9]=PC_st[k-1,4]*Thermo_point.k +(1-PC_st[k-1,4])*Thermo2_point.k

# #     PC_st_column={'T[degC]' 'P[bar]' 'h[kJ/kg]' 's[kJ/kg]' 'X[-]' 'v[m3/kg]' 'miu[kg/ms]' ...
# #                     'mdot[kg/s]' 'Cp[kJ/kg]' 'k[W/mK]'};
#
# end
    return[PC_st]
