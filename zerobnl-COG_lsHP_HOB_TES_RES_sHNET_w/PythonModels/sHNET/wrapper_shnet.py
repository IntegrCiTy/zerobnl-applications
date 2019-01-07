import json

from zerobnl.kernel import Node

import numpy as np


class sHnet(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        #Inputs (set)
        self.HNET_QDH_1 = 2000.
        self.HNET_QDH_2 = 2000.
        self.HNET_TsSET = 75.
        #Outputs
        self.HNET_QDH = 2000. / 1000. * 35490.
        self.HNET_MDOTtot = 507.
        #Internal variables (get)
        self.cp = 4.186
        self.HNET_Tr = 54.56
        
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
        
        a= self.HNET_QDH_1 - 0.1 * self.HNET_QDH_1
        b= self.HNET_QDH_1 + 0.1 * self.HNET_QDH_1
        self.HNET_QDH_1r = (b - a) * np.random.random_sample() + a

        c= self.HNET_QDH_2 - 0.1 * self.HNET_QDH_2
        d= self.HNET_QDH_2 + 0.1 * self.HNET_QDH_2
        self.HNET_QDH_2r = (d - c) * np.random.random_sample() + c		
		
		
        self.HNET_QDH = (self.HNET_QDH_1 + self.HNET_QDH_2+self.HNET_QDH_1r + self.HNET_QDH_2r)/ 1000. * 35490./4	# kW tot
        #self.HNET_QDH = (self.HNET_QDH_1 + self.HNET_QDH_2)/ 1000. * 35490.	# kW tot
		
        self.HNET_MDOTtot = self.HNET_QDH/self.cp/(self.HNET_TsSET-self.HNET_Tr) # Portata piccola perché DT alto. O ingrandisco il vicinato o riduco il sizing del base load
		
if __name__ == "__main__":
    node = sHnet()
    node.run()
