''' Idea is to create the if conditionals for all blocks and import
setModelLabel in order to compare, and create separate default parameter files for each possible component HES3_1.....etc'''

# To import all block names
from Core.setModelLabel import *

if HESname == 'HES3_1':
    from DesignParameters.HES3_1_Def_Par import *


# Complete the rest of the cases



# Loading EEG default parameters

elif EEGname == 'EEG1_2':
    from DesignParameters.EEG1_2_Def_Par import *


from DesignParameters.ECON_Def_Par import *

# Check this one with Monica  ----> Osama
# Convert minutes to seconds. (Useful only for TRNSYS based models)
model_dt = model_dt * 60

print('>>  Technical and economic parameters set')
print(' ')
