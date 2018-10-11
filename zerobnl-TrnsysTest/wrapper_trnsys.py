import json

from docopt import docopt
from zerobnl.core import Node

import numpy as np
import fmipp
import os.path


class MyNode(Node):
	"""docstring for MyNode"""

	def __init__(self, name, group, inputs_map, outputs, init_values):  # If needed you can pass more values to your node constructor.
		super(MyNode, self).__init__(name, group, inputs_map, outputs, init_values)  # Keep this line, it triggers the parent class method.


		# This is where you define the attribute of your model, this one is pretty basic.
		# FMU loading
		work_dir = os.path.split(os.path.abspath(__file__))[0]  # define working directory
		model_name = 'HES3_2__TES1_1__EEG0__EES0'  # define FMU model name
		path_to_fmu = os.path.join(work_dir, model_name + '.fmu')  # path to FMU		
		uri_to_extracted_fmu = fmipp.extractFMU(path_to_fmu, work_dir)  # extract FMU		
		logging_on = False
		time_diff_resolution = 1e-9		
		self.fmu = fmipp.FMUCoSimulationV2(uri_to_extracted_fmu, model_name, logging_on, time_diff_resolution)
		print( 'successfully loaded the FMU' )

		## FMU instantiation
		start_time = 0.
		stop_time = 3600. * 24.  # 24 hours
		self.step_size = 3600. # 1 hour
		self.tempo=self.step_size
		instance_name = "trnsys_fmu_test"
		visible = False
		interactive = False
		status = self.fmu.instantiate(instance_name, start_time, visible, interactive)
		assert status == fmipp.fmiOK        
		print( 'successfully instantiated the FMU' )	

		## FMU initialization
		stop_time_defined = True
		status = self.fmu.initialize(start_time, stop_time_defined, stop_time)
		assert status == fmipp.fmiOK        
		print( 'successfully initialized the FMU' )  

	def set_attribute(self, attr, value):
		"""This method is called to set an attribute of the model to a given value, you need to adapt it to your model."""
		super(MyNode, self).set_attribute(attr, value)  # Keep this line, it triggers the parent class method.

		#setattr(self, attr, value)
		self.fmu.setRealValue(attr, value)
		assert self.fmu.getLastStatus() == fmipp.fmiOK  

	def get_attribute(self, attr):
		"""This method is called to get the value of an attribute, you need to adapt it to your model."""
		super(MyNode, self).get_attribute(attr)  # Keep this line, it triggers the parent class method.

		#return getattr(self, attr)
		print('base plus 60',attr)
		return self.fmu.getRealValue(attr)

	def step(self, value, unit):
		"""This method is called to make a step, you need to adapt it to your model."""
		super(MyNode, self).step(value, unit)  # Keep this line, it triggers the parent class method.
		value *= self.UNIT[unit]  # Keep this line, it converts the step value to seconds

		#self.y = np.random.choice([-1, 0, 1])
		#self.b = self.a + self.y * self.c
		#self.save_attribute("y")		
		new_step=True		
		print('Time',self.tempo)		
		status = self.fmu.doStep(self.tempo-self.step_size, self.step_size, new_step)        
		assert status == fmipp.fmiOK  
		self.tempo=self.tempo+self.step_size


if __name__ == "__main__":
    args = docopt(Node.DOC, version="0.0.1")

    with open(Node.ATTRIBUTE_FILE) as json_data:
        attrs = json.load(json_data)

    with open(Node.INIT_VALUES_FILE) as json_data:
        init_val = json.load(json_data)

    i_map = attrs["to_set"]
    o_list = attrs["to_get"]

    # If you need to load files or data, do it here, and you can pass it to the node contructor.

    node = MyNode(name=args["<name>"], group=args["<group>"], inputs_map=i_map, outputs=o_list, init_values=init_val)

    node.run()
