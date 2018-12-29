import json

from zerobnl.kernel import Node

import numpy as np


class Lctrl(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        # This is where you define the attribute of your model, this one is pretty basic.
        #Inputs (set)		
        self.TindoorIN = 20.
        self.mdotTOT = 507.        
        self.TES_socIN = 1
        self.ToutdoorP = 0.
        #Outputs (get)
        self.demandFlag = 0 
        self.demandFlag_mdot = 0
        self.Tth = 20.
        self.TsetP = 75. # Fake for the moment. There should be a function that calcuates it based on weather.
        #Internal variables
        self.TS_bl = 75.
        self.mdot_bl = 507.
        self.TindoorMIN = 19.
        self.TindoorMAX = 22.
        self.TsetMatrix = np.loadtxt("TS_set.txt", comments='#', delimiter='\t', converters=None, skiprows=2, usecols=(0,1), unpack=False, ndmin=0)   

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
                
        self.TsetP = np.interp(self.ToutdoorP,self.TsetMatrix[:,0],self.TsetMatrix[:,1]) # Supply set point based on outdoor temperature
	
        self.demandFlag = 0
		
        if  self.TsetP > self.TS_bl: # Request for a Tsupply higher than the BL (75 Cdeg)
            if self.TindoorIN >= self.TindoorMIN and self.Tth >= self.TindoorMIN: # First check the possibility to use the capacity in the buildings
               self.Tth = max(self.Tth -1,18.) 
               self.demandFlag = 1 #--> Tth
            else:
               self.demandFlag = -2 #--> HOBS # !! Un paio di volte arriva qui perché la Tindoor scende a 17.9
				
        if  self.mdotTOT > self.mdot_bl:  # Request for a Mdot higher than the BL
            if self.TindoorIN >= self.TindoorMIN and self.Tth >= self.TindoorMIN: # First check the possibility to use the capacity in the buildings
               self.Tth = max(self.Tth -1,18.) 
               self.demandFlag_mdot = 1 #--> Tth # !! si ferma qui ma non si sa se sia sufficiente e sovrascrive il -2 di prima
            elif self.TES_socIN > -1:
               self.demandFlag_mdot = -1 #--> TES discharge
            else:
               self.demandFlag_mdot = -2 #--> HOBS
			   
        else:
            self.Tth = min(self.Tth + 1, 22.) # Since there is surplus, fill in the capacity in the buildings
            if self.TES_socIN < 1:
               self.demandFlag_mdot = -3 #--> TES charge
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
