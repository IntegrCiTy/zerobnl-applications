import importlib

from Core.setModelLabel import*

# Here functions to evaluate CAPEX, OPEX and techno-economic performance

# Calculate investment and O&M costs.
importlib.import_module('DynSim&TEcalculations.' + HESTech + '.' + model_plant + '.technoEconomics.calculateInvestmentCost' )

importlib.import_module('DynSim&TEcalculations.' + HESTech + '.' + model_plant + '.technoEconomics.calculateOperationMaintenanceCost' )

# Calculate performance indicators.
importlib.import_module('DynSim&TEcalculations.' + HESTech + '.' + model_plant + '.technoEconomics.calculatePerformance_noFIN' )

# Visuals:
importlib.import_module('DynSim&TEcalculations.' + HESTech + '.' + model_plant + '.Visuals.displayResults' )
