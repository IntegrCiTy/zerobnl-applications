function TRNSYS = prepareTRNSYSinput(o, TRNSYS)


%% -------------------------- Steam Turbine ------------------------------%

%HPT1
TRNSYS.HPT1_Pi_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st,2);
TRNSYS.HPT1_Po_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st,2)/o.PC.HPT.pr(1);
TRNSYS.HPT1_FR_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st,8)*3600;
TRNSYS.HPT1_ETA_dsgn    = o.PC.HPT.ETA(1);
TRNSYS.HPT1_bypass      = 1;
TRNSYS.HPT1_GenEff      = o.PC.Gen_Eff;

TRNSYS.HPT1_Po          = o.PC.st(o.PC.keyst.HPTin_n_st+1,2);
TRNSYS.HPT1_FR          = o.PC.st(o.PC.keyst.HPTin_n_st,8)*3600 ;
TRNSYS.HPT1_h           = o.PC.st(o.PC.keyst.HPTin_n_st,3);

if o.PC.n_hotPH > 1 || (o.PC.n_hotPH == 1 && o.PC.DeaLocatHP == 1)
    %HPT2 yes
    TRNSYS.HPT2_Pi_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st+2,2);
    TRNSYS.HPT2_Po_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st+2,2)/o.PC.HPT.pr(2);
    TRNSYS.HPT2_FR_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st+2,8)*3600;
    TRNSYS.HPT2_ETA_dsgn    = o.PC.HPT.ETA(2);
    TRNSYS.HPT2_bypass      = 1;
    
    TRNSYS.HPT2_Po          = o.PC.st(o.PC.keyst.HPTin_n_st+3,2);
    TRNSYS.HPT2_FR          = o.PC.st(o.PC.keyst.HPTin_n_st+2,8)*3600;
    TRNSYS.HPT2_h           = o.PC.st(o.PC.keyst.HPTin_n_st+2,3);

    
%     if o.PC.n_hotPH == 2 && o.PC.DeaLocatHP == 1
%         %HPT3 yes
%         TRNSYS.HPT3_Pi_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st+4,2);
%         TRNSYS.HPT3_Po_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st+4,2)/o.PC.HPT.pr(3);
%         TRNSYS.HPT3_FR_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st+4,8)*3600;
%         TRNSYS.HPT3_ETA_dsgn    = o.PC.HPT.ETA(3);
%         TRNSYS.HPT3_bypass      = 1;
%     
%         TRNSYS.HPT3_Po          = o.PC.st(o.PC.keyst.HPTin_n_st+5,2);
%         TRNSYS.HPT3_FR          = o.PC.st(o.PC.keyst.HPTin_n_st+4,8)*3600;
%         TRNSYS.HPT3_h           = o.PC.st(o.PC.keyst.HPTin_n_st+4,3);
%   
%     else
%         %HPT3 no
%         TRNSYS.HPT3_Pi_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st,2);
%         TRNSYS.HPT3_Po_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st,2)/o.PC.HPT.pr(2);
%         TRNSYS.HPT3_FR_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st,8)*3600;
%         TRNSYS.HPT3_ETA_dsgn    = o.PC.HPT.ETA(1);
%         TRNSYS.HPT3_bypass      = 0;
% 
%         TRNSYS.HPT3_Po          = o.PC.st(o.PC.keyst.HPTin_n_st+1,2);
%         TRNSYS.HPT3_FR          = o.PC.st(o.PC.keyst.HPTin_n_st,8)*3600;
%         TRNSYS.HPT3_h           = o.PC.st(o.PC.keyst.HPTin_n_st,3);   
%     end
%     
% else
%     %HPT2 no
%     TRNSYS.HPT2_Pi_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st+2,2);
%     TRNSYS.HPT2_Po_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st+2,2)/o.PC.HPT.pr(2);
%     TRNSYS.HPT2_FR_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st+2,8)*3600;
%     TRNSYS.HPT2_ETA_dsgn    = o.PC.HPT.ETA(2);
%     TRNSYS.HPT2_bypass      = 0;
%     
%     TRNSYS.HPT2_Po          = o.PC.st(o.PC.keyst.HPTin_n_st+3,2);
%     TRNSYS.HPT2_FR          = o.PC.st(o.PC.keyst.HPTin_n_st+2,8)*3600;
%     TRNSYS.HPT2_h           = o.PC.st(o.PC.keyst.HPTin_n_st+2,3);   
%     
%         %HPT3 no
%         TRNSYS.HPT3_Pi_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st,2);
%         TRNSYS.HPT3_Po_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st,2)/o.PC.HPT.pr(2);
%         TRNSYS.HPT3_FR_dsgn     = o.PC.st(o.PC.keyst.HPTin_n_st,8)*3600;
%         TRNSYS.HPT3_ETA_dsgn    = o.PC.HPT.ETA(1);
%         TRNSYS.HPT3_bypass      = 0;
% 
%         TRNSYS.HPT3_Po          = o.PC.st(o.PC.keyst.HPTin_n_st+1,2);
%         TRNSYS.HPT3_FR          = o.PC.st(o.PC.keyst.HPTin_n_st,8)*3600;
%         TRNSYS.HPT3_h           = o.PC.st(o.PC.keyst.HPTin_n_st,3); 
end

