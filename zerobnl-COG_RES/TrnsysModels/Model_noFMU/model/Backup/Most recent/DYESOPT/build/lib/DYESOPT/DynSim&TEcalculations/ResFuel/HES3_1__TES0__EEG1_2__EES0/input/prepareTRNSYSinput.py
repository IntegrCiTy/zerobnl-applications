import numpy as np
from PPSteadyStateDesign.EEG.EEG1_2.PowerBlock import *

## -------------------------- Steam Turbine ------------------------------#

#HPT1
TRNSYS_HPT1_Pi_dsgn     = PC_st[PC_keyst_HPTin_n_st-1,1]
TRNSYS_HPT1_Po_dsgn     = PC_st[PC_keyst_HPTin_n_st-1,1]/PC_HPT_pr[0]
TRNSYS_HPT1_FR_dsgn     = PC_st[PC_keyst_HPTin_n_st-1,7]*3600
TRNSYS_HPT1_ETA_dsgn    = PC_HPT_ETA[0,0]
TRNSYS_HPT1_bypass      = 1

TRNSYS_HPT1_Po          = PC_st[PC_keyst_HPTin_n_st+1-1,1]
TRNSYS_HPT1_FR          = PC_st[PC_keyst_HPTin_n_st-1,7]*3600
TRNSYS_HPT1_h           = PC_st[PC_keyst_HPTin_n_st-1,2]

if PC_n_hotPH > 1 or (PC_n_hotPH == 1 and PC_DeaLocatHP == 1):
    #HPT2 yes
    TRNSYS_HPT2_Pi_dsgn     = PC_st[PC_keyst_HPTin_n_st+2-1,1]
    TRNSYS_HPT2_Po_dsgn     = PC_st[PC_keyst_HPTin_n_st+2-1,1]/PC_HPT_pr[1]
    TRNSYS_HPT2_FR_dsgn     = PC_st[PC_keyst_HPTin_n_st+2-1,7]*3600
    TRNSYS_HPT2_ETA_dsgn    = PC_HPT_ETA[0,1]
    TRNSYS_HPT2_bypass      = 1

    TRNSYS_HPT2_Po          = PC_st[PC_keyst_HPTin_n_st+3-1,1]
    TRNSYS_HPT2_FR          = PC_st[PC_keyst_HPTin_n_st+2-1,7]*3600
    TRNSYS_HPT2_h           = PC_st[PC_keyst_HPTin_n_st+2-1,2]


#     if PC_n_hotPH == 2 && PC_DeaLocatHP == 1
#         #HPT3 yes
#         TRNSYS_HPT3_Pi_dsgn     = PC_st(PC_keyst.HPTin_n_st+4,2);
#         TRNSYS_HPT3_Po_dsgn     = PC_st(PC_keyst.HPTin_n_st+4,2)/PC_HPT.pr(3);
#         TRNSYS_HPT3_FR_dsgn     = PC_st(PC_keyst.HPTin_n_st+4,8)*3600;
#         TRNSYS_HPT3_ETA_dsgn    = PC_HPT.ETA(3);
#         TRNSYS_HPT3_bypass      = 1;
#
#         TRNSYS_HPT3_Po          = PC_st(PC_keyst.HPTin_n_st+5,2);
#         TRNSYS_HPT3_FR          = PC_st(PC_keyst.HPTin_n_st+4,8)*3600;
#         TRNSYS_HPT3_h           = PC_st(PC_keyst.HPTin_n_st+4,3);
#
#     else
#         #HPT3 no
#         TRNSYS_HPT3_Pi_dsgn     = PC_st(PC_keyst.HPTin_n_st,2);
#         TRNSYS_HPT3_Po_dsgn     = PC_st(PC_keyst.HPTin_n_st,2)/PC_HPT.pr(2);
#         TRNSYS_HPT3_FR_dsgn     = PC_st(PC_keyst.HPTin_n_st,8)*3600;
#         TRNSYS_HPT3_ETA_dsgn    = PC_HPT.ETA(1);
#         TRNSYS_HPT3_bypass      = 0;
#
#         TRNSYS_HPT3_Po          = PC_st(PC_keyst.HPTin_n_st+1,2);
#         TRNSYS_HPT3_FR          = PC_st(PC_keyst.HPTin_n_st,8)*3600;
#         TRNSYS_HPT3_h           = PC_st(PC_keyst.HPTin_n_st,3);
#     end
#
# else
#     #HPT2 no
#     TRNSYS_HPT2_Pi_dsgn     = PC_st(PC_keyst.HPTin_n_st+2,2);
#     TRNSYS_HPT2_Po_dsgn     = PC_st(PC_keyst.HPTin_n_st+2,2)/PC_HPT.pr(2);
#     TRNSYS_HPT2_FR_dsgn     = PC_st(PC_keyst.HPTin_n_st+2,8)*3600;
#     TRNSYS_HPT2_ETA_dsgn    = PC_HPT.ETA(2);
#     TRNSYS_HPT2_bypass      = 0;
#
#     TRNSYS_HPT2_Po          = PC_st(PC_keyst.HPTin_n_st+3,2);
#     TRNSYS_HPT2_FR          = PC_st(PC_keyst.HPTin_n_st+2,8)*3600;
#     TRNSYS_HPT2_h           = PC_st(PC_keyst.HPTin_n_st+2,3);
#
#         #HPT3 no
#         TRNSYS_HPT3_Pi_dsgn     = PC_st(PC_keyst.HPTin_n_st,2);
#         TRNSYS_HPT3_Po_dsgn     = PC_st(PC_keyst.HPTin_n_st,2)/PC_HPT.pr(2);
#         TRNSYS_HPT3_FR_dsgn     = PC_st(PC_keyst.HPTin_n_st,8)*3600;
#         TRNSYS_HPT3_ETA_dsgn    = PC_HPT.ETA(1);
#         TRNSYS_HPT3_bypass      = 0;
#
#         TRNSYS_HPT3_Po          = PC_st(PC_keyst.HPTin_n_st+1,2);
#         TRNSYS_HPT3_FR          = PC_st(PC_keyst.HPTin_n_st,8)*3600;
#         TRNSYS_HPT3_h           = PC_st(PC_keyst.HPTin_n_st,3);
# end

