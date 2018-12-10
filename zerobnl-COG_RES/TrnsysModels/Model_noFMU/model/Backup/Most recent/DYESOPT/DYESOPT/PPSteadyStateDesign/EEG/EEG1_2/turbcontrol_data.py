import numpy as np
from PPSteadyStateDesign.EEG.EEG1_2.PowerBlock import *
# start-up-data for SST-900

# values for Cast Iron
overallUvalue	=5.7               #[W/(m^2 K)], reference: http://www.engineeringtoolbox.com/overall-heat-transfer-coefficients-d_284.html
cpcastiron      =460               #[J/(kg K)], reference: http://www.engineeringtoolbox.com/specific-heat-metals-d_152.html
Densitycastiron	=(7800+6800)/2     #[Kg/m^3], (Assumed in the middle of the range) reference: http://www.engineeringtoolbox.com/metal-alloys-densities-d_50.html

heightcasing	=10                #[m]
lengthcasing	=20.5              #[m], including generator
widthcasing     =11                #[m]

#Acasing=2*heightcasing*lengthcasing/2+2*lengthcasing*widthcasing/2+2*heightcasing*widthcasing;  #Assumed as a rectangular box,	Area of Steam turbine casing, reference: Siemens - Industrial steam turbines catalogue
Acasing=2*(heightcasing*lengthcasing+heightcasing*widthcasing+lengthcasing*widthcasing)    #[m2]
Thicknesscasing	=0.25      #[m] Assumed

Masssteamturbine=Acasing*Densitycastiron*Thicknesscasing                                   #[kg] Assumed as the area x thickness of 0.25 m x and the density of cast iron

Timeconstant=Masssteamturbine*cpcastiron/(3600*overallUvalue*Acasing)                      #[hours]
Tempambient=25                                                                             #[C] Assumed

#Calculations with respect to HPT
#Time to reach the hot/warm casing-temperature border for start-up
Thot=410                                                                                   #[C], Hot to Warm start-up Border temperature
Thottimezero=PC_st[13,0]                                                                   #[C], taken as the rated temprature of SH steam
TBHWS=(-np.log((Thot-Tempambient)/(Thottimezero-Tempambient)))*Timeconstant                #[hours]

#Time to reach the warm/cold casing-temperature border for start-up
Twarm=200                                                                                  #[C], Warm to Cold start-up Border temperature
Twarmtimezero=PC_st[13,0]                                                                  #[C], taken as the rated temprature of SH steam
TBWCS=(-np.log((Twarm-Tempambient)/(Twarmtimezero-Tempambient)))*Timeconstant              #[hours]

#Data for turbcontrol component based on start-up curves (All low curves have been used (as it is a concentrated solar application))
SDH=0.067                                                                                  #[hours] Turbine sync. delay (hot)
SDW=0.617                                                                                  #[hours] Turbine sync. delay (warm)
SDC=1.5                                                                                    #[hours] Turbine sync. delay (cold)
RDH=0.517                                                                                  #[hours] Ramp delay (hot)
RDW=1.133                                                                                  #[hours] Ramp delay (warm)
RDC=1.833                                                                                  #[hours] Ramp delay (cold)

Des_SupHt=30                                                                               #[C] Assumed 30 as the superheat degree should be 30 to 50 C higher than the Sat. Temp.
Rampdown=0.5                                                                               #[hours] RAMPDOWN (assumed: 30 mins)

#Desired Steam Pressure
DesiredSteamPressureHot=29.165                                                             #[bar]
DesiredSteamPressureWarm=28.820                                                            #[bar]
DesiredSteamPressureCold=29.170                                                            #[bar]

#Desired Steam Temperature
DesiredSteamTemperatureHot=480.6                                                           #[C]
DesiredSteamTemperatureWarm=420.2                                                          #[C]
DesiredSteamTemperatureCold=400.6                                                          #[C]


PC_turbcontrol_TBHWS=TBHWS                                                                 #[hours] Time to reach the hot/warm start-up border
PC_turbcontrol_TBWCS=TBWCS                                                                 #[hours] Time to reach the warm/cold start-up border
PC_turbcontrol_SDH=SDH                                                                     #[hours] Turbine sync. delay (hot)
PC_turbcontrol_SDW=SDW                                                                     #[hours] Turbine sync. delay (warm)
PC_turbcontrol_SDC=SDC                                                                     #[hours] Turbine sync. delay (cold)
PC_turbcontrol_RDH=RDH                                                                     #[hours] Ramp delay (hot)
PC_turbcontrol_RDW=RDW                                                                     #[hours] Ramp delay (warm)
PC_turbcontrol_RDC=RDC                                                                     #[hours] Ramp delay (cold)

PC_turbcontrol_Des_SupHt=Des_SupHt                                                         #[C] Assumed 30 as the superheat degree should be 30 to 50 C higher than the Sat. Temp.
PC_turbcontrol_Rampdown=Rampdown                                                           #[hours] RAMPDOWN (assumed: 30 mins)

#Desired Steam Pressure
PC_turbcontrol_DesiredSteamPressureHot=DesiredSteamPressureHot                             #[bar]     Hot start, Desired Steam Pressure Hot
PC_turbcontrol_DesiredSteamPressureWarm=DesiredSteamPressureWarm                           #[bar]     Warm start, Desired Steam Pressure Warm
PC_turbcontrol_DesiredSteamPressureCold=DesiredSteamPressureCold                           #[bar]     Cold start, Desired Steam Pressure Cold

#Desired Steam Temperature
PC_turbcontrol_DesiredSteamTemperatureHot=DesiredSteamTemperatureHot                       #[C]   Hot start, Desired Steam Temperature Hot
PC_turbcontrol_DesiredSteamTemperatureWarm=DesiredSteamTemperatureWarm                     #[C]   Warm start, Desired Steam Temperature Warm
PC_turbcontrol_DesiredSteamTemperatureCold=DesiredSteamTemperatureCold                     #[C]   Cold start, Desired Steam Temperature Cold


