import json

from zerobnl.kernel import Node

import numpy as np


class Isel(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        #Inputs (set)
        self.soo1 = 1 # ex. COG
        self.mdot1 = 507
        self.Tin1 = 75.
        self.soo2 = 1 # ex. TES
        self.mdot2 = 100
        self.Tin2 = 75.
        #Outputs
        self.mdot = 507.
        self.Tout =	75.	
        #Internal variables (get)

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

        #Inputs (set)
        self.soo1 = 1 # ex. COG
        self.mdot1 = 507
        self.Tin1 = 75.
        self.soo2 = 1 # ex. TES
        self.mdot2 = 100
        self.Tin2 = 75.
        #Outputs
        self.mdot = 507.
        self.Tout =	75.	
      
        if self.soo1 > 0.5 and self.soo2> 0.5:
		
           self.mdot = self.mdot1 + self.mdot2
           self.Tout = (self.Tin1*self.mdot1 + self.Tin2*self.mdot2)/ self.mdot	
		   
        else:		
		
            if self.soo1 > 0.5:
		   
               self.mdot = self.mdot1
               self.Tout = self.Tin1
			  
            elif self.soo2> 0.5:

               self.mdot = self.mdot2
               self.Tout = self.Tin2			
		
		
if __name__ == "__main__":
    node = Isel()
    node.run()