if PC_DeaLocatHP == 0:
    #LPT1 (IPT]
    TRNSYS_IPT_Pi_dsgn     = PC_st[PC_keyst_IPTin_n_st-1,1]
    TRNSYS_IPT_Po_dsgn     = PC_st[PC_keyst_IPTin_n_st+1-1,1]
    TRNSYS_IPT_FR_dsgn     = PC_st[PC_keyst_IPTin_n_st-1,7]*3600
    TRNSYS_IPT_ETA_dsgn    = PC_IPT_ETA
    TRNSYS_IPT_bypass      = 1

    TRNSYS_IPT_Po          = PC_st[PC_keyst_IPTin_n_st+1-1,1]
    TRNSYS_IPT_FR          = PC_st[PC_keyst_IPTin_n_st-1,7]*3600
    TRNSYS_IPT_h           = PC_st[PC_keyst_IPTin_n_st-1,2]



#LPT1
TRNSYS_LPT1_Pi_dsgn     = PC_st[PC_keyst_LPTin_n_st-1,1]
TRNSYS_LPT1_Po_dsgn     = PC_st[PC_keyst_LPTin_n_st+1-1,1]
TRNSYS_LPT1_FR_dsgn     = PC_st[PC_keyst_LPTin_n_st-1,7]*3600
TRNSYS_LPT1_ETA_dsgn    = PC_LPT_ETA[0,0]
TRNSYS_LPT1_bypass      = 1

TRNSYS_LPT1_Po          = PC_st[PC_keyst_LPTin_n_st+1-1,1]
TRNSYS_LPT1_FR          = PC_st[PC_keyst_LPTin_n_st-1,7]*3600
TRNSYS_LPT1_h           = PC_st[PC_keyst_LPTin_n_st-1,1]

if PC_n_coldPH > 0:
    #LPT2 yes
    TRNSYS_LPT2_Pi_dsgn     = PC_st[PC_keyst_LPTin_n_st+2-1,1]
    TRNSYS_LPT2_Po_dsgn     = PC_st[PC_keyst_LPTin_n_st+3-1,1]
    TRNSYS_LPT2_FR_dsgn     = PC_st[PC_keyst_LPTin_n_st+2-1,7]*3600
    TRNSYS_LPT2_ETA_dsgn    = PC_LPT_ETA[0,1]
    TRNSYS_LPT2_bypass      = 1

    TRNSYS_LPT2_Po          = PC_st[PC_keyst_LPTin_n_st+3-1,1]
    TRNSYS_LPT2_FR          = PC_st[PC_keyst_LPTin_n_st+2-1,7]*3600
    TRNSYS_LPT2_h           = PC_st[PC_keyst_LPTin_n_st+2-1,2]

