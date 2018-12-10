import DYESOPT

# Here the 4 DYESOPT main steps are run: default parameters, power plant
# design, dynamic model simulation and thermo-economic calculations.

# Selected model components are loaded and model label is created
import model_Choice

from Core.Display.dyesoptHeader import *

if DYESOPT.runMode == 'single':
    dyesoptHeader(DYESOPT.runMode)
    print(' ')

# Inform of current operation.
if DYESOPT.runMode == 'single':
    print('>>  Opening ' + model_plant + ' model...')
    print(' ')
    print('>>  Loading specifications...')


# According to the selected components, the corresponding default parameters are loaded
from Core import setDefaultParameters

# Steady state design of selected Power Plant
from Core import designPowerPlant

# Run desired annual performance model simulation.
from Core import runPerformance

# Run thermoeconomic analysis
from Core import runTechnoeconomics
print('')
print('')
