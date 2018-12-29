import json

from zerobnl.kernel import Node

import numpy as np


class Ctrl(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        # This is where you define the attribute of your model, this one is pretty basic.
        self.PRflag = -1

        self.priority = np.empty([1])
		
        self.COGwflag = -1
		
        self.demandOK = 1
		
        self.TESflag = -1
		
        self.HOBflag = -1
		
        self.demandOK = 1
		
        self.COG_plant = {'Name':'COGplant','Flag': self.COGwflag}
        self.TES_plant = {'Name':'TESplant','Flag': self.TESflag}
        self.HOB_plant = {'Name':'HOBplant','Flag': self.HOBflag}

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
        
        if self.PRflag < 0: # set: 1; not set: -1

            self.priority = np.empty([2])
			
			# You are going to have a function here or maybe a separated model?
			# The priority will be set based on operational costs of the different options.
			# There will be more than one vector based on the time of the day, thus depending on
			# weather conditions , level of the demand and costs.
            self.priority = [self.COG_plant,self.TES_plant,self.HOB_plant]
            self.PRflag = 1
			
            print('Priority is set')
			
            for plant in self.priority:
			
                plant['Flag'] = 1 	
                if plant['Name'] == "COGplant":
                   self.COGwflag = plant['Flag']
				   
                if plant['Name'] == "TESplant" and self.demandOK == -1:
                   self.TESflag = plant['Flag']
                elif plant['Name'] == "TESplant" and self.demandOK == -3:
                   self.TESflag = -1
                else:
                   self.TESflag = 0
				
                if plant['Name'] == "HOBplant" and self.demandOK == -2:
                   self.HOBflag = plant['Flag']
                else:
                   self.HOBflag = -1
			
                print('Plants are activated')
			
            if self.demandOK < 0: # satisfied: 1; not satisfied: -1 OBS!! This is based on the indoor temperature		
		
               self.PRflag = -1
			
               print('The capacity in the building is over')			
		
if __name__ == "__main__":
    node = Ctrl()
    node.run()
