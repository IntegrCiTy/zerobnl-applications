from Core.Interface.standardTRNSYSdata import *

#convert sec to hrs#
TRNSYS_data_dtSim = round((TRNSYS_data_dtSim / 3600)*100)/100  ##Osama--> rounding function brings 12.5 to 12 instead of 13, i.e not necessarily to the higher integer, that's a python thing

