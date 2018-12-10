

# Here the user choose the model components

    # Label structure: HEStechnology_TESblock_EEGblock_EESblock
    # Special label structure: HEStechnology_TESblock_EEGblock_EESblock_<additional feature>
    # Combined blocks: &

# DYESOPT AVAILABLE MODELS

    # BioFuel models___________________________________________________

        # Boiler_off_RankineCycleCHP_off

        # Boiler_off_RankineCycleCHPII_off


    # CSP models_______________________________________________________

        # DSG&STTP_off_RankineCycle_off (DS off)

        # DSG&STTP_off_RankineCycle_off_startupsVs1

        # MS&STTP&Boiler_TwoTanks_RankineCycle&PhotovoltaicSystem_Batteries

        # MS&STTP&Boiler_TwoTanks_RankineCycle&PhotovoltaicSystem_off

        # MS&STTP_Thermocline_RankineCycle_off (DS Peak/Base)

        # MS&STTP_TwoTanks_RankineCycle&PhotovoltaicSystem_Batteries

        # MS&STTP_TwoTanks_RankineCycle&PhotovoltaicSystem_off

        # MS&STTP_TwoTanks_RankineCycle_off (DS Peak/Base)

    # Photovoltaic System models_______________________________________

        # off_off_PhotovoltaicSystem&DieselGenerator_off

        # off_off_PhotovoltaicSystem_Batteries

        # off_off_PhotovoltaicSystem_off
#______________________________________________________________________

## First block: heat energy source (HES) block

HESblock                   = 3
    # CSP                  = 1
    # FossilFuel           = 2
    # ResFuel              = 3
    # off                  = 0

HESblockCode               = 1
    # CSP
        # MS&STTP          = 1
        # DSG&STTP         = 2
    # FossilFuel
        # Boiler           = 1
    # ResFuel
        # Boiler           = 1
    # off                  = 0

if HESblock == 0 :
    HESblockCode = ('HES' + str(HESblock))
else:
    HESblockCode = ('HES'+ str(HESblock) + '_' + str(HESblockCode))
#______________________________________________________________________
## Second block: electrical energy generation (EEG) block

EEGblock                   = 1
    # RankineCycle         = 1
    # PhotovoltaicSystem   = 2            OBS! Remember to check MainFile and o.model.tool in the related designParameters folder
    # Diesel Generator     = 3
    # off                  = 0

EEGblockCode               = 2
    # Rankine Cycle
        # Base             = 0
        # Double Condenser = 1
        # Vattenfall       = 2
    # Photovoltaic
        # Base             = 0
    # Diesel Generator
        # Base             = 0
    # off                  = 0

if EEGblock == 0 :
    EEGblockCode = ('EEG' + str(EEGblock))
else:
    EEGblockCode = ('EEG'+ str(EEGblock) + '_' + str(EEGblockCode))
#______________________________________________________________________
## Third block: thermal energy storage (TES) block

TESblock                   = 0
    # Thermocline          = 1
    # TwoTanks             = 2
    # off                  = 0

TESblockCode               = 0
    # Thermocline
        # Base             = 0
    # TwoTanks
        # Base             = 0
    # off                  = 0

if TESblock == 0 :
    TESblockCode = ('TES' + str(TESblock))
else:
    TESblockCode = ('TES'+ str(TESblock) + '_' + str(TESblockCode))
#______________________________________________________________________
## Fourth block: electrical energy storage (EES) block

EESblock                   = 0
    # Batteries            = 1
    # off                  = 0

EESblockCode               = 0
    # Batteries
        # Base             = 0
    # Otherwise            = 0

if EESblock == 0 :
    EESblockCode = ('EES' + str(EESblock))
else:
    EESblockCode = ('EES'+ str(EESblock) + '_' + str(EESblockCode))
#______________________________________________________________________
## Combined (COMB) option

COMB_HESblock             = 0
    # CSP                 = 1
    # FossilFuel          = 2
    # ResFuel             = 3
    # off                 = 0

COMB_HESblockCode         = 0
    # CSP
        # MS&STTP         = 1
        # DSG&STTP        = 2
    # FossilFuel
        # Boiler          = 1
    # ResFuel
        # Boiler          = 1
    # off                 = 0

COMB_EEGblock             = 0
    # PhotovoltaicSystem  = 2           OBS! Remember to check MainFile and o.model.tool in the related designParameters folder
    # DieselGenerator     = 3
    # off                 = 0

COMB_EEGblockCode         = 0
    # Photovoltaic
        # Base            = 0
    # Diesel Generator
        # Base            = 0
    # Otherwise           = 0

COMB_TESblock             = 0
COMB_TESblockCode         = 0
# Implemented but no options yet available

COMB_EESblock             = 0
COMB_EESblockCode         = 0
# not yet implemented
#______________________________________________________________________
## Dispatch strategy (DS) option

DS_mode                   = 1
    # Baseload            = 1
    # Peakload            = 2          OBS! To be chosen only if a TES block or EES block is available
    # off                 = 0          OBS! To be chosen only if a TES block or EES block is available

DS_type                   = 1
    # PDS (Pre-Defined)   = 1          Dispatch control is predetermined in MATLAB
    # DDS (Dynamic)       = 2          Dispatch control is handled in TRNSYS
#______________________________________________________________________
## For Dynamic simulation purposes ---> Osama

if HESblock == 3:
    HESTech = 'ResFuel'


## Dynamic model identification (supposed to be automatic)
'''OBS! If you will need more than one combined block at once then you
should think of creating more options using like o.combinedSYS = 2 ..You 
might create dedicated functions..'''

from Core import setModelLabel





# Check MODEL_choice.m for fixing temporary conditions - Linus' project