if o.PC.DeaLocatHP == 0
%LPT1 (IPT)
TRNSYS.IPT_Pi_dsgn     = o.PC.st(o.PC.keyst.IPTin_n_st,2);
TRNSYS.IPT_Po_dsgn     = o.PC.st(o.PC.keyst.IPTin_n_st+1,2);
TRNSYS.IPT_FR_dsgn     = o.PC.st(o.PC.keyst.IPTin_n_st,8)*3600; 
TRNSYS.IPT_ETA_dsgn    = o.PC.IPT.ETA;
TRNSYS.IPT_bypass      = 1;

TRNSYS.IPT_Po          = o.PC.st(o.PC.keyst.IPTin_n_st+1,2);
TRNSYS.IPT_FR          = o.PC.st(o.PC.keyst.IPTin_n_st,8)*3600; 
TRNSYS.IPT_h           = o.PC.st(o.PC.keyst.IPTin_n_st,3);
end


%LPT1
TRNSYS.LPT1_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st,2);
TRNSYS.LPT1_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+1,2);
TRNSYS.LPT1_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st,8)*3600; 
TRNSYS.LPT1_ETA_dsgn    = o.PC.LPT.ETA(1);
TRNSYS.LPT1_bypass      = 1;

TRNSYS.LPT1_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+1,2);
TRNSYS.LPT1_FR          = o.PC.st(o.PC.keyst.LPTin_n_st,8)*3600;
TRNSYS.LPT1_h           = o.PC.st(o.PC.keyst.LPTin_n_st,3);

if o.PC.n_coldPH > 0
    %LPT2 yes
    TRNSYS.LPT2_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+2,2);
    TRNSYS.LPT2_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+3,2);
    TRNSYS.LPT2_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+2,8)*3600;
    TRNSYS.LPT2_ETA_dsgn    = o.PC.LPT.ETA(2);
    TRNSYS.LPT2_bypass      = 1;
    
    TRNSYS.LPT2_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+3,2);
    TRNSYS.LPT2_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+2,8)*3600;
    TRNSYS.LPT2_h           = o.PC.st(o.PC.keyst.LPTin_n_st+2,3);
    
