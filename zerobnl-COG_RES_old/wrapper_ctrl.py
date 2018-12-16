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
		
        self.CAPBflag = -1
		
        self.demandOK = 18
		
        self.COG_plant = {'Name':'COGplant','Flag': self.COGwflag}

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

            self.priority = np.empty([1])
			
			# You are going to have a function here or maybe a separated model?
			# The priority will be set based on operational costs of the different options.
			# There will be more than one vector based on the time of the day, thus depending on
			# weather conditions , level of the demand and costs.
            self.priority = [self.COG_plant]
            self.PRflag = 1
			
            print('Priority is set')
			
            for plant in self.priority:
			
                plant['Flag'] = 1 	
                if plant['Name'] == "COGplant":
                   self.COGwflag = plant['Flag']
			
                print('Plants are activated')
			
            if self.demandOK < 18: # satisfied: 1; not satisfied: -1 OBS!! This is based on the indoor temperature		
		
                self.PRflag = -1
			
                print('The capacity over the building is over')
			
		    ##
			#Check if your can use the CAPB: if demand is -1 then you need the HOB to intervene
		    ##
			# search for the first 0 and turn it to 1
					
			#ii = 0
			
			#for plant in self.priority:
			
			#	if ii == 0:
				
			#		plant['Flag'] = 1 	
			
			#		ii=ii+1
			
			#self.priority.remove(self.priority(0))
			#self.priority[:] = [d for d in self.priority if d.get('Flag') != 1]	

			#print('The demand is being processed')
			
		#else: # Display an error that the sizing is wrong
		     
		
if __name__ == "__main__":
    node = Ctrl()
    node.run()
