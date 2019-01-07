import json

from zerobnl.kernel import Node

import numpy as np


class lsHp(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        # This is where you define the attribute of your model, this one is pretty basic.
        #Inputs (set)
        self.LSHP_FlagIN = -1
        self.LSHP_QDH = 2000. / 1000. * 35490.

        #Outputs (get)
        self.LSHP_ToutL = 75.
        LSHP_MDOTtoLOAD = 0.
        self.LSHP_soo = 0.
        self.LSHP_MDOTtoTES = 0.
        self.LSHP_MDOTfromTES = 0.
        self.LSHP_TTESin = 75.
		
        #Internal variables
        self.LSHP_cp = 4.186     
        self.LSHP_cop = 3.2
        self.LSHP_TinL = 54.56 # as for the cogeneration plant. The pre-heating is done with  fgc 
        self.mdot_bl = 507.
        self.LSHP_ToutLset = 75.

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

        self.LSHP_soo = self.LSHP_FlagIN
		
        if self.LSHP_FlagIN > 0.5:
		
		   self.LSHP_MDOTtot = self.LSHP_QDH/self.LSHP_cp/(self.LSHP_ToutLset-self.LSHP_TinL)

            if self.LSHP_MDOTtot > self.mdot_bl. #  ask from TES
		
               self.LSHP_ToutL = self.LSHP_ToutLset
               self.LSHP_MDOTtoTES = 0.
               self.LSHP_MDOTfromTES = self.LSHP_MDOTtot - self.mdot_bl
               self.LSHP_TTESin = self.LSHP_TinL 
               LSHP_MDOTtoLOAD = self.mdot_bl
		   
            else: #  To charge TES
			
               self.LSHP_ToutL = self.LSHP_ToutLset
               self.LSHP_MDOTtoTES = self.mdot_bl - self.LSHP_MDOTtot
               self.LSHP_MDOTfromTES = 0.
               self.LSHP_TTESin = self.LSHP_ToutLset	
               LSHP_MDOTtoLOAD = self.LSHP_MDOTtot			   
		
        else:
        
           self.LSHP_ToutL = self.LSHP_TinL
           self.LSHP_MDOTtot = 0.
           self.LSHP_MDOTtoTES = 0.
           self.LSHP_MDOTfromTES = 0.
           self.LSHP_TTESin = 75.
           LSHP_MDOTtoLOAD = 0.		   
      
        self.LSHP_PdotEl = (self.LSHP_MDOTtot - self.LSHP_MDOTfromTES)/self.LSHP_cop


if __name__ == "__main__":
    node = lsHp()
    node.run()
