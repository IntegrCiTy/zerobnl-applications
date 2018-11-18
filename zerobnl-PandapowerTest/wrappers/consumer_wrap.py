import redis
import json

import logging
from docopt import docopt

from obnl.core.client import ClientNode

import numpy as np


# This doc is used by docopt to make the wrapper callable by command line and gather easily all the given parameters
doc = """>>> IntegrCiTy wrapper for power consumer <<<

Usage:
	consumer_wrap.py (<host> <name> <init>) [--i=TO_SET... --o=TO_GET... --first --cmd=CMD]
	consumer_wrap.py -h | --help
	consumer_wrap.py --version

Options
	-h --help   show this
	--version   show version
	--i         parameters to set
	--o         parameters to get
	--first     node in sequence's first group
	--cmd       optional list of commands to run wrapper

"""


class Node(ClientNode):
    """
    Node class for the wrapper (model can be called by the container or can be self contained directly in the wrapper)
    """
    def __init__(self, host, input_attributes=None, output_attributes=None, is_first=False):
        # Implement OBNL client node
        super(Node, self).__init__(host, 'obnl_vhost', 'obnl', 'obnl', 'config_file.json',
                                   input_attributes=input_attributes,
                                   output_attributes=output_attributes,
                                   is_first=is_first)

        self.redis = redis.StrictRedis(host=host, port=6379, db=0)

        # Declare model
        self.loc = 0
        self.scale = 1.0

        self.pf = 0.1

        self.p_kw = 0
        self.q_kvar = 0

        # Set initial values / model parameters
        with open('init_values.json') as json_data:
            init_values = json.load(json_data)

        for key, val in init_values.items():
            setattr(self, key, val)

    def step(self, current_time, time_step):
        """
        Run a step for the wrapper/model

        :param current_time: current simulation time
        :param time_step: next time step to run
        :return: nothing :)
        """
        logging.debug('----- ' + self.name + ' -----')
        logging.debug(self.name, 'time_step', time_step, "s")
        logging.debug(self.name, 'current_time', current_time - time_step)
        logging.debug(self.name, 'inputs', self.input_values)

        # Update input attributes and save input attributes and corresponding simulation time step to Redis DB
        for key, value in self.input_values.items():
            setattr(self, key, value)
            self.redis.rpush('IN||' + self.name + '||' + key, getattr(self, key))
            self.redis.rpush('IN||' + self.name + '||' + key + '||time', current_time)

        # Compute intern state
        logging.debug(self.name, "compute new intern state")
        self.p_kw = round(np.random.normal(self.loc, self.scale), 2)
        self.q_kvar = round(max(0.0, self.p_kw * self.pf), 2)

        # Send updated output attributes
        logging.debug(self.name, "outputs", {key: getattr(self, key) for key in self.output_attributes})
        for key in self.output_attributes:
            self.update_attribute(key, getattr(self, key))

        # Save output attributes and corresponding simulation time step to Redis DB
        for key in self.output_attributes:
            self.redis.rpush('OUT||' + self.name + '||' + key, getattr(self, key))
            self.redis.rpush('OUT||' + self.name + '||' + key + '||time', current_time)


if __name__ == "__main__":
    args = docopt(doc, version='0.0.1')

    node = Node(
        host=args['<host>'],
        is_first=args['--first'],
        input_attributes=args['--i'],
        output_attributes=args['--o']
    )

    node.start()