%     if o.PC.n_coldPH > 1 
%         %LPT3 yes
%         TRNSYS.LPT3_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+4,2);
%         TRNSYS.LPT3_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+5,2);
%         TRNSYS.LPT3_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+4,8)*3600;
%         TRNSYS.LPT3_ETA_dsgn    = o.PC.LPT.ETA(3);
%         TRNSYS.LPT3_bypass      = 1;
%         
%         TRNSYS.LPT3_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+5,2);
%         TRNSYS.LPT3_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+4,8)*3600;
%         TRNSYS.LPT3_h           = o.PC.st(o.PC.keyst.LPTin_n_st+4,3);
%         
%         if o.PC.n_coldPH > 2 
%             %LPT4 yes
%             TRNSYS.LPT4_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+6,2);
%             TRNSYS.LPT4_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+7,2);
%             TRNSYS.LPT4_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+6,8)*3600;
%             TRNSYS.LPT4_ETA_dsgn    = o.PC.LPT.ETA(4);
%             TRNSYS.LPT4_bypass      = 1;
%             
%             TRNSYS.LPT4_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+7,2);
%             TRNSYS.LPT4_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+6,8)*3600;
%             TRNSYS.LPT4_h           = o.PC.st(o.PC.keyst.LPTin_n_st+6,3);
%             
%             if o.PC.DoubleCond == 1
%                 %LPT5 yes
%                 TRNSYS.LPT5_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,2);
%                 TRNSYS.LPT5_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                 TRNSYS.LPT5_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,8)*3600;
%                 TRNSYS.LPT5_ETA_dsgn    = o.PC.LPT.ETA(5);
%                 TRNSYS.LPT5_bypass      = 1;
% 
%                 TRNSYS.LPT5_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                 TRNSYS.LPT5_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+7,8)*3600;
%                 TRNSYS.LPT5_h           = o.PC.st(o.PC.keyst.LPTin_n_st+7,3);
%             else
%                 %LPT5 no
%                 TRNSYS.LPT5_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,2);
%                 TRNSYS.LPT5_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                 TRNSYS.LPT5_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,8)*3600;
%                 TRNSYS.LPT5_ETA_dsgn    = o.PC.LPT.ETA(5);
%                 TRNSYS.LPT5_bypass      = 0;
% 
%                 TRNSYS.LPT5_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                 TRNSYS.LPT5_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+7,8)*3600;
%                 TRNSYS.LPT5_h           = o.PC.st(o.PC.keyst.LPTin_n_st+7,3);
%             end
%           
%         else
%             if o.PC.DoubleCond == 1
%                 %LPT4 yes
%                 TRNSYS.LPT4_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+6,2);
%                 TRNSYS.LPT4_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+7,2);
%                 TRNSYS.LPT4_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+6,8)*3600;
%                 TRNSYS.LPT4_ETA_dsgn    = o.PC.LPT.ETA(4);
%                 TRNSYS.LPT4_bypass      = 1;
% 
%                 TRNSYS.LPT4_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+7,2);
%                 TRNSYS.LPT4_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+6,8)*3600;
%                 TRNSYS.LPT4_h           = o.PC.st(o.PC.keyst.LPTin_n_st+6,3);
%                 %LPT5 no
%                 TRNSYS.LPT5_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,2);
%                 TRNSYS.LPT5_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                 TRNSYS.LPT5_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,8)*3600;
%                 TRNSYS.LPT5_ETA_dsgn    = o.PC.LPT.ETA(5);
%                 TRNSYS.LPT5_bypass      = 0;
% 
%                 TRNSYS.LPT5_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                 TRNSYS.LPT5_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+7,8)*3600;
%                 TRNSYS.LPT5_h           = o.PC.st(o.PC.keyst.LPTin_n_st+7,3);
%             else
%                 %LPT4 no
%                 TRNSYS.LPT4_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+6,2);
%                 TRNSYS.LPT4_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+7,2);
%                 TRNSYS.LPT4_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+6,8)*3600;
%                 TRNSYS.LPT4_ETA_dsgn    = o.PC.LPT.ETA(4);
%                 TRNSYS.LPT4_bypass      = 0;
% 
%                 TRNSYS.LPT4_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+7,2);
%                 TRNSYS.LPT4_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+6,8)*3600;
%                 TRNSYS.LPT4_h           = o.PC.st(o.PC.keyst.LPTin_n_st+6,3);
%                 
%                 %LPT5 no
%                 TRNSYS.LPT5_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,2);
%                 TRNSYS.LPT5_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                 TRNSYS.LPT5_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,8)*3600;
%                 TRNSYS.LPT5_ETA_dsgn    = o.PC.LPT.ETA(5);
%                 TRNSYS.LPT5_bypass      = 0;
% 
%                 TRNSYS.LPT5_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                 TRNSYS.LPT5_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+7,8)*3600;
%                 TRNSYS.LPT5_h           = o.PC.st(o.PC.keyst.LPTin_n_st+7,3);
%             end
%         end
%     else
        %LPT2 yes
        if o.PC.DoubleCond == 1
            %LPT3 yes
            TRNSYS.LPT3_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,2);
            TRNSYS.LPT3_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+5+o.PC.DeaLP,2);
            TRNSYS.LPT3_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,8)*3600;
            TRNSYS.LPT3_ETA_dsgn    = o.PC.LPT.ETA(3);
            TRNSYS.LPT3_bypass      = 1;

            TRNSYS.LPT3_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+5+o.PC.DeaLP,2);
            TRNSYS.LPT3_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,8)*3600;
            TRNSYS.LPT3_h           = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,3);
