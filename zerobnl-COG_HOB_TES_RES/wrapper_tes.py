import json

from zerobnl.kernel import Node

import numpy as np


class Tes(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

		#Inputs (set)
        self.TES_FlagIN = 0	
        self.TES_Tin = 54.
        self.TES_MDOTinC = 507.
        self.TES_MDOTinD = 507.
        
		#Outputs (get)        
        self.TES_socOUT = 1	
        self.TES_MDOToutC = 507. # Fake for the moment
        self.TES_MDOToutD = 507.
        self.TES_ToutD = 75. 
        self.TES_ToutC = 75. # Fake for the moment 		
		#Internal variables
        self.TES_dT = 21.        

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
        
		# For the moment I assume a gradient dT
        self.TES_dT = 21.
				
        if self.TES_FlagIN > 0.5: # Discharge TES		
           self.TES_Tin = 54. # I also assume a Tin since I plan to use fgc to reach this temperature		
           self.TES_ToutD = self.TES_Tin + self.TES_dT	
           self.TES_MDOToutD = self.TES_MDOTinD 		   
        elif self.TES_FlagIN < 0.5: # Charge TES
           self.TES_ToutC = self.TES_Tin - self.TES_dT
           self.TES_MDOToutC = self.TES_MDOTinC 		   
        else: # Nothing happens
           self.TES_Tout = self.TES_Tin
           self.TES_MDOToutD = 0.
           self.TES_MDOToutC = 0.
           self.TES_MDOToutD = self.TES_Tin
           self.TES_MDOToutC = self.TES_Tin
		
        self.TES_socOUT = 1 # This has to be properly simulated!! charged: 1 ; discharged:-1		


if __name__ == "__main__":
    node = Tes()
    node.run()