#     if PC_n_coldPH > 1
#         #LPT3 yes
#         TRNSYS_LPT3_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+4,2);
#         TRNSYS_LPT3_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+5,2);
#         TRNSYS_LPT3_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+4,8)*3600;
#         TRNSYS_LPT3_ETA_dsgn    = PC_LPT.ETA(3);
#         TRNSYS_LPT3_bypass      = 1;
#
#         TRNSYS_LPT3_Po          = PC_st(PC_keyst.LPTin_n_st+5,2);
#         TRNSYS_LPT3_FR          = PC_st(PC_keyst.LPTin_n_st+4,8)*3600;
#         TRNSYS_LPT3_h           = PC_st(PC_keyst.LPTin_n_st+4,3);
#
#         if PC_n_coldPH > 2
#             #LPT4 yes
#             TRNSYS_LPT4_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+6,2);
#             TRNSYS_LPT4_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+7,2);
#             TRNSYS_LPT4_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+6,8)*3600;
#             TRNSYS_LPT4_ETA_dsgn    = PC_LPT.ETA(4);
#             TRNSYS_LPT4_bypass      = 1;
#
#             TRNSYS_LPT4_Po          = PC_st(PC_keyst.LPTin_n_st+7,2);
#             TRNSYS_LPT4_FR          = PC_st(PC_keyst.LPTin_n_st+6,8)*3600;
#             TRNSYS_LPT4_h           = PC_st(PC_keyst.LPTin_n_st+6,3);
#
#             if PC_DoubleCond == 1
#                 #LPT5 yes
#                 TRNSYS_LPT5_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,2);
#                 TRNSYS_LPT5_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+9,2);
#                 TRNSYS_LPT5_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,8)*3600;
#                 TRNSYS_LPT5_ETA_dsgn    = PC_LPT.ETA(5);
#                 TRNSYS_LPT5_bypass      = 1;
#
#                 TRNSYS_LPT5_Po          = PC_st(PC_keyst.LPTin_n_st+9,2);
#                 TRNSYS_LPT5_FR          = PC_st(PC_keyst.LPTin_n_st+7,8)*3600;
#                 TRNSYS_LPT5_h           = PC_st(PC_keyst.LPTin_n_st+7,3);
#             else
#                 #LPT5 no
#                 TRNSYS_LPT5_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,2);
#                 TRNSYS_LPT5_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+9,2);
#                 TRNSYS_LPT5_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,8)*3600;
#                 TRNSYS_LPT5_ETA_dsgn    = PC_LPT.ETA(5);
#                 TRNSYS_LPT5_bypass      = 0;
#
#                 TRNSYS_LPT5_Po          = PC_st(PC_keyst.LPTin_n_st+9,2);
#                 TRNSYS_LPT5_FR          = PC_st(PC_keyst.LPTin_n_st+7,8)*3600;
#                 TRNSYS_LPT5_h           = PC_st(PC_keyst.LPTin_n_st+7,3);
#             end
#
#         else
#             if PC_DoubleCond == 1
#                 #LPT4 yes
#                 TRNSYS_LPT4_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+6,2);
#                 TRNSYS_LPT4_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+7,2);
#                 TRNSYS_LPT4_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+6,8)*3600;
#                 TRNSYS_LPT4_ETA_dsgn    = PC_LPT.ETA(4);
#                 TRNSYS_LPT4_bypass      = 1;
#
#                 TRNSYS_LPT4_Po          = PC_st(PC_keyst.LPTin_n_st+7,2);
#                 TRNSYS_LPT4_FR          = PC_st(PC_keyst.LPTin_n_st+6,8)*3600;
#                 TRNSYS_LPT4_h           = PC_st(PC_keyst.LPTin_n_st+6,3);
#                 #LPT5 no
#                 TRNSYS_LPT5_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,2);
#                 TRNSYS_LPT5_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+9,2);
#                 TRNSYS_LPT5_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,8)*3600;
#                 TRNSYS_LPT5_ETA_dsgn    = PC_LPT.ETA(5);
#                 TRNSYS_LPT5_bypass      = 0;
#
#                 TRNSYS_LPT5_Po          = PC_st(PC_keyst.LPTin_n_st+9,2);
#                 TRNSYS_LPT5_FR          = PC_st(PC_keyst.LPTin_n_st+7,8)*3600;
#                 TRNSYS_LPT5_h           = PC_st(PC_keyst.LPTin_n_st+7,3);
#             else
#                 #LPT4 no
#                 TRNSYS_LPT4_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+6,2);
#                 TRNSYS_LPT4_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+7,2);
#                 TRNSYS_LPT4_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+6,8)*3600;
#                 TRNSYS_LPT4_ETA_dsgn    = PC_LPT.ETA(4);
#                 TRNSYS_LPT4_bypass      = 0;
#
#                 TRNSYS_LPT4_Po          = PC_st(PC_keyst.LPTin_n_st+7,2);
#                 TRNSYS_LPT4_FR          = PC_st(PC_keyst.LPTin_n_st+6,8)*3600;
#                 TRNSYS_LPT4_h           = PC_st(PC_keyst.LPTin_n_st+6,3);
#
#                 #LPT5 no
#                 TRNSYS_LPT5_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,2);
#                 TRNSYS_LPT5_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+9,2);
#                 TRNSYS_LPT5_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,8)*3600;
#                 TRNSYS_LPT5_ETA_dsgn    = PC_LPT.ETA(5);
#                 TRNSYS_LPT5_bypass      = 0;
#
#                 TRNSYS_LPT5_Po          = PC_st(PC_keyst.LPTin_n_st+9,2);
#                 TRNSYS_LPT5_FR          = PC_st(PC_keyst.LPTin_n_st+7,8)*3600;
#                 TRNSYS_LPT5_h           = PC_st(PC_keyst.LPTin_n_st+7,3);
#             end
#         end
#     else
        #LPT2 yes
    if PC_DoubleCond == 1:
        #LPT3 yes
        TRNSYS_LPT3_Pi_dsgn     = PC_st[PC_keyst_LPTin_n_st+4+PC_DeaLP-1,1]
        TRNSYS_LPT3_Po_dsgn     = PC_st[PC_keyst_LPTin_n_st+5+PC_DeaLP-1,1]
        TRNSYS_LPT3_FR_dsgn     = PC_st[PC_keyst_LPTin_n_st+4+PC_DeaLP-1,7]*3600
        TRNSYS_LPT3_ETA_dsgn    = PC_LPT_ETA[0,2]
        TRNSYS_LPT3_bypass      = 1

        TRNSYS_LPT3_Po          = PC_st[PC_keyst_LPTin_n_st+5+PC_DeaLP-1,1]
        TRNSYS_LPT3_FR          = PC_st[PC_keyst_LPTin_n_st+4+PC_DeaLP-1,7]*3600
        TRNSYS_LPT3_h           = PC_st[PC_keyst_LPTin_n_st+4+PC_DeaLP-1,2]