%                 
%                 %LPT4 no
%                 TRNSYS.LPT4_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+6,2);
%                 TRNSYS.LPT4_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+7,2);
%                 TRNSYS.LPT4_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+6,8)*3600;
%                 TRNSYS.LPT4_ETA_dsgn    = o.PC.LPT.ETA(4);
%                 TRNSYS.LPT4_bypass      = 0;
% 
%                 TRNSYS.LPT4_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+7,2);
%                 TRNSYS.LPT4_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+6,8)*3600;
%                 TRNSYS.LPT4_h           = o.PC.st(o.PC.keyst.LPTin_n_st+6,3);
%                 
%                 %LPT5 no
%                 TRNSYS.LPT5_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,2);
%                 TRNSYS.LPT5_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                 TRNSYS.LPT5_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,8)*3600;
%                 TRNSYS.LPT5_ETA_dsgn    = o.PC.LPT.ETA(5);
%                 TRNSYS.LPT5_bypass      = 0;
% 
%                 TRNSYS.LPT5_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                 TRNSYS.LPT5_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+7,8)*3600;
%                 TRNSYS.LPT5_h           = o.PC.st(o.PC.keyst.LPTin_n_st+7,3);
%             
%         else
%             %LPT3 no
%             TRNSYS.LPT3_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,2);
%             TRNSYS.LPT3_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+5+o.PC.DeaLP,2);
%             TRNSYS.LPT3_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,8)*3600;
%             TRNSYS.LPT3_ETA_dsgn    = o.PC.LPT.ETA(3);
%             TRNSYS.LPT3_bypass      = 0;
% 
%             TRNSYS.LPT3_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+5+o.PC.DeaLP,2);
%             TRNSYS.LPT3_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,8)*3600;
%             TRNSYS.LPT3_h           = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,3);
%                 
%                 %LPT4 no
%                 TRNSYS.LPT4_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+6,2);
%                 TRNSYS.LPT4_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+7,2);
%                 TRNSYS.LPT4_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+6,8)*3600;
%                 TRNSYS.LPT4_ETA_dsgn    = o.PC.LPT.ETA(4);
%                 TRNSYS.LPT4_bypass      = 0;
% 
%                 TRNSYS.LPT4_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+7,2);
%                 TRNSYS.LPT4_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+6,8)*3600;
%                 TRNSYS.LPT4_h           = o.PC.st(o.PC.keyst.LPTin_n_st+6,3);
%                 
%                 %LPT5 no
%                 TRNSYS.LPT5_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,2);
%                 TRNSYS.LPT5_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                 TRNSYS.LPT5_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,8)*3600;
%                 TRNSYS.LPT5_ETA_dsgn    = o.PC.LPT.ETA(5);
%                 TRNSYS.LPT5_bypass      = 0;
% 
%                 TRNSYS.LPT5_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                 TRNSYS.LPT5_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+7,8)*3600;
%                 TRNSYS.LPT5_h           = o.PC.st(o.PC.keyst.LPTin_n_st+7,3);
        end
%     end
%     
%  else
%     %LPT1 yes
%     if o.PC.DoubleCond == 1
%         %LPT2 yes
%         TRNSYS.LPT2_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+2,2);
%         TRNSYS.LPT2_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+3,2);
%         TRNSYS.LPT2_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+2,8)*3600;
%         TRNSYS.LPT2_ETA_dsgn    = o.PC.LPT.ETA(2);
%         TRNSYS.LPT2_bypass      = 1;
% 
%         TRNSYS.LPT2_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+3,2);
%         TRNSYS.LPT2_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+2,8)*3600;
%         TRNSYS.LPT2_h           = o.PC.st(o.PC.keyst.LPTin_n_st+2,3);
% 
% 
%             %LPT3 no
%             TRNSYS.LPT3_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,2);
%             TRNSYS.LPT3_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+5+o.PC.DeaLP,2);
%             TRNSYS.LPT3_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,8)*3600;
%             TRNSYS.LPT3_ETA_dsgn    = o.PC.LPT.ETA(3);
%             TRNSYS.LPT3_bypass      = 0;
% 
%             TRNSYS.LPT3_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+5+o.PC.DeaLP,2);
%             TRNSYS.LPT3_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,8)*3600;
%             TRNSYS.LPT3_h           = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,3);
% 
%                 %LPT4 no
%                 TRNSYS.LPT4_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+6,2);
%                 TRNSYS.LPT4_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+7,2);
%                 TRNSYS.LPT4_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+6,8)*3600;
%                 TRNSYS.LPT4_ETA_dsgn    = o.PC.LPT.ETA(4);
%                 TRNSYS.LPT4_bypass      = 0;
% 
%                 TRNSYS.LPT4_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+7,2);
%                 TRNSYS.LPT4_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+6,8)*3600;
%                 TRNSYS.LPT4_h           = o.PC.st(o.PC.keyst.LPTin_n_st+6,3);
% 
%                 %LPT5 no
%                 TRNSYS.LPT5_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,2);
%                 TRNSYS.LPT5_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                 TRNSYS.LPT5_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,8)*3600;
%                 TRNSYS.LPT5_ETA_dsgn    = o.PC.LPT.ETA(5);
%                 TRNSYS.LPT5_bypass      = 0;
% 
%                 TRNSYS.LPT5_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                 TRNSYS.LPT5_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+7,8)*3600;
%                 TRNSYS.LPT5_h           = o.PC.st(o.PC.keyst.LPTin_n_st+7,3);
%     else
%         %LPT2 no
%         TRNSYS.LPT2_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+2,2);
%         TRNSYS.LPT2_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+3,2);
%         TRNSYS.LPT2_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+2,8)*3600;
%         TRNSYS.LPT2_ETA_dsgn    = o.PC.LPT.ETA(2);
%         TRNSYS.LPT2_bypass      = 0;
% 
%         TRNSYS.LPT2_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+3,2);
%         TRNSYS.LPT2_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+2,8)*3600;
%         TRNSYS.LPT2_h           = o.PC.st(o.PC.keyst.LPTin_n_st+2,3);
%                 %LPT3 no
%                 TRNSYS.LPT3_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,2);
%                 TRNSYS.LPT3_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+5+o.PC.DeaLP,2);
%                 TRNSYS.LPT3_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,8)*3600;
%                 TRNSYS.LPT3_ETA_dsgn    = o.PC.LPT.ETA(3);
%                 TRNSYS.LPT3_bypass      = 0;
% 
%                 TRNSYS.LPT3_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+5+o.PC.DeaLP,2);
%                 TRNSYS.LPT3_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,8)*3600;
%                 TRNSYS.LPT3_h           = o.PC.st(o.PC.keyst.LPTin_n_st+4+o.PC.DeaLP,3);
% 
%                     %LPT4 no
%                     TRNSYS.LPT4_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+6,2);
%                     TRNSYS.LPT4_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+7,2);
%                     TRNSYS.LPT4_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+6,8)*3600;
%                     TRNSYS.LPT4_ETA_dsgn    = o.PC.LPT.ETA(4);
%                     TRNSYS.LPT4_bypass      = 0;
% 
%                     TRNSYS.LPT4_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+7,2);
%                     TRNSYS.LPT4_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+6,8)*3600;
%                     TRNSYS.LPT4_h           = o.PC.st(o.PC.keyst.LPTin_n_st+6,3);
% 
%                     %LPT5 no
%                     TRNSYS.LPT5_Pi_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,2);
%                     TRNSYS.LPT5_Po_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                     TRNSYS.LPT5_FR_dsgn     = o.PC.st(o.PC.keyst.LPTin_n_st+8,8)*3600;
%                     TRNSYS.LPT5_ETA_dsgn    = o.PC.LPT.ETA(5);
%                     TRNSYS.LPT5_bypass      = 0;
% 
%                     TRNSYS.LPT5_Po          = o.PC.st(o.PC.keyst.LPTin_n_st+9,2);
%                     TRNSYS.LPT5_FR          = o.PC.st(o.PC.keyst.LPTin_n_st+7,8)*3600;
%                     TRNSYS.LPT5_h           = o.PC.st(o.PC.keyst.LPTin_n_st+7,3);
%         
%     end
  
    
end 

