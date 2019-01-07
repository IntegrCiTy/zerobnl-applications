import json

from zerobnl.kernel import Node

import numpy as np


class Ctrl(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        #Inputs (set)
        self.demandOK = 1
        self.demandOK_mdot = 1
        self.demandOK_price = 0
        #Outputs
        self.COG_FlagOUT = -1
        self.LSHP_FlagOUT = -1		
        self.TEScog_FlagOUT = -1
        self.TESlshp_FlagOUT = -1		
        self.HOB_FlagOUT = -1		
        #Internal variables (get)
        self.PRflag = -1
        self.priority = np.empty([1])		
        self.COG_plant = {'Name':'COGplant','Flag': self.COG_FlagOUT}
        self.LSHP_plant = {'Name':'LSHPplant','Flag': self.LSHP_FlagOUT}
        self.TES_plantCOG = {'Name':'TESplantCOG','Flag': self.TEScog_FlagOUT}
        self.TES_plantLSHP = {'Name':'TESplantLSHP','Flag': self.TESlshp_FlagOUT}
        self.HOB_plant = {'Name':'HOBplant','Flag': self.HOB_FlagOUT}

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


        if self.demandOK < 0 or self.demandOK_mdot < 0: # satisfied: 1; not satisfied: -1 OBS!! This is based on the indoor temperature		
		
            self.PRflag = -1
			
            print('The capacity in the building is over')	
			
        else:
		
            self.TEScog_FlagOUT = 0
            self.TESlshp_FlagOUT = 0 			
            self.HOB_FlagOUT = -1          

        
        if self.PRflag < 0: # set: 1; not set: -1

            self.priority = np.empty([3])
			
			# You are going to have a function here or maybe a separated model?
			# The priority will be set based on operational costs of the different options.
			# There will be more than one vector based on the time of the day, thus depending on
			# weather conditions , level of the demand and costs.
            self.priority = [self.COG_plant,self.LSHP_plant,self.TES_plantCOG,self.TES_plantLSHP,self.HOB_plant]
            self.PRflag = 1
			
            print('Priority is set')
			
            for plant in self.priority:
			
                plant['Flag'] = 1 	
                if plant['Name'] == "COGplant" and self.demandOK_price == 1:
                   self.COG_FlagOUT = plant['Flag']
                   self.LSHP_FlagOUT = 0.				   
                elif plant['Name'] == "LSHPplant" and self.demandOK_price == 2:
                   self.LSHP_FlagOUT = plant['Flag']
                   self.COG_FlagOUT = 0.
				   
                if plant['Name'] == "TESplantCOG" and self.COG_FlagOUT==1:
                    if self.demandOK_mdot == -1 :
                       self.TEScog_FlagOUT = plant['Flag'] # Discharge
                    elif self.demandOK_mdot == -3:
                       self.TEScog_FlagOUT = -1 # Charge
                    else:
                       self.TEScog_FlagOUT = 0 # Nothing happens
					   
                if plant['Name'] == "TESplantLSHP" and self.LSHP_FlagOUT==1:
                    if self.demandOK_mdot == -1 :
                       self.TESlshp_FlagOUT = plant['Flag'] # Discharge
                    elif self.demandOK_mdot == -3:
                       self.TESlshp_FlagOUT = -1 # Charge
                    else:
                       self.TESlshp_FlagOUT = 0 # Nothing happens
				
                if plant['Name'] == "HOBplant" and (self.demandOK == -2 or self.demandOK_mdot == -2):
                   self.HOB_FlagOUT = plant['Flag']
                else:
                   self.HOB_FlagOUT = -1
			
                print('Plants are activated')
			
		
		
if __name__ == "__main__":
    node = Ctrl()
    node.run()