#                 #LPT4 no
#                 TRNSYS_LPT4_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+6,2);
#                 TRNSYS_LPT4_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+7,2);
#                 TRNSYS_LPT4_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+6,8)*3600;
#                 TRNSYS_LPT4_ETA_dsgn    = PC_LPT.ETA(4);
#                 TRNSYS_LPT4_bypass      = 0;
#
#                 TRNSYS_LPT4_Po          = PC_st(PC_keyst.LPTin_n_st+7,2);
#                 TRNSYS_LPT4_FR          = PC_st(PC_keyst.LPTin_n_st+6,8)*3600;
#                 TRNSYS_LPT4_h           = PC_st(PC_keyst.LPTin_n_st+6,3);
#
#                 #LPT5 no
#                 TRNSYS_LPT5_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,2);
#                 TRNSYS_LPT5_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+9,2);
#                 TRNSYS_LPT5_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,8)*3600;
#                 TRNSYS_LPT5_ETA_dsgn    = PC_LPT.ETA(5);
#                 TRNSYS_LPT5_bypass      = 0;
#
#                 TRNSYS_LPT5_Po          = PC_st(PC_keyst.LPTin_n_st+9,2);
#                 TRNSYS_LPT5_FR          = PC_st(PC_keyst.LPTin_n_st+7,8)*3600;
#                 TRNSYS_LPT5_h           = PC_st(PC_keyst.LPTin_n_st+7,3);
#
#         else
#             #LPT3 no
#             TRNSYS_LPT3_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+4+PC_DeaLP,2);
#             TRNSYS_LPT3_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+5+PC_DeaLP,2);
#             TRNSYS_LPT3_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+4+PC_DeaLP,8)*3600;
#             TRNSYS_LPT3_ETA_dsgn    = PC_LPT.ETA(3);
#             TRNSYS_LPT3_bypass      = 0;
#
#             TRNSYS_LPT3_Po          = PC_st(PC_keyst.LPTin_n_st+5+PC_DeaLP,2);
#             TRNSYS_LPT3_FR          = PC_st(PC_keyst.LPTin_n_st+4+PC_DeaLP,8)*3600;
#             TRNSYS_LPT3_h           = PC_st(PC_keyst.LPTin_n_st+4+PC_DeaLP,3);
#
#                 #LPT4 no
#                 TRNSYS_LPT4_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+6,2);
#                 TRNSYS_LPT4_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+7,2);
#                 TRNSYS_LPT4_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+6,8)*3600;
#                 TRNSYS_LPT4_ETA_dsgn    = PC_LPT.ETA(4);
#                 TRNSYS_LPT4_bypass      = 0;
#
#                 TRNSYS_LPT4_Po          = PC_st(PC_keyst.LPTin_n_st+7,2);
#                 TRNSYS_LPT4_FR          = PC_st(PC_keyst.LPTin_n_st+6,8)*3600;
#                 TRNSYS_LPT4_h           = PC_st(PC_keyst.LPTin_n_st+6,3);
#
#                 #LPT5 no
#                 TRNSYS_LPT5_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,2);
#                 TRNSYS_LPT5_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+9,2);
#                 TRNSYS_LPT5_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,8)*3600;
#                 TRNSYS_LPT5_ETA_dsgn    = PC_LPT.ETA(5);
#                 TRNSYS_LPT5_bypass      = 0;
#
#                 TRNSYS_LPT5_Po          = PC_st(PC_keyst.LPTin_n_st+9,2);
#                 TRNSYS_LPT5_FR          = PC_st(PC_keyst.LPTin_n_st+7,8)*3600;
#                 TRNSYS_LPT5_h           = PC_st(PC_keyst.LPTin_n_st+7,3);

