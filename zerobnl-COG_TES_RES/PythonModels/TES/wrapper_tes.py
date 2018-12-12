import json

from zerobnl.kernel import Node

import numpy as np


class Tes(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        # This is where you define the attribute of your model, this one is pretty basic.
        self.a = 0
        self.b = 0

        self.y = None

        self.c = None

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
		self.TES_dT = 35.
		
        if self.TES_flag > 0.5: # Discharge TES			
			self.TES_Tout = self.TES_Tin + self.TES_dT
		elif  self.TES_flag < 0.5: # Charge TES
			self.TES_Tout = self.TES_Tin - self.TES_dT
		else: # Nothing happens
			self.TES_Tout = self.TES_Tin


if __name__ == "__main__":
    node = MyNode()
    node.run()
