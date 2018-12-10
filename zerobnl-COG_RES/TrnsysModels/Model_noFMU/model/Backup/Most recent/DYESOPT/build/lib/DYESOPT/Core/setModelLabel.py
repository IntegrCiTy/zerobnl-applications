
 # This is to choose the correct subfolder in the Dyn&TEcalculation folder


from model_Choice import *

if HESblock != 0 :
    dynGroups = HESblock
else:
    dynGroups = EEGblock
  #  return dynGroups

    # Label identification for combined blocks

if COMB_HESblock != 0 :
    HESname = HESblockCode +'&'+ 'HES' + str(COMB_HESblock) + '_' + str(COMB_HESblockCode)
else:
    HESname = HESblockCode

if COMB_TESblock != 0 :
   TESname = TESblockCode +'&'+ 'TES' + str(COMB_TESblock) + '_' + str( COMB_TESblockCode)
else:
   TESname = TESblockCode

if COMB_EEGblock != 0 :
   EEGname = EEGblockCode +'&'+ 'EEG' + str(COMB_EEGblock) + '_' + str( COMB_EEGblockCode)
else:
   EEGname = EEGblockCode

if COMB_EESblock != 0 :
   EESname = EESblockCode +'&'+ 'EES' + str(COMB_EESblock) + '_' + str( COMB_EESblockCode)
else:
   EESname = EESblockCode

model_plant = HESname + '__' + TESname + '__' + EEGname + '__' + EESname

'''TO BE EDITED '''
#elseif mode == 2  # It should be modified!!
#    o.model.plant = ([o.model.plant '_' addLab]);