#     end
#
#  else
#     #LPT1 yes
#     if PC_DoubleCond == 1
#         #LPT2 yes
#         TRNSYS_LPT2_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+2,2);
#         TRNSYS_LPT2_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+3,2);
#         TRNSYS_LPT2_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+2,8)*3600;
#         TRNSYS_LPT2_ETA_dsgn    = PC_LPT.ETA(2);
#         TRNSYS_LPT2_bypass      = 1;
#
#         TRNSYS_LPT2_Po          = PC_st(PC_keyst.LPTin_n_st+3,2);
#         TRNSYS_LPT2_FR          = PC_st(PC_keyst.LPTin_n_st+2,8)*3600;
#         TRNSYS_LPT2_h           = PC_st(PC_keyst.LPTin_n_st+2,3);
#
#
#             #LPT3 no
#             TRNSYS_LPT3_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+4+PC_DeaLP,2);
#             TRNSYS_LPT3_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+5+PC_DeaLP,2);
#             TRNSYS_LPT3_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+4+PC_DeaLP,8)*3600;
#             TRNSYS_LPT3_ETA_dsgn    = PC_LPT.ETA(3);
#             TRNSYS_LPT3_bypass      = 0;
#
#             TRNSYS_LPT3_Po          = PC_st(PC_keyst.LPTin_n_st+5+PC_DeaLP,2);
#             TRNSYS_LPT3_FR          = PC_st(PC_keyst.LPTin_n_st+4+PC_DeaLP,8)*3600;
#             TRNSYS_LPT3_h           = PC_st(PC_keyst.LPTin_n_st+4+PC_DeaLP,3);
#
#                 #LPT4 no
#                 TRNSYS_LPT4_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+6,2);
#                 TRNSYS_LPT4_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+7,2);
#                 TRNSYS_LPT4_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+6,8)*3600;
#                 TRNSYS_LPT4_ETA_dsgn    = PC_LPT.ETA(4);
#                 TRNSYS_LPT4_bypass      = 0;
#
#                 TRNSYS_LPT4_Po          = PC_st(PC_keyst.LPTin_n_st+7,2);
#                 TRNSYS_LPT4_FR          = PC_st(PC_keyst.LPTin_n_st+6,8)*3600;
#                 TRNSYS_LPT4_h           = PC_st(PC_keyst.LPTin_n_st+6,3);
#
#                 #LPT5 no
#                 TRNSYS_LPT5_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,2);
#                 TRNSYS_LPT5_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+9,2);
#                 TRNSYS_LPT5_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,8)*3600;
#                 TRNSYS_LPT5_ETA_dsgn    = PC_LPT.ETA(5);
#                 TRNSYS_LPT5_bypass      = 0;
#
#                 TRNSYS_LPT5_Po          = PC_st(PC_keyst.LPTin_n_st+9,2);
#                 TRNSYS_LPT5_FR          = PC_st(PC_keyst.LPTin_n_st+7,8)*3600;
#                 TRNSYS_LPT5_h           = PC_st(PC_keyst.LPTin_n_st+7,3);
#     else
#         #LPT2 no
#         TRNSYS_LPT2_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+2,2);
#         TRNSYS_LPT2_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+3,2);
#         TRNSYS_LPT2_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+2,8)*3600;
#         TRNSYS_LPT2_ETA_dsgn    = PC_LPT.ETA(2);
#         TRNSYS_LPT2_bypass      = 0;
#
#         TRNSYS_LPT2_Po          = PC_st(PC_keyst.LPTin_n_st+3,2);
#         TRNSYS_LPT2_FR          = PC_st(PC_keyst.LPTin_n_st+2,8)*3600;
#         TRNSYS_LPT2_h           = PC_st(PC_keyst.LPTin_n_st+2,3);
#                 #LPT3 no
#                 TRNSYS_LPT3_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+4+PC_DeaLP,2);
#                 TRNSYS_LPT3_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+5+PC_DeaLP,2);
#                 TRNSYS_LPT3_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+4+PC_DeaLP,8)*3600;
#                 TRNSYS_LPT3_ETA_dsgn    = PC_LPT.ETA(3);
#                 TRNSYS_LPT3_bypass      = 0;
#
#                 TRNSYS_LPT3_Po          = PC_st(PC_keyst.LPTin_n_st+5+PC_DeaLP,2);
#                 TRNSYS_LPT3_FR          = PC_st(PC_keyst.LPTin_n_st+4+PC_DeaLP,8)*3600;
#                 TRNSYS_LPT3_h           = PC_st(PC_keyst.LPTin_n_st+4+PC_DeaLP,3);
#
#                     #LPT4 no
#                     TRNSYS_LPT4_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+6,2);
#                     TRNSYS_LPT4_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+7,2);
#                     TRNSYS_LPT4_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+6,8)*3600;
#                     TRNSYS_LPT4_ETA_dsgn    = PC_LPT.ETA(4);
#                     TRNSYS_LPT4_bypass      = 0;
#
#                     TRNSYS_LPT4_Po          = PC_st(PC_keyst.LPTin_n_st+7,2);
#                     TRNSYS_LPT4_FR          = PC_st(PC_keyst.LPTin_n_st+6,8)*3600;
#                     TRNSYS_LPT4_h           = PC_st(PC_keyst.LPTin_n_st+6,3);
#
#                     #LPT5 no
#                     TRNSYS_LPT5_Pi_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,2);
#                     TRNSYS_LPT5_Po_dsgn     = PC_st(PC_keyst.LPTin_n_st+9,2);
#                     TRNSYS_LPT5_FR_dsgn     = PC_st(PC_keyst.LPTin_n_st+8,8)*3600;
#                     TRNSYS_LPT5_ETA_dsgn    = PC_LPT.ETA(5);
#                     TRNSYS_LPT5_bypass      = 0;
#
#                     TRNSYS_LPT5_Po          = PC_st(PC_keyst.LPTin_n_st+9,2);
#                     TRNSYS_LPT5_FR          = PC_st(PC_keyst.LPTin_n_st+7,8)*3600;
#                     TRNSYS_LPT5_h           = PC_st(PC_keyst.LPTin_n_st+7,3);
#
#     end