%% Boiler

TRNSYS.Boiler_Q  = o.PC.ECO.Q + o.PC.EV.Q + o.PC.SH.Q;

TRNSYS.Boiler_h_out = o.PC.st(o.PC.keyst.HPTin_n_st,3);

TRNSYS.Boiler_Fuel        = o.Fuel.LHV;

if o.PC.RHpresence == 1
    
    TRNSYS.ReHeat_Q           = o.PC.RH.Q;

    TRNSYS.ReHeat_h_out       = o.PC.st(o.PC.keyst.HPTin_n_st,3);

    TRNSYS.ReHeat_Pdrop       = o.PC.RH.dP;
end


%         %% ------------------------ DSG Receivers -------------------------------%
%         %Economizer
TRNSYS.ECO_UA            =                 o.PC.ECO.UA; %ok
TRNSYS.EV_UA            =                 o.PC.EVA.UA; %ok
TRNSYS.SH_UA            =                 o.PC.SH.UA; %ok
%         TRNSYS.SH_Qloss_dsgn   =                o.rec.SH.Qloss_total;
%         TRNSYS.SH_PdSH_dsgn      =                        o.PC.SH.dP;
%         TRNSYS.SH_mdot_dsgn         =                      o.PC.mdot;
%         TRNSYS.SH_Qinmin_dsgn            = o.rec.SH.Qin*o.rec.Qminfrac;%2.6200e+06;%2.9943e+06;%4.1920e+06;%5.2400e+06;%5.8223e+06;%6.9867e+06;% 8.7334e+06;%1.0480e+07;
%         TRNSYS.SH_MaxheatFlux_dsgn   =                         300000;
%         TRNSYS.SH_Arec_dsgn      =                      o.rec.SH.Arec;
%         TRNSYS.SH_Tatemp_dsgn      =                      o.PC.TinHPT;
%         TRNSYS.SH_mode_dsgn      =                                 1;

