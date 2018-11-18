import redis
import json

import logging
from docopt import docopt

from obnl.core.client import ClientNode

import pandapower as pp
import pandas as pd

# This doc is used by docopt to make the wrapper callable by command line and gather easily all the given parameters
doc = """>>> IntegrCiTy wrapper for pandapower power grid model <<<

Usage:
	power_grid_wrap.py (<host> <name> <init>) [--i=TO_SET... --o=TO_GET... --first --cmd=CMD]
	power_grid_wrap.py -h | --help
	power_grid_wrap.py --version

Options
	-h --help   show this
	--version   show version
	--i         parameters to set
	--o         parameters to get
	--first     node in sequence's first group
	--cmd       optional list of commands to run wrapper

"""


def set_value(net, table, name, col, value):
    df = getattr(net, table)
    df.loc[df.name == name, col] = value


def get_res_value(net, table, name, res_col):
    obj = pp.get_element_index(net, table, name)
    df = getattr(net, "res_"+table)
    return df.loc[obj, res_col]


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

        # Declare and implement model
        self.net = pp.create_empty_network()

        for i in ["bus", "bus_geodata", "line", "switch", "trafo", "ext_grid", "load"]:
            df = pd.DataFrame(json.load(open('{}.json'.format(i))))
            df.index = map(int, df.index)
            setattr(self.net, i, df)

        # Set initial values / model parameters (only loads can be set as initial values)
        with open('init_values.json') as json_data:
            init_values = json.load(json_data)

        print(".oO-", self.name, ": read init_values.json")

        for key, val in init_values.items():
            set_value(self.net, "load", key, "p_kw", val[0])
            set_value(self.net, "load", key, "q_var", val[1])

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
            a = key.split("_")
            set_value(self.net, "load", a[0], a[1]+"_"+a[2], value)
            self.redis.rpush('IN||' + self.name + '||' + key, value)
            self.redis.rpush('IN||' + self.name + '||' + key + '||time', current_time)

        # Compute internal state
        # logging.debug(self.name, "compute new intern state")
        pp.runpp(self.net)

        # Save chosen internal state and corresponding simulation time step to Redis DB
        for key in ["Feeder_p_kw", "Feeder_q_kvar"]:
            a = key.split("_")
            val = get_res_value(self.net, "ext_grid", a[0], a[1] + "_" + a[2])
            self.redis.rpush('X||' + self.name + '||' + key, val)
            self.redis.rpush('X||' + self.name + '||' + key + '||time', current_time)

        # Send updated output attributes
        o_attr = {}
        for key in self.output_attributes:
            a = key.split("_")
            o_attr[key] = get_res_value(self.net, "ext_grid", a[0], a[1]+"_"+a[2])

        # logging.debug(self.name, "outputs", o_attr)
        for key in self.output_attributes:
            self.update_attribute(key, o_attr[key])

        # Save output attributes and corresponding simulation time step to Redis DB
        for key in self.output_attributes:
            self.redis.rpush('OUT||' + self.name + '||' + key, o_attr[key])
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