
# Default Parameters of HES3_1 which is the Rankine


# Here the default parameters for a Res driven boiler technology can be set by the
# user concerning: LHV, density and price (for the moment).

# Importing useful libraries
import xlrd                                                # For extracting data from fuel excel file
import pandas as pd                                        # Alternative for XLRD
import numpy                                               # Helper for pandas

## -----------------------DESIGN AMBIENT BOUNDARIES----------------------##
design_location               = '3_Upington2013'           # 1_Seville - 2_Ouarzazate - 3_Upington2013 - 4_UpingtonSpot -
                                                                # 5_UpingtonFixed - 6_Calama - 7_Daggett

design_mode                   = 7                          # Design mode
                                                                # 1: DNI,T for given day and time (see below for day and tsolar, DNI and T are calculated)
                                                                # 2: DNI,T for summer solstice at noon (at location, DNI and T are calculated)
                                                                # 3: DNI,T for winter solstice at noon (at location, DNI and T are calculated)
                                                                # 4: DNI,T for Spring Equinox (at location, DNI and T are calculated)
                                                                # 5: DNI,T fixed by user together with design date (for solar position. see below for DNI and T)
                                                                # 6: DNI,T for maximum DNI and T (at location)
                                                                # 7: Not considered

design_DNI                    = 800                        # Direct Normal Irradiance (necessary for design mode 5)

design_TinHPTset              = 2                          # 1: evaluated by means of rec.Tset
                                                                # 2: fixed by means of PC.TinHPT

design_ToutRHset              = 3                          # 1: fixed by means of PC.RH.TTD as a temperature difference with respect Tset
                                                                # 2: fixed by means of PC.TdropRH as a percentage
                                                                # 3: CHP

design_HTFloop_set            = 0                          # 1: on
                                                                # 0: off

## -----------------------DYNAMIC PLANT MODEL----------------------------##
model_tool                    = 'TRNSYS'                # Transient simulation software      [-]
##-----------------------------------------------------------------------##
model_location                = int(design_location[0])              # Location identity number           [-]
model_wFile                   = design_location +'_weather'    # Weather file of the location        [-]
model_dt                      = 7.5                             # Dynamic model timestep            [min]
model_maxIter                 = 50                              # Maximum internal iterations        [#]
model_errConv                 = 1e-3                            # Relative error on convergence      [-]
model_tWait                   = 320*50                          # Maximum waiting time before error  [s]
model_hrSim                   = 8760                            # Simulation duration                [h]


# Economics

# Fuel economics
Fuel_type                     = 4

    # WoodPellets             = 1
    # WoodChips               = 2
    # LNG                     = 3
    # VATTENFALL              = 4

# Fuel excel file path
Fuel_table                    = xlrd.open_workbook(r'C:\DYESOPT\DYESOPT\DesignParameters\fuel.xlsx')
sheet                         = Fuel_table.sheet_by_index(0)
Fuel_LHV                      = sheet.cell_value(rowx=int(Fuel_type), colx=1)    # [kJ/kg]
Fuel_Cost                     = sheet.cell_value(rowx=int(Fuel_type), colx=2)    # reference cost of the fuel [USD/tonne]
Fuel_BiomassFeedstock         = 624                                              # ton/day of wood waste to be reintegrated

econ_Flag_Price               = 100                                              # minimum electricity price to start ops [USD]
econ_PPA                      = 1                                                # 1: yes  0: NO    - use PPA (only for South Africa)
econ_Discount_rate            = 0.1
F_Lifespan                    = 25

# steam turbogenerator set economics

econ_STG_Cost_ref             = 110    # reference cost of the steam turbogenerator set [USD/kW]
econ_STG_Size_ref             = 80000  # reference size of the steam turbogenerator set [kW]
econ_STG_Scale_ref            = 0.67   # reference scale factor for cost and size of the steam turbogenerator set [-]

# Condenser and coolin tower economics
econ_Cond_Cost_ref            = 250    # reference cost of the condenser [USD/m2]
econ_mf_Cost_ref              = 650    # reference cost of the cooling flow [USD/kg/s]
econ_Cond_MS_index            = 1.56   # Marshall & Swift index

#Boiler Corr Factor economics
econ_Boiler_corr_factor       = 2      #account for the higher steam pressure in Vattenfall w.r.t. the literature
##-----------------------------------------------------------------------##
# CONTROL STRATEGIES
CTRL_Strong_Grid              = 0      # 1: yes  0: NO