## Boiler

TRNSYS_Boiler_Q     = PC_ECO_Q + PC_EV_Q + PC_SH_Q

TRNSYS_Boiler_h_out = PC_st[PC_keyst_HPTin_n_st-1,2]

TRNSYS_Boiler_Fuel  = Fuel_LHV

if PC_RHpresence == 1:

    TRNSYS_ReHeat_Q           = PC_RH_Q

    TRNSYS_ReHeat_h_out       = PC_st[PC_keyst_HPTin_n_st-1,2]

    TRNSYS_ReHeat_Pdrop       = PC_RH_dP

# #         ## ------------------------ DSG Receivers -------------------------------#
# #         #Superheater
# #         TRNSYS_SH_Qin_dsgn            =                 o.rec.SH.Qin;
# #         TRNSYS_SH_Qloss_dsgn   =                o.rec.SH.Qloss_total;
# #         TRNSYS_SH_PdSH_dsgn      =                        PC_SH.dP;
# #         TRNSYS_SH_mdot_dsgn         =                      PC_mdot;
# #         TRNSYS_SH_Qinmin_dsgn            = o.rec.SH.Qin*o.rec.Qminfrac;#2.6200e+06;#2.9943e+06;#4.1920e+06;#5.2400e+06;#5.8223e+06;#6.9867e+06;# 8.7334e+06;#1.0480e+07;
# #         TRNSYS_SH_MaxheatFlux_dsgn   =                         300000;
# #         TRNSYS_SH_Arec_dsgn      =                      o.rec.SH.Arec;
# #         TRNSYS_SH_Tatemp_dsgn      =                      PC_TinHPT;
# #         TRNSYS_SH_mode_dsgn      =                                 1;
# #
# #         TRNSYS_SH_Tin=            PC_st(PC_keyst.HPTin_n_st-1,1);
# #         TRNSYS_SH_PinTurb=          PC_st(PC_keyst.HPTin_n_st,2);
# #         TRNSYS_SH_Qin=                                  o.rec.SH.Qin;
# #         TRNSYS_SH_mdot=                                    PC_mdot;
# #
# #         #Evaporator
# #         TRNSYS_EV_Qin_dsgn            =                 o.rec.EV.Qin;
# #         TRNSYS_EV_Qloss_dsgn   =                o.rec.EV.Qloss_total;
# #         TRNSYS_EV_PdropSH_dsgn      =                     PC_SH.dP;
# #         TRNSYS_EV_PdropEV_dsgn      =                     PC_EV.dP;
# #         TRNSYS_EV_mdot_dsgn         =                      PC_mdot;
# #         TRNSYS_EV_Qinmin_dsgn            =                o.rec.EV.Qin*o.rec.Qminfrac;#4.2089e+06;#4.8101e+06;#6.7342e+06;#8.4177e+06;#9.3530e+06;#1.1224e+07;#1.4030e+07;#1.6835e+07;
# #         TRNSYS_EV_MaxheatFlux_dsgn   =                         650000;
# #         TRNSYS_EV_Arec_dsgn      =                      o.rec.EV.Arec;
# #
# #         TRNSYS_EV_Tin=             PC_st(PC_keyst.HPTin_n_st-2,1);
# #         TRNSYS_EV_PinTurb=           PC_st(PC_keyst.HPTin_n_st,2);
# #         TRNSYS_EV_Qin=                                  o.rec.EV.Qin;
# #
# #         #Reheater
# #         TRNSYS_RH_Qin_dsgn            =                     o.rec.RH.Qin;
# #         TRNSYS_RH_Qloss_dsgn   =                    o.rec.RH.Qloss_total;
# #         TRNSYS_RH_PdropRH_dsgn      =                         PC_RH.dP;
# #         TRNSYS_RH_mdot_dsgn         =   PC_st(PC_keyst.IPTin_n_st-1,8);
# #         TRNSYS_RH_Qinmin_dsgn            =                    o.rec.RH.Qin*o.rec.Qminfrac;#9.6748e+05;#1.1057e+06;#1.5480e+06;#1.9350e+06;#2.1500e+06;#2.5800e+06;#3.2249e+06;#3.8699e+06;
# #         TRNSYS_RH_MaxheatFlux_dsgn   =                         300000;
# #         TRNSYS_RH_Arec_dsgn      =                      o.rec.RH.Arec;
# #         TRNSYS_RH_Tatemp_dsgn      = PC_st(PC_keyst.IPTin_n_st,1);
# #         TRNSYS_RH_mode_dsgn      =                                 2;
# #
# #         TRNSYS_RH_PinTurb=          PC_st(PC_keyst.IPTin_n_st,2);
# #         TRNSYS_RH_Qin=                                  o.rec.RH.Qin;
# #         TRNSYS_RH_mdot=           PC_st(PC_keyst.IPTin_n_st-1,8);
# #         TRNSYS_RH_hin=            PC_st(PC_keyst.IPTin_n_st-1,3);
#
#
## ---------------------------- PUMPS ------------------------------------#
if PC_PumpBeforeMix == 0:
    #PUMP 1
    TRNSYS_PUMP1_mode       = 2
    TRNSYS_PUMP1_Pin        = PC_st[0,1]
    TRNSYS_PUMP1_ro         = 1000
    TRNSYS_PUMP1_ETA        = PC_COND_Pump_EFF
    TRNSYS_PUMP1_W          = PC_COND_Pump_Power*3600            #kJ/hr