%         %Superheater
%         TRNSYS.SH_Qin_dsgn            =                 o.rec.SH.Qin;
%         TRNSYS.SH_Qloss_dsgn   =                o.rec.SH.Qloss_total;
%         TRNSYS.SH_PdSH_dsgn      =                        o.PC.SH.dP;
%         TRNSYS.SH_mdot_dsgn         =                      o.PC.mdot;
%         TRNSYS.SH_Qinmin_dsgn            = o.rec.SH.Qin*o.rec.Qminfrac;%2.6200e+06;%2.9943e+06;%4.1920e+06;%5.2400e+06;%5.8223e+06;%6.9867e+06;% 8.7334e+06;%1.0480e+07;
%         TRNSYS.SH_MaxheatFlux_dsgn   =                         300000;
%         TRNSYS.SH_Arec_dsgn      =                      o.rec.SH.Arec;
%         TRNSYS.SH_Tatemp_dsgn      =                      o.PC.TinHPT;
%         TRNSYS.SH_mode_dsgn      =                                 1;
% 
%         TRNSYS.SH_Tin=            o.PC.st(o.PC.keyst.HPTin_n_st-1,1);
%         TRNSYS.SH_PinTurb=          o.PC.st(o.PC.keyst.HPTin_n_st,2);
%         TRNSYS.SH_Qin=                                  o.rec.SH.Qin;
%         TRNSYS.SH_mdot=                                    o.PC.mdot;
% 
%         %Evaporator
%         TRNSYS.EV_Qin_dsgn            =                 o.rec.EV.Qin;
%         TRNSYS.EV_Qloss_dsgn   =                o.rec.EV.Qloss_total;
%         TRNSYS.EV_PdropSH_dsgn      =                     o.PC.SH.dP;
%         TRNSYS.EV_PdropEV_dsgn      =                     o.PC.EV.dP;
%         TRNSYS.EV_mdot_dsgn         =                      o.PC.mdot;
%         TRNSYS.EV_Qinmin_dsgn            =                o.rec.EV.Qin*o.rec.Qminfrac;%4.2089e+06;%4.8101e+06;%6.7342e+06;%8.4177e+06;%9.3530e+06;%1.1224e+07;%1.4030e+07;%1.6835e+07;
%         TRNSYS.EV_MaxheatFlux_dsgn   =                         650000;
%         TRNSYS.EV_Arec_dsgn      =                      o.rec.EV.Arec;
% 
%         TRNSYS.EV_Tin=             o.PC.st(o.PC.keyst.HPTin_n_st-2,1);
%         TRNSYS.EV_PinTurb=           o.PC.st(o.PC.keyst.HPTin_n_st,2);
%         TRNSYS.EV_Qin=                                  o.rec.EV.Qin;
% 
%         %Reheater
%         TRNSYS.RH_Qin_dsgn            =                     o.rec.RH.Qin;
%         TRNSYS.RH_Qloss_dsgn   =                    o.rec.RH.Qloss_total;
%         TRNSYS.RH_PdropRH_dsgn      =                         o.PC.RH.dP;
%         TRNSYS.RH_mdot_dsgn         =   o.PC.st(o.PC.keyst.IPTin_n_st-1,8);
%         TRNSYS.RH_Qinmin_dsgn            =                    o.rec.RH.Qin*o.rec.Qminfrac;%9.6748e+05;%1.1057e+06;%1.5480e+06;%1.9350e+06;%2.1500e+06;%2.5800e+06;%3.2249e+06;%3.8699e+06;
%         TRNSYS.RH_MaxheatFlux_dsgn   =                         300000;
%         TRNSYS.RH_Arec_dsgn      =                      o.rec.RH.Arec;
%         TRNSYS.RH_Tatemp_dsgn      = o.PC.st(o.PC.keyst.IPTin_n_st,1);
%         TRNSYS.RH_mode_dsgn      =                                 2;
% 
%         TRNSYS.RH_PinTurb=          o.PC.st(o.PC.keyst.IPTin_n_st,2);
%         TRNSYS.RH_Qin=                                  o.rec.RH.Qin;
%         TRNSYS.RH_mdot=           o.PC.st(o.PC.keyst.IPTin_n_st-1,8);
%         TRNSYS.RH_hin=            o.PC.st(o.PC.keyst.IPTin_n_st-1,3);


%% ---------------------------- PUMPS ------------------------------------%
if o.PC.PumpBeforeMix == 0
%PUMP 1
TRNSYS.PUMP1_mode       = 2;
TRNSYS.PUMP1_Pin        = o.PC.st(1,2);
TRNSYS.PUMP1_ro         = 1000;
TRNSYS.PUMP1_ETA        = o.PC.Pump_Eff; %o.PC.COND.Pump.EFF; %Monica 16/04/2018
TRNSYS.PUMP1_W          = o.PC.COND.Pump.Power*3600; %kJ/hr
else
TRNSYS.PUMP_befmix_mode       = 2;
TRNSYS.PUMP_befmix_Pin        = o.PC.st(1,2);
TRNSYS.PUMP_befmix_ro         = 1000;
TRNSYS.PUMP_befmix_ETA        = o.PC.Pump_Eff;
TRNSYS.PUMP_befmix_W          = o.PC.PumpBefMix.Power*3600; %kJ/hr
end

