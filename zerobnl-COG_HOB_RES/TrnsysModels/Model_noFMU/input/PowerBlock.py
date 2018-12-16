from economizer import *
from evaporator import *

# I am currently understanding what do I need from the steadt state, so that it matches with the new TRNSYS layout.
# After this phase, I can go back to the RankineReheat

SteamIN_ECO = [225,125,0,0,0,0,0,35] # T, p, ..., mdot
SteamOUT_ECO = [292]
FlueGasIN_ECO = [410,6,0,51] # T, , ..., mdot

SteamIN_EV = [292,125,0,0,0,0,0,35]
FlueGasIN_EV = [600,6,0,51]
FlueGasOUT_EV = [410,6,0,51]

SteamIN_SH = [292,125,0,0,0,0,0,35]
SteamOUT_SH = [535]
FlueGasIN_SH = [1150,6,0,51]

[PC_ECO_EFF,   PC_ECO_UA]    = economizer(SteamIN_ECO,FlueGasIN_ECO,SteamOUT_ECO) 
[PC_EV_EFF,    PC_EV_UA]     = evaporator(FlueGasIN_EV,SteamIN_EV,FlueGasOUT_EV)               
[PC_SH_EFF,    PC_SH_UA]     = economizer(SteamIN_SH,FlueGasIN_SH,SteamOUT_SH)        
