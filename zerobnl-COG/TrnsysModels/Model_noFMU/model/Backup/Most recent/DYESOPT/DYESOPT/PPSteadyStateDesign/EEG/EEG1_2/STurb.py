def STurb(Tin,Pin,m,PR,n):

    from iapws import IAPWS97

    import numpy as np

    if n < 5:

        PROP   = np.zeros(shape=(7))
        PROP[6]= 0
        PROP[1]= Pin
        PROP[0]= Tin
        state   = np.zeros(shape=(2,9))

        if PROP[1] == float('inf'):
            PROP=[float('NaN'),float('inf'),float('NaN'),float('NaN'),0,float('NaN'),float('NaN')]
            state[0,8] = float('NaN')
        elif PROP[1]== 0:
            PROP= [float('NaN'),0,float('NaN'),float('NaN'),1,float('NaN'),float('NaN')]
            state[0,8]= float('NaN')
            state[0,7] = 0
        elif np.isnan(PROP[1])== True:
            PROP= [float('NaN'),float('NaN'),float('NaN'),float('NaN'),1,float('NaN'),float('NaN')]
            state[0,8]= float('NaN')
            state[0,7]= float('NaN')
        else:
            if PROP[1]> 10:                                        # A work around to provide the right h value for both cases
                Thermo_point= IAPWS97(P=PROP[1]/10, T=(PROP[0]+273.15))
            else:
                Thermo_point= IAPWS97(P=PROP[1]/10, x=1)          #T=(PROP[0]+273.15), changed from identifying point by P and T to P and x to avoid confusion with wet steam same P and T
            PROP[2]= Thermo_point.h
            PROP[3]= Thermo_point.s
            PROP[4]= Thermo_point.x
            PROP[5]= Thermo_point.v
            PROP[6]= Thermo_point.u
            ## Cp calculated as an approximated value as the one in the source code calculated the Cp for saturated vapor for the vapor part (X) and Cp for saturated liquid for the liquid part (1-X)
            state[0,8] = Thermo_point.cp

        for i in range  (1,8,1):
            state[0,i-1] = PROP[i-1]


        if PROP[1]== float('inf') or PR == 0 or np.isnan(PR) == True or np.isnan(m) == True or m<0:
            state[0,7] = 0
            ETA = float('NaN')

        else:

            state[0,7] = m
            ETA = 0.5*((0.835 + 0.02*np.log(m*state[0,5])) + (0.835 + 0.02*np.log(m*state[0,5]*(PR**(1/1.32))))) - (4.536*((1-state[0,4])**2) + 0.0367*(1-state[0,4]))

        if PR == 0 or PR == float('inf'):
            state[1,1]= float('inf')

        elif np.isnan(PR) == True:
            state[1,1]= float('NaN')

        else:

            state[1,1] = state[0,1]/PR
        state[1,3] = state[0,3]
        PROP[6] = 0
        PROP[1] = state[1,1]
        PROP[3] = state[1,3]

        if PROP[1] == float('inf'):
            PROP=[float('NaN'),float('inf'),float('NaN'),float('NaN'),0,float('NaN'),float('NaN')]

        elif np.isnan(PROP[1])== True:
            PROP=[float('NaN'),float('NaN'),float('NaN'),float('NaN'),1,float('NaN'),float('NaN')]
        elif PROP[1]== 0:
            PROP= [float('NaN'),0,float('NaN'),float('NaN'),1,float('NaN'),float('NaN')]

        else:

            Thermo2_point= IAPWS97(P=PROP[1]/10, s=PROP[3])
            PROP[0]= Thermo2_point.T-273.15
            PROP[2]= Thermo2_point.h
            PROP[4]= Thermo2_point.x
            PROP[5]= Thermo2_point.v
            PROP[6]= Thermo2_point.u

        state[1,2] = PROP[2]
        state[1,2] = state[0,2] - ETA*(state[0,2] - state[1,2])
        PROP[6]=0
        PROP[1]=state[1,1]
        PROP[2]=state[1,2]

        if PROP[1]== float('inf'):
            PROP= [float('NaN'),float('inf'),float('NaN'),float('NaN'),1,float('NaN'),float('NaN')]
            state[1,8]= float('NaN')
            state[1,7] = float('NaN')
        elif PROP[1]== 0:
            PROP= [float('NaN'),0,float('NaN'),float('NaN'),1,float('NaN'),float('NaN')]
            state[1,8]= float('NaN')
            state[1,7] = 0
        elif np.isnan(PROP[1])== True:
            PROP=[float('NaN'),float('NaN'),float('NaN'),float('NaN'),1,float('NaN'),float('NaN')]
            state[1,8]= float('NaN')
            state[1,7]= float('NaN')
        elif np.isnan(PROP[2])== True:
            PROP=[PROP[1],float('NaN'),float('NaN'),float('NaN'),1,float('NaN'),float('NaN')]
        else:
            Thermo3_point= IAPWS97(P=PROP[1]/10, h=PROP[2])

            PROP[0]= Thermo3_point.T-273.15
            PROP[3]= Thermo3_point.s
            PROP[4]= Thermo3_point.x
            PROP[5]= Thermo3_point.v
            PROP[6]= Thermo3_point.u
            ## Cp calculated as an approximated value as the one in the source code calculated the Cp for saturated vapor for the vapor part (X) and Cp for saturated liquid for the liquid part (1-X)
            state[1,8] = Thermo3_point.cp0
            state[1,7] = m
        for i in range  (1,8,1):
            state[1,i-1] = PROP[i-1]



        W = m*(state[0,2] - state[1,2])

    elif n== 1:
        PROP[6]=0
        PROP[1]=Pin
        PROP[0]=Tin
        Thermo_point= IAPWS97(P=PROP[1]/10, T=PROP[0]+273.15)
        PROP[2]= Thermo_point.h
        PROP[3]= Thermo_point.s
        PROP[4]= Thermo_point.x
        PROP[5]= Thermo_point.v
        PROP[6]= Thermo_point.u
        state   = np.zeros(shape=(2,9))
        for i in range  (1,8,1):
            state[0,i-1] = PROP[i-1]

        ETA = 0
        W = 0


    return [state, ETA, W]
    # # elseif n == 2
    # #
    # # end
