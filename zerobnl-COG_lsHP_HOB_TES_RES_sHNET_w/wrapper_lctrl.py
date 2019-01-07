import json

from zerobnl.kernel import Node

import numpy as np


class Lctrl(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        # This is where you define the attribute of your model, this one is pretty basic.
        #Inputs (set)		
        self.TindoorIN_0 = 20.
        self.TindoorIN_1 = 20.
        self.mdotTOT = 507.        
        self.TEScog_socIN = 1
        self.TESlshp_socIN = 1
        self.ToutdoorP = 0.
        #Outputs (get)
        self.demandFlag = 0 
        self.demandFlag_mdot = 0
        self.Tth_0 = 20.
        self.Tth_1 = 20.		
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
	    
        TindoorVector = [self.TindoorIN_0,self.TindoorIN_1]
        TthVector = [self.Tth_0,self.Tth_1]
		
        d={}
		
        ii=0
		
        for Tindoor in TindoorVector:
		
            self.demandFlag = 0            
            Tth = TthVector[ii]			
		
            if  self.TsetP > self.TS_bl: # Request for a Tsupply higher than the BL (75 Cdeg)
                if Tindoor >= self.TindoorMIN and Tth >= self.TindoorMIN: # First check the possibility to use the capacity in the buildings
                   Tth = max(Tth -1,18.) 
                   self.demandFlag = 1 #--> Tth
                else:
                   self.demandFlag = -2 #--> HOBS # !! Un paio di volte arriva qui perché la Tindoor scende a 17.9
				
            if  self.mdotTOT > self.mdot_bl:  # Request for a Mdot higher than the BL
                if Tindoor >= self.TindoorMIN and Tth >= self.TindoorMIN: # First check the possibility to use the capacity in the buildings
                   Tth = max(Tth -1,18.) 
                   self.demandFlag_mdot = 1 #--> Tth # !! si ferma qui ma non si sa se sia sufficiente e sovrascrive il -2 di prima
                elif self.TEScog_socIN or self.TESlshp_socIN > -1:
                   self.demandFlag_mdot = -1 #--> TES discharge
                else:
                   self.demandFlag_mdot = -2 #--> HOBS
			   
            else:
                Tth = min(Tth + 1, 22.) # Since there is surplus, fill in the capacity in the buildings
                if self.TEScog_socIN or self.TESlshp_socIN < 1:
                   self.demandFlag_mdot = -3 #--> TES charge
                else:
                   print("Heat is being wasted")
            
            #d["self.Tth{0}".format(ii)]=Tth	
            if ii == 0:
               self.Tth_0 = Tth 
            elif ii == 1:
               self.Tth_1 = Tth
			   
            ii = ii+1				
				
		
if __name__ == "__main__":
    node = Lctrl()
    node.run()
