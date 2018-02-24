# CommunicationsManager.py
# - configure and control ports
# -- select port and assign part_id
# -- read and write port data

# called from helper class:
# reconnect(port_id)
# send(port_id,data)
# is_async_data_ready(port_id)
# get_async_data(port_id)
# set_using_port(string port_id)

import importlib
import sys

class CommunicationsManager:
    def __init__(self):
        self.active_port = None
        self.available_port_ids = {}  # format "port_id":{ "protocol_class_name": "name", "description": " desc"}
        self.ports_connected = []
        self.log_observers = []
        self.proto_class = None

    def get_available_ports(self):
        return self.available_port_ids

    def set_active_port(self, prt_id):
        self.active_port = prt_id

    def assign_port(self, prt_id,  protocol_class):
        pass

    def unassign_port(self, prt_id):
        pass
        # check if self.active_port should be set to None

    def connect(self,**kwargs):  # not completed yet
        # CALL FOR SETUP OF FIRST CONNECTION
        # kwargs
        # 'type' : serial or ethernet
        # 'port_id' : any unused number
        # 'protocol_class_name' : python file name with class name same as file
        # 'IP' : '192.168.1.1'
        # 'networkPort' : '502'
        type = None
        port_id = None
        protocol_class_name = None
        protocol_module_name = None
        IP = None
        networkPort = None
        ret_val = False

        if 'type' in kwargs:
            self.notify_log('connect::found type')
            type = kwargs['type']
        if 'port_id' in kwargs:
            self.notify_log('connect::found port_id')
            port_id = kwargs['port_id']
        if 'protocol_class_name' in kwargs:
            self.notify_log('connect::found IP')
            protocol_class_name = kwargs['protocol_class_name']
        if 'protocol_module_name' in kwargs:
            self.notify_log('connect::found IP')
            protocol_module_name = kwargs['protocol_class_name']

        if port_id is None:
            return ret_val, "Must specify a port ID"
        if protocol_class_name is None:
            return ret_val, "Must specify a protocol class"
        if protocol_module_name is None:
            return ret_val, "Must specify a protocol class"



        if type is "serial":
            return ret_val, "Serial protocol not completed"
        elif type is "ethernet":
            if 'IP' in kwargs:
                self.notify_log('connect::found IP')
                IP = kwargs['IP']
            if 'networkPort' in kwargs:
                self.notify_log('connect::found networkPort')
                networkPort = kwargs['networkPort']
        else:
            return False, "type {} is incorrect".format(type)

        # ethernet --- have to divide into serial and ethernet !!!!!!!!!!!!!!!!
        # load class
        # https://www.blog.pythonlibrary.org/2012/07/31/advanced-python-how-to-dynamically-load-modules-or-classes/
        self.proto_class = None
        try:
            self.module = importlib.__import__(protocol_module_name)
            my_class = getattr(self.module, protocol_class_name)
            self.proto_class = my_class(port_id)   # !! only if in same directory --
                                            # have to split class name if there is a path
            self.notify_log(str(self.proto_class))
            self.proto_class.select_port(IP=IP, networkPort=networkPort)
            self.notify_log(str(self.proto_class))
            ret_val = self.proto_class.connect()
        except Exception as e:
            self.notify_log( str(e) + str(sys.exc_info()[0]))

        if self.proto_class is None:
            return False, "could not load protocol class"

        # try to connect
        if ret_val:
            return True, "connected"
        return False, "Could not connect"

    def register_log(self, observ):
        self.log_observers.append(observ)

    def unsubscribe_log(self, observ):
        if observ in self.log_observers:
            self.log_observers.remove(observ)

    def notify_log(self, data):
        for item in self.log_observers:
            item("CommunicationsManager::" + data)

    def reconnect(self, port_id=None):  # not completed yet
        if port_id is None and self.active_port is None:
            raise ValueError('When trying to reconnect, a port is not specified')

        ret_val = False
        if port_id is None:  # default to active port
            port_id = self.active_port

        # try to reconnect

        return ret_val

    def send(self, data, port_id=None):
        if port_id is None and self.active_port is None:
            raise ValueError('When trying to send data, a port is not specified')

    def is_async_data_ready(self, port_id=None):
        if port_id is None and self.active_port is None:
            raise ValueError('When checking for available asynchronous data, a port is not specified')

    def get_async_data(self, port_id=None):
        if port_id is None and self.active_port is None:
            raise ValueError('When trying to get asynchronous data, a port is not specified')

    def set_using_port(self, port_id):
        pass


if __name__ == "__main__":
    def print_log(message):
        print(message)

    cm = CommunicationsManager()
    cm.register_log(print_log)
    result, mess = cm.connect(type = "ethernet",
                              port_id=0, protocol_class_name="NetworkNoProtocol",
                              protocol_module_name="NetworkNoProtocol",
                              IP="127.0.0.1", networkPort=23)
    print("result: {}, with message: {}".format(result, mess))