if o.PC.DeaLP == 1
TRNSYS.PUMP_dealp_mode       = 2;
TRNSYS.PUMP_dealp_Pin        = o.PC.st((o.PC.keyst.LPTout_n_st+o.PC.n_hotPH+1+o.PC.n_coldPH+o.PC.DeaLP),2);
TRNSYS.PUMP_dealp_ro         = 1000;
TRNSYS.PUMP_dealp_ETA        = o.PC.Pump_Eff;
TRNSYS.PUMP_dealp_W          = o.PC.PUMP.W_DeaLP*3600; %kJ/hr
end
%PUMP 2
TRNSYS.PUMP2_mode       = 2;
TRNSYS.PUMP2_Pin        = o.PC.st(o.PC.keyst.DEAin_n_st+1,2);
TRNSYS.PUMP2_ro         = 1000;
TRNSYS.PUMP2_ETA        = o.PC.Pump_Eff;
TRNSYS.PUMP2_W          = o.PC.PUMP.W2*3600; %kJ/hr


        %% -------------------------- SUBCOOLERS ---------------------------------%
        %HE1
        TRNSYS.HE1_UA           = o.PC.hotSC(1,2)*3600;
        TRNSYS.HE1_Cp_hot       = min(o.PC.hotSC(1,3),o.PC.hotSC(1,4));
        TRNSYS.HE1_CP_cold      = max(o.PC.hotSC(1,3),o.PC.hotSC(1,4));
        TRNSYS.HE1_FRref_cold   = o.PC.st(o.PC.keyst.DEAin_n_st+1,8)*3600;

%         %HE2        
%         TRNSYS.HE2_UA           = o.PC.hotSC(2,2)*3600;
%         TRNSYS.HE2_Cp_hot       = min(o.PC.hotSC(2,3),o.PC.hotSC(2,4))/(o.PC.st(o.PC.keyst.LPTout_n_st+2,8));
%         TRNSYS.HE2_CP_cold      = max(o.PC.hotSC(2,3),o.PC.hotSC(2,4))/(o.PC.mdot);
%         TRNSYS.HE2_FRref_cold   = o.PC.mdot*3600;

        %---COLD-----%
        %HE3
        TRNSYS.HE3_UA           = o.PC.coldSC(1,2)*3600;
        TRNSYS.HE3_Cp_hot       = min(o.PC.coldSC(1,3),o.PC.coldSC(1,4));
        TRNSYS.HE3_CP_cold      = max(o.PC.coldSC(1,3),o.PC.coldSC(1,4));
        TRNSYS.HE3_FRref_cold   = o.PC.st(o.PC.keyst.DEAin_n_st,8)*3600;

%         %HE4
%         TRNSYS.HE4_UA           = o.PC.coldSC(2,2)*3600;
%         TRNSYS.HE4_Cp_hot       = min(o.PC.coldSC(2,3),o.PC.coldSC(2,4))/(o.PC.st(o.PC.keyst.LPTout_n_st+4,8));
%         TRNSYS.HE4_CP_cold      = max(o.PC.coldSC(2,3),o.PC.coldSC(2,4))/(o.PC.st(o.PC.keyst.DEAin_n_st,8));
%         TRNSYS.HE4_FRref_cold   = o.PC.st(o.PC.keyst.DEAin_n_st,8)*3600;

        %% -------------------------- PREHEATERS ---------------------------------%

        %PH1
        TRNSYS.PH1_Cp_cold      = o.PC.hotPH(1,4);
        TRNSYS.PH1_UA           = o.PC.hotPH(1,2)*3600;
        TRNSYS.PH1_FRref_cold   = o.PC.st(o.PC.keyst.DEAin_n_st+1,8)*3600;
        TRNSYS.PH1_onoff        = 1;

%          %PH2
%         TRNSYS.PH2_Cp_cold      = o.PC.hotPH(2,4);
%         TRNSYS.PH2_UA           = o.PC.hotPH(2,2)*3600;
%         TRNSYS.PH2_FRref_cold   = o.PC.mdot*3600;
%         TRNSYS.PH2_onoff        = 1;

        %---COLD----%
        %PH3
        TRNSYS.PH3_Cp_cold      = o.PC.coldPH(1,4);
        TRNSYS.PH3_UA           = o.PC.coldPH(1,2)*3600;
        TRNSYS.PH3_FRref_cold   = o.PC.st(o.PC.keyst.DEAin_n_st,8)*3600;
        TRNSYS.PH3_onoff        = 1;

