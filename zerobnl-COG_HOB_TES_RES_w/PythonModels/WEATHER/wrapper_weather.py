import json

from zerobnl.kernel import Node

import numpy as np
from pyepw.epw import EPW

class Weather(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        # This is where you define the attribute of your model, this one is pretty basic.
        epw = EPW()
        self.epw.read(r"SWE_Stockholm.Arlanda.024600_IWEC.epw")
		self.VdryBulb = np.empty([24])
        for wd in self.epw.weatherdata:
            self.VdryBulb = wd.dry_bulb_temperature
			
        self.ii = 0

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
        
        self.VdryBulb = self.VdryBulb(self.ii)
        self.ii+1			     
		
if __name__ == "__main__":
    node = Weather()
    node.run()
