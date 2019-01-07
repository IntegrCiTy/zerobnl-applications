import json

from zerobnl.kernel import Node

import numpy as np


class Pctrl(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        # This is where you define the attribute of your model, this one is pretty basic.
        #Inputs (set)		

        #Outputs (get)
        self.demandFlag_price = 0 

        #Internal variables
		# File with costs figures
        self.name1 = "COGWaste"
        self.CostFigure1 = np.loadtxt(self.name1+'_cost.txt',skiprows=0)	  
        self.name2 = "LSHP"
        self.CostFigure2 = np.loadtxt(self.name2+'_cost.txt',skiprows=0)
        self.COG_EFFe = 0.37

        self.PelSpot = np.loadtxt('ElPrices2016_Stockholm.txt',skiprows=3)	
        self.ii=0
        self.jj=0

    def set_attribute(self, attr, value):
        """This method is called to set an attribute of the model to a given value, you need to adapt it to your model."""
        super().set_attribute(attr, value)  # Keep this line, it triggers the parent class method.
        setattr(self, attr, value)

    def get_attribute(self, attr):
        """This method is called to get the value of an attribute, you need to adapt it to your model."""
        super().get_attribute(attr)  # Keep this line, it triggers the parent class method.
        return getattr(self, attr)

    def step(self, value):
        """This method is called to make a step, you need to adapt it to your model."""
        super().step(value)  # Keep this line, it triggers the parent class method.
 
        # Always use the fuel as specific unit 
        # OPEX variable Plant 
        OPEXvariable1 = self.CostFigure1[2] #40 sek/MWh* efficiencycorrection for everyone (I mean below also)# From ElForsk [kr/MWh_fuel]
        OPEXvariable2 = self.CostFigure2[2] #5.1 sek/MWh* efficiencycorrection for everyone (I mean below also)# From ElForsk [kr/MWh_fuel]
		
        #Fuel cost
        if self.CostFigure2[3] == -1: # Required double
           Fuel1 = self.CostFigure1[3] #Time series
           Fuel2 = self.PelSpot[self.ii]# Time series
           self.ii=self.ii+1
		   
        else:
           Fuel1 = self.CostFigure1[3]# -130 From ElForsk [sek/MWh_fuel/y]
           Fuel2 = self.CostFigure2[3]# 1000 From ElForsk [sek/MWh_fuel/y]

        # Total Plant plus network
        OPEXtot1 = OPEXvariable1 + Fuel1
        OPEXtot2 = OPEXvariable2 + Fuel2		

        # Revenues
        if self.CostFigure1[4] == -1: # Required double
           Rev1 = self.PelSpot[self.jj]# Time series
           self.jj=self.jj+1
           Rev2 = self.CostFigure2[4] # 0
		   
        else:
           Rev1 = self.CostFigure1[4] * self.COG_EFFe# 150 sek/MWhe -->sek/MWhp
           Rev2 = self.CostFigure2[4] # 0	

        # Substract
        opexV1 = OPEXtot1 - Rev1 # Eff correction needed
        opexV2 = OPEXtot2 - Rev2 # Eff correction needed

#Take the minimum
        if opexV1 < opexV2:
           self.demandFlag_price = 1 # COG
        else:
           self.demandFlag_price = 2 # LSHP
		
if __name__ == "__main__":
    node = Pctrl()
    node.run()
