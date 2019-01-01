import json

from zerobnl.kernel import Node

import numpy as np


class Hob(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        # This is where you define the attribute of your model, this one is pretty basic.
        #Inputs (set)
        self.HOB_Tset = 75.
        self.HOB_Tin = 75.
        self.HOB_MDOTin = 507.
        self.HOB_FlagIN = 0.
        #self.HOB_TtesIN = 75.
        #self.HOB_MDOTtesIN = 0.
        #Outputs (get)
        self.HOB_Tout = 75. # Fake so far
        self.HOB_Q = 0. # Fake so far
        self.HOB_MDOTout = 507. # Fake so far
        #Internal variables
        self.HOB_cp = 4.186
        self.HOB_Qplus = 0.

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
        
        if self.HOB_FlagIN > 0.5: # For the moment is a 2 steps scale, but you should implement a refinement so that you can count how many hobs
            self.HOB_Tout = self.HOB_Tset
		   
            #if self.HOB_TtesIN < self.HOB_Tin:
             #  self.HOB_Qplus = self.HOB_MDOTtesIN * self.HOB_cp (HOB_Tin - self.HOB_TtesIN)
            #else:
             #  self.HOB_Qplus = 0.		   
		   
            self.HOB_Q = self.HOB_MDOTin * self.HOB_cp * (self.HOB_Tout - self.HOB_Tin) #+ self.HOB_Qplus
            self.HOB_MDOTout = self.HOB_MDOTin
        else:
            self.HOB_Tout = self.HOB_Tin
            self.HOB_MDOTout = 0.


if __name__ == "__main__":
    node = Hob()
    node.run()
