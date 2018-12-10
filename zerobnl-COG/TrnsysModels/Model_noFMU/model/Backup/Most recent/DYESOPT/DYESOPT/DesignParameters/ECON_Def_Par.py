# Here the default parameters for economics of PV/CSP technology are set.

##
econ_ITC                            = 30                          # Investment tax credit #               [#]
econ_currencyrate                   = 1.0672                      # Currency Exchange rate                [EUR/USD] # Price in USD (average exchange rate in 2014 after www.irs.gov)
econ_i                              = 0.10                        # Real debt interest rate#              [-]
econ_n                              = 20                          # Power plant lifetime#                 [yrs]
econ_ncon                           = 2                           # Plant construction time               [yrs]
                                                                       # - 1 yr for PV/PV-battery
                                                                       # - 2 yrs for CSP/PV-CSP
econ_kins                           = 0.01                        # Capital insurance rate#               [-]
econ_cont                           = 0.10                        # Direct CAPEX contingency (for CSP)    [-]
econ_decom                          = 0                           # Plant decomissioning cost#            [-]
econ_SalesTax                       = 0.075                       # Sales tax                             [-]

##only MS---------------------------------------------------------------##
econ_fixedtariff                    = 1                           # Fixed tariff for 'case' 5          [USD/MWh]

## FINANTIAL models specifications---------------------------------------##

fin_model                           = 'noFIN' 
                                                                  # noFIN
                                                                  # SO single owner
                                                                  # AEPF all equity partnership flip
                                                                  # LPF leveraged partnership flip
                                                                  # SAL sale and leaseback
fin_utility                         =  'SCE' 
                                                                  # (for U.S.)
                                                                  # Chosen utility (for tariff scheme calculations)
                                                                  # - known_prices  =  prices are known through market data
                                                                  # - UD  =  Uniform Dispatch Scheme (i.e. no specific utility, all TOD factors are equal to1)
                                                                  # - SCE  =  Southern California Edison
                                                                  # - PG&E  =  Pacific Gas & Electric
                                                                  # - SDG&E  =  San Diego Gas & Electric

##-----------------------------------------------------------------------##
fin_PropTax                         = 0.01                        # property TAX                          [-]
fin_IncTax                          = 0.35                        # income TAX                            [-]
fin_icon                            = 0.115                       # cost of construciton loan             [-]
                                                                  # - (for alternative NPV calculation)
fin_deg_CSP                         = 0.1                         # Degradation                           [#]
fin_deg_PV                          = 0.79 
fin_deg_battery                     = 0 

fin_infl                            = 3                           # Inflation                             [#]
fin_esc                             = 3                           # PPA escalation                        [#]
fin_depr                            = 2                           # Depreciation                          [#]
                                                                  # - 0 = linear (always 20 years)
                                                                  # - 1 = accelerating
                                                                  # - 2 = MACRS (5 years for solar installations in the US)
fin_PPA                             = 1                           # PPA tariff first year               [USD/MWh]
##-----------------------------------------------------------------------##
# required input for 1: single owner
fin_iequity                         = 0.135                       # cost of equity                        [-]
fin_idebt                           = 0.09                        # cost of debt                          [-]
fin_xdebt                           = 0.7                         # share of debt                         [-]
fin_nloan                           = 16                          # duration of loan                     [yrs]
##-----------------------------------------------------------------------##
# required input for 2: all equity partnership flip
fin2_xequity                        = 0.60                        # fraction of equity (TCI)              [-]
fin2_iequity                        = 0.135                       # cost of equity (TCI) =  req IRR       [-]
fin2_ideveloper                     = 0.03                        # cost of equity (development fee)      [-]
fin2_Tpart1                         = 0.99                        # tax allocation before flip (TCI)      [-]
fin2_Tpart2                         = 0.90                        # tax allocation after flip (TCI)       [-]
fin2_DCpart1                        = 0.00                        # income allocation before flip (TCI)   [-]
fin2_DCpart2                        = 0.99                        # income allocation after flip (TCI)    [-]
fin2_DCpart3                        = 0.90                        # income allocation after 2.flip (TCI)  [-]
##-----------------------------------------------------------------------##
# required input for 3: leverage partnership flip from view of  TCI
fin3_idebt                          = 0.11                        # cost of debt                          [-]
fin3_nloan                          = 20                          # duration of loan                     [yrs]
fin3_xequity                        = 0.98                        # contribution of equity (TCI)          [-]
fin3_iequity                        = 0.135                       # cost of equity (TCI) =  IRR target    [-]
fin3_ideveloper                     = 0.03                        # cost of equity (development fee)      [-]
fin3_Tpart1                         = 0.98                        # tax allocation before flip (TCI)      [-]
fin3_Tpart2                         = 0.10                        # tax allocation after flip (TCI)       [-]
fin3_DCpart1                        = 0.98                        # income allocation before flip (TCI)   [-]
fin3_DCpart2                        = 0.10                        # income allocation after flip (TCI)    [-]
fin3_DSCRmin                        = 1.3                         # min. allowed debt service coverage ratio
fin3_IRR_target_year                = 20                          # predefined flip point                 [-]
##-----------------------------------------------------------------------##
# required input for 4: sale and lease back
fin4_iequity                        = 0.135                       # cost of equity (TCI) =  IRR target    [-]
fin4_LSCRmin                        = 1.3                         # min. allowed lease service coverage ratio
fin4_LPesc                          = 3                           # lease payment escalation             [#/a]
fin4_ideveloper                     = 0.03                        # development fee                       [#]