else:
    TRNSYS_PUMP_befmix_mode       = 2
    TRNSYS_PUMP_befmix_Pin        = PC_st[0,1]
    TRNSYS_PUMP_befmix_ro         = 1000
    TRNSYS_PUMP_befmix_ETA        = PC_Pump_Eff
    TRNSYS_PUMP_befmix_W          = PC_PumpBefMix_Power*3600     #kJ/hr


if PC_DeaLP == 1:
    TRNSYS_PUMP_dealp_mode       = 2
    TRNSYS_PUMP_dealp_Pin        = PC_st[(PC_keyst_LPTout_n_st+PC_n_hotPH+1+PC_n_coldPH+PC_DeaLP)-1,1]
    TRNSYS_PUMP_dealp_ro         = 1000
    TRNSYS_PUMP_dealp_ETA        = PC_Pump_Eff
    TRNSYS_PUMP_dealp_W          = PC_PUMP_W_DeaLP*3600 #kJ/hr

#PUMP 2
TRNSYS_PUMP2_mode       = 2
TRNSYS_PUMP2_Pin        = PC_st[PC_keyst_DEAin_n_st+1-1,1]
TRNSYS_PUMP2_ro         = 1000
TRNSYS_PUMP2_ETA        = PC_Pump_Eff
TRNSYS_PUMP2_W          = PC_PUMP_W2*3600 #kJ/hr


## -------------------------- SUBCOOLERS ---------------------------------#
#HE1
TRNSYS_HE1_UA           = PC_hotSC[0,1]*3600
TRNSYS_HE1_Cp_hot       = np.minimum(PC_hotSC[0,2],PC_hotSC[0,3])
TRNSYS_HE1_CP_cold      = np.maximum(PC_hotSC[0,2],PC_hotSC[0,3])
TRNSYS_HE1_FRref_cold   = PC_st[PC_keyst_DEAin_n_st+1-1,7]*3600

# #         #HE2
# #         TRNSYS_HE2_UA           = PC_hotSC(2,2)*3600;
# #         TRNSYS_HE2_Cp_hot       = min(PC_hotSC(2,3),PC_hotSC(2,4))/(PC_st(PC_keyst.LPTout_n_st+2,8));
# #         TRNSYS_HE2_CP_cold      = max(PC_hotSC(2,3),PC_hotSC(2,4))/(PC_mdot);
# #         TRNSYS_HE2_FRref_cold   = PC_mdot*3600;

#---COLD-----#
#HE3
TRNSYS_HE3_UA           = PC_coldSC[0,1]*3600
TRNSYS_HE3_Cp_hot       = np.minimum(PC_coldSC[0,2],PC_coldSC[0,3])
TRNSYS_HE3_CP_cold      = np.maximum(PC_coldSC[0,2],PC_coldSC[0,3])
TRNSYS_HE3_FRref_cold   = PC_st[PC_keyst_DEAin_n_st-1,7]*3600

# #         #HE4
# #         TRNSYS_HE4_UA           = PC_coldSC(2,2)*3600;
# #         TRNSYS_HE4_Cp_hot       = min(PC_coldSC(2,3),PC_coldSC(2,4))/(PC_st(PC_keyst.LPTout_n_st+4,8));
# #         TRNSYS_HE4_CP_cold      = max(PC_coldSC(2,3),PC_coldSC(2,4))/(PC_st(PC_keyst.DEAin_n_st,8));
# #         TRNSYS_HE4_FRref_cold   = PC_st(PC_keyst.DEAin_n_st,8)*3600;
#
## -------------------------- PREHEATERS ---------------------------------#

#PH1
TRNSYS_PH1_Cp_cold      = PC_hotPH[0,3]
TRNSYS_PH1_UA           = PC_hotPH[0,1]*3600
TRNSYS_PH1_FRref_cold   = PC_st[PC_keyst_DEAin_n_st+1-1,7]*3600
TRNSYS_PH1_onoff        = 1

