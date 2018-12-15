import json

from zerobnl.kernel import Node

import numpy as np


class CDem(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        # This is where you define the attribute of your model, this one is pretty basic.
        self.CDEM_TR = 30.
        self.CDEM_mdotR = 0.04	
        self.Ts_second = 55. 
        self.CDEM_cmf = 1.

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
        
        self.CDEM_TR = self.Ts_second - 30.
        self.CDEM_mdotR = 0.04		
        self.CDEM_cmf = 1.


if __name__ == "__main__":
    node = CDem()
    node.run()
