import json

from zerobnl.kernel import Node

import numpy as np


class Lctrl(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        # This is where you define the attribute of your model, this one is pretty basic.
        self.TS_bl = 75
        self.mdot_bl = 507
        self.TindoorMIN = 19
        self.TindoorMAX = 22
		
        self.TsetP = 75. 
        self.demandFlag = 0 
        self.Tindoor = 20
        self.Tth = 19				
        self.mdotTOT = 507        
        self.TES_soc = 1
               

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
        
        self.TsetP = 75. #self.TsetP = f(self.Toutdoor)
        self.demandFlag = 0
		
        if  self.TsetP > self.TS_bl:
            if self.Tindoor > self.TindoorMIN:
               self.Tth = self.Tth -1 
               self.demandFlag = 1 #--> Tth
            else:
               self.demandFlag = -2 #--> HOBS
				
        if  self.mdotTOT > self.mdot_bl:
            if self.Tindoor > self.TindoorMIN:
               self.Tth = self.Tth -1 
               self.demandFlag = 1 #--> Tth
            elif self.TES_soc > 0:
               self.demandFlag = -1 #--> TES discharge
            else:
               self.demandFlag = -2 #--> HOBS
			   
        else:
            if self.TES_soc < 0:
               self.demandFlag = -3 #--> TES charge
            else:
               print("Heat is being wasted")
				
		
		#self.Tindoor --> self.Tth
		#demandFlag = 1 --> Tth
		#demandFlag = 0 --> bl
		#demandFlag = -1 --> TES
		#demandFlag = -2 --> HOBS
		
		
if __name__ == "__main__":
    node = Lctrl()
    node.run()