%         %PH4
%         TRNSYS.PH4_Cp_cold      = o.PC.coldPH(2,4);
%         TRNSYS.PH4_UA           =  o.PC.coldPH(2,2)*3600;
%         TRNSYS.PH4_FRref_cold   = o.PC.st(o.PC.keyst.DEAin_n_st,8)*3600;
%         TRNSYS.PH4_onoff        = 1;
        
 
%% -------------------- Deaerator & Condenser ----------------------------%

%Deaerator

%Condenser

if o.PC.PCONDset ~= 3
TRNSYS.CND_UAref    =     o.PC.COND.UA*3600;


        TRNSYS.CND_Ttarget   = o.PC.COND.Tcout;    
        TRNSYS.CND_Pmax       = o.PC.COND.fan.Power*3600;
        TRNSYS.CND_TTDref    = o.PC.COND.dTapp;
        TRNSYS.CND_UAexp        = 1;
        TRNSYS.CND_FRamax       = o.PC.COND.air.FR*3600; 
        
        TRNSYS.CND_Hin=   o.PC.st(o.PC.keyst.LPTout_n_st,3);
        TRNSYS.CND_FRcond= o.PC.st(o.PC.keyst.LPTout_n_st,8)*3600;
        TRNSYS.CND_Tair_in= o.design.Tamb;
        TRNSYS.CND_Tin=  o.PC.st(o.PC.keyst.LPTout_n_st,1);
        
elseif o.PC.PCONDset == 3
    
    if o.PC.DoubleCond == 1
        
%         TRNSYS.dT_WtrOutCond_1 = o.PC.dT_wtr_out_condensing;
%                       
%         TRNSYS.dT_water_DH_1 = o.APPROACH_COND1;
%         
%         %second condenser as a preheater
%         TRNSYS.PHdh_Cp_cold      = o.PC.COND2.DH_PH(1,4);
%         TRNSYS.PHdh_UA           = o.PC.COND2.DH_PH(1,2)*3600;
%         TRNSYS.PHdh_FRref_cold   = o.PC.DH_massflow*3600;
%         TRNSYS.PHdh_onoff        = 1;
%         
%     end


%     TRNSYS.UA_COND2       = o.PC.COND2.UA_DELTA*3600    ;
 
%     TRNSYS.DH_massflow   = o.PC.DH_massflow ;
% 
%     TRNSYS.DH_T_out_COND1  = o.PC.DH_T_return + o.APPROACH_COND1; 
%     
%     TRNSYS.DH_T_in_COND1 = o.PC.DH_T_return;
% 
% 
%     
%     TRNSYS.DH_T_out_COND2 = o.PC.DH_T_supply ;
%     
%     TRNSYS.DH_T_in_COND2 = o.PC.DH_T_return + o.APPROACH_COND1; 
    end

    TRNSYS.DH_massflow  = o.PC.DH_massflow ;

    TRNSYS.DH_T_supply  = o.PC.DH_T_supply ;
end

%% PID
%TRNSYS.Heat_Demand = o.PC.Heat_demand*1000;

%o.PC.Heat_Demand_ex = xlsread('Head_Demand');
%TRNSYS.Heat_Demand  = o.PC.Heat_Demand_ex(:,1); %fixed demand

%%
% %% ------------------- Spliters and bleedings ----------------------------%
% 
% 
% %% --------------- Solar Field Components --------------------------------%
% 
% %Helio Flied
% TRNSYS.Sfield_nEl       = o.field.nEl;
% TRNSYS.Sfield_nAz       = o.field.nAz;
% TRNSYS.Sfield_nHelio    = o.field.nHelio;
% TRNSYS.Sfield_Ahelio    = o.field.Ahelio;
% TRNSYS.Sfield_refl      = o.field.refl;
% 
%         %% ---------------------- Controllers ------------------------------------%
% 
%         %DSG Splitter
%         TRNSYS.SPL_QminEV=          TRNSYS.EV_Qinmin_dsgn;
%         TRNSYS.SPL_QminSH=          TRNSYS.SH_Qinmin_dsgn;
%         TRNSYS.SPL_QminRH=          TRNSYS.RH_Qinmin_dsgn;
%         TRNSYS.SPL_QmaxEV=                  o.rec.EV.Arec*650000;
%         TRNSYS.SPL_QmaxSH=                  o.rec.SH.Arec*300000;
%         TRNSYS.SPL_QmaxRH=                  o.rec.RH.Arec*300000;
% 
%         TRNSYS.SPL_QinSF= (o.rec.EV.Qin+o.rec.SH.Qin+o.rec.RH.Qin)*3600/1000;

end

%% -----------------------------------------------------------------------%
%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%