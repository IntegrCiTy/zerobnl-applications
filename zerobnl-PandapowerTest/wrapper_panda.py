import json

from docopt import docopt
from zerobnl.core import Node

import numpy as np


class MyNode(Node):
    """docstring for MyNode"""

    def __init__(self, name, group, inputs_map, outputs, init_values):  # If needed you can pass more values to your node constructor.
        super(MyNode, self).__init__(name, group, inputs_map, outputs, init_values)  # Keep this line, it triggers the parent class method.


        # This is where you define the attribute of your model, this one is pretty basic.
        self.a = 0
        self.b = 0

        self.y = None

        self.c = None

    def set_attribute(self, attr, value):
        """This method is called to set an attribute of the model to a given value, you need to adapt it to your model."""
        super(MyNode, self).set_attribute(attr, value)  # Keep this line, it triggers the parent class method.

        setattr(self, attr, value)

    def get_attribute(self, attr):
        """This method is called to get the value of an attribute, you need to adapt it to your model."""
        super(MyNode, self).get_attribute(attr)  # Keep this line, it triggers the parent class method.

        return getattr(self, attr)

    def step(self, value, unit):
        """This method is called to make a step, you need to adapt it to your model."""
        super(MyNode, self).step(value, unit)  # Keep this line, it triggers the parent class method.
        value *= self.UNIT[unit]  # Keep this line, it converts the step value to seconds

        self.y = np.random.choice([-1, 0, 1])
        self.b = self.a + self.y * self.c
        self.save_attribute("y")


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