# #          #PH2
# #         TRNSYS_PH2_Cp_cold      = PC_hotPH(2,4);
# #         TRNSYS_PH2_UA           = PC_hotPH(2,2)*3600;
# #         TRNSYS_PH2_FRref_cold   = PC_mdot*3600;
# #         TRNSYS_PH2_onoff        = 1;

#---COLD----#
#PH3
TRNSYS_PH3_Cp_cold      = PC_coldPH[0,3]
TRNSYS_PH3_UA           = PC_coldPH[0,1]*3600
TRNSYS_PH3_FRref_cold   = PC_st[PC_keyst_DEAin_n_st-1,7]*3600
TRNSYS_PH3_onoff        = 1

# #         #PH4
# #         TRNSYS_PH4_Cp_cold      = PC_coldPH(2,4);
# #         TRNSYS_PH4_UA           =  PC_coldPH(2,2)*3600;
# #         TRNSYS_PH4_FRref_cold   = PC_st(PC_keyst.DEAin_n_st,8)*3600;
# #         TRNSYS_PH4_onoff        = 1;


## -------------------- Deaerator & Condenser ----------------------------#

#Deaerator

#Condenser

if PC_PCONDset != 3:
    TRNSYS_CND_UAref    =     PC_COND_UA*3600


    TRNSYS_CND_Ttarget   = PC_COND_Tcout
    TRNSYS_CND_Pmax       = PC_COND_fan_Power*3600
    TRNSYS_CND_TTDref    = PC_COND_dTapp
    TRNSYS_CND_UAexp        = 1
    TRNSYS_CND_FRamax       = PC_COND_air_FR*3600

    TRNSYS_CND_Hin=   PC_st[PC_keyst_LPTout_n_st-1,2]
    TRNSYS_CND_FRcond= PC_st[PC_keyst_LPTout_n_st-1,7]*3600
    TRNSYS_CND_Tair_in= design_Tamb   ###OSAMA--> Should be fixed in design power plant first, as it is avoided by having a 7th design mode
    TRNSYS_CND_Tin=  PC_st[PC_keyst_LPTout_n_st-1,0]

elif PC_PCONDset == 3:

    if PC_DoubleCond == 1:

#         TRNSYS_dT_WtrOutCond_1 = PC_dT_wtr_out_condensing;
#
#         TRNSYS_dT_water_DH_1 = o.APPROACH_COND1;
#
#         #second condenser as a preheater
#         TRNSYS_PHdh_Cp_cold      = PC_COND2.DH_PH(1,4);
#         TRNSYS_PHdh_UA           = PC_COND2.DH_PH(1,2)*3600;
#         TRNSYS_PHdh_FRref_cold   = PC_DH_massflow*3600;
#         TRNSYS_PHdh_onoff        = 1;
#
#     end


        TRNSYS_UA_COND2       = PC_COND2_UA_DELTA*3600

        TRNSYS_DH_massflow   = PC_DH_massflow

        TRNSYS_DH_T_out_COND1  = PC_DH_T_return + APPROACH_COND1

        TRNSYS_DH_T_in_COND1 = PC_DH_T_return



        TRNSYS_DH_T_out_COND2 = PC_DH_T_supply

        TRNSYS_DH_T_in_COND2 = PC_DH_T_return + APPROACH_COND1


    TRNSYS_DH_massflow  = PC_DH_massflow

    TRNSYS_DH_T_supply  = PC_DH_T_supply


## PID
#TRNSYS_Heat_Demand = PC_Heat_demand*1000;

#PC_Heat_Demand_ex = xlsread('Head_Demand');
#TRNSYS_Heat_Demand  = PC_Heat_Demand_ex(:,1); #fixed demand

##
# ## ------------------- Spliters and bleedings ----------------------------#
#
#
# ## --------------- Solar Field Components --------------------------------#
#
# #Helio Flied
# TRNSYS_Sfield_nEl       = o.field.nEl;
# TRNSYS_Sfield_nAz       = o.field.nAz;
# TRNSYS_Sfield_nHelio    = o.field.nHelio;
# TRNSYS_Sfield_Ahelio    = o.field.Ahelio;
# TRNSYS_Sfield_refl      = o.field.refl;
#
#         ## ---------------------- Controllers ------------------------------------#
#
#         #DSG Splitter
#         TRNSYS_SPL_QminEV=          TRNSYS_EV_Qinmin_dsgn;
#         TRNSYS_SPL_QminSH=          TRNSYS_SH_Qinmin_dsgn;
#         TRNSYS_SPL_QminRH=          TRNSYS_RH_Qinmin_dsgn;
#         TRNSYS_SPL_QmaxEV=                  o.rec.EV.Arec*650000;
#         TRNSYS_SPL_QmaxSH=                  o.rec.SH.Arec*300000;
#         TRNSYS_SPL_QmaxRH=                  o.rec.RH.Arec*300000;
#
#         TRNSYS_SPL_QinSF= (o.rec.EV.Qin+o.rec.SH.Qin+o.rec.RH.Qin)*3600/1000;


## -----------------------------------------------------------------------#
#-------------------------------------------------------------------------#
#-------------------------------------------------------------------------#


