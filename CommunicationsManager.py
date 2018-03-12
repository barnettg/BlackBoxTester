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
import time

class CommunicationsManager:
    def __init__(self):
        self.active_port = 0 # default to fist one
        self.available_port_ids = {}  # format "port_id":{ "protocol_class_name": "name", "description": " desc"}
        self.ports_connected = []
        self.log_observers = []
        self.proto_class = None
        self.module = None

    def get_available_ports(self):
        return self.available_port_ids

    def set_active_port(self, prt_id):
        self.active_port = prt_id

    def assign_port(self, prt_id,  protocol_class):  # not completed yet !!!!!!!!!what for????!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        pass

    def unassign_port(self, prt_id):
        if prt_id in self.available_port_ids.keys():
            del self.available_port_ids[prt_id]
        # check if self.active_port should be set to None
        if self.active_port == prt_id:
            self.active_port = 0

    def connect(self, **kwargs):
        # CALL FOR SETUP OF FIRST CONNECTION
        # kwargs
        # 'type' : serial or ethernet
        # 'port_id' : any unused number
        # 'protocol_class_name' : python file name with class name same as file
        # 'IP' : '192.168.1.1'
        # 'networkPort' : '502'
        con_type = None
        port_id = None
        protocol_class_name = None
        protocol_module_name = None
        con_ip = None
        network_port = None
        ret_val = False

        # must have :
        if 'con_type' in kwargs:
            self.notify_log('connect::found con_type')
            con_type = kwargs['con_type']
        if 'port_id' in kwargs:
            self.notify_log('connect::found port_id')
            port_id = kwargs['port_id']
        if 'protocol_class_name' in kwargs:
            self.notify_log('connect::found protocol_class_name')
            protocol_class_name = kwargs['protocol_class_name']
        if 'protocol_module_name' in kwargs:
            self.notify_log('connect::found protocol_module_name')
            protocol_module_name = kwargs['protocol_class_name']

        if protocol_class_name is None:
            return ret_val, "Must specify a protocol class"
        if protocol_module_name is None:
            return ret_val, "Must specify a protocol file"
        if con_type is None:
            return ret_val, "Must specify a communication type of serial or Ethernet"
        if port_id is None:
            return ret_val, "Must specify a port ID"
        if port_id in self.available_port_ids.keys():
            return False, "Port ID is being used"

        if con_type is "serial":
            # 'comport' : comx or /dev/ttyx   depending on system
            # 'baudrate' : '9600'
            # 'parity' : none , odd, even
            # 'stopbits' : 1, 1.5, 2
            if 'comport' in kwargs:
                self.notify_log('connect::found comport')
                com_port = kwargs['comport']
            else:
                return False, "Must specify a COM port"
            # others are optional and have defaults
            # if 'baudrate' in kwargs:
            #     self.notify_log('connect::found baudrate')
            #     com_baudrate = kwargs['baudrate']
            # if 'parity' in kwargs:
            #     self.notify_log('connect::found parity')
            #     com_parity = kwargs['parity']
            # if 'stopbits' in kwargs:
            #     self.notify_log('connect::found stopbits')
            #     com_stopbits = kwargs['stopbits']

            # load class
            # https://www.blog.pythonlibrary.org/2012/07/31/advanced-python-how-to-dynamically-load-modules-or-classes/
            self.proto_class = None
            try:
                self.module = importlib.__import__(protocol_module_name)
                my_class = getattr(self.module, protocol_class_name)
                self.proto_class = my_class(port_id)   #
                self.notify_log(str(self.proto_class))
                self.proto_class.select_port(**kwargs)  # pass the kwargs along
                self.notify_log(str(self.proto_class))
                ret_val = self.proto_class.connect()
                print("ret_val: " + str(ret_val))
            except Exception as e:
                print("Exception !!!!")
                self.notify_log(str(e) + str(sys.exc_info()[0]))

            if self.proto_class is None:
                return False, "could not load protocol class"

            if self.proto_class is None:
                return False, "could not load protocol class"

            if ret_val:
                descrip = str(self.proto_class)
                # save to port ID list
                self.available_port_ids[port_id] = {"protocol_class_name": protocol_class_name,
                                    "instance": self.proto_class,
                                    "description": descrip}
                return True, "connected"

            return False, "Could not connect"

        elif con_type is "ethernet":
            if 'IP' in kwargs:
                self.notify_log('connect::found IP')
                con_ip = kwargs['IP']
            else:
                return False, "Must specify an Ethernet IP"

            if 'networkPort' in kwargs:
                self.notify_log('connect::found networkPort')
                network_port = kwargs['networkPort']
            else:
                return False, "Must specify an Ethernet port"

            # load class
            # https://www.blog.pythonlibrary.org/2012/07/31/advanced-python-how-to-dynamically-load-modules-or-classes/
            self.proto_class = None
            try:
                self.module = importlib.__import__(protocol_module_name)
                my_class = getattr(self.module, protocol_class_name)
                self.proto_class = my_class(port_id)   #
                self.notify_log(str(self.proto_class))
                self.proto_class.select_port(IP=con_ip, networkPort=network_port)
                self.notify_log(str(self.proto_class))
                ret_val = self.proto_class.connect()
            except Exception as e:
                self.notify_log(str(e) + str(sys.exc_info()[0]))

            if self.proto_class is None:
                return False, "could not load protocol class"

            if ret_val:
                descrip = str(self.proto_class)
                # save to port ID list
                self.available_port_ids[port_id] = {"protocol_class_name": protocol_class_name,
                                                    "instance": self.proto_class,
                                                    "description": descrip}
                return True, "connected"

            return False, "Could not connect"

        else:
            return False, "type {} is incorrect".format(type)

    def register_log(self, observ):
        self.log_observers.append(observ)

    def unsubscribe_log(self, observ):
        if observ in self.log_observers:
            self.log_observers.remove(observ)

    def notify_log(self, data):
        for item in self.log_observers:
            item("CommunicationsManager::" + data)

    def reconnect(self, prt_id=None):  # not completed yet !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ret_val = False
        if prt_id is None:  # default to active port
            port_id = self.active_port

        # try to reconnect

        return ret_val

    def send(self, data, port_id=None):  # not completed yet !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # send data and wait for response
        pid = port_id

        if port_id is None:  # use default port
            pid = self.active_port

        if pid in self.available_port_ids.keys():
            response = self.available_port_ids[pid]["instance"].send_data(data)
            return response
        else:
            return "Error, port ID {} not available".format(pid)

    def send_async(self, data, port_id=None):
        # send data but don't wait for response
        pid = port_id

        if port_id is None:  # use default port
            pid = self.active_port

        if pid in self.available_port_ids.keys():
            self.available_port_ids[pid]["instance"].send_data_async()
        else:
            return "Error, port ID {} not available".format(pid)

    def is_async_data_ready(self, port_id=None):  # not completed yet !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        pass

    def get_async_data(self, port_id=None):  # not completed yet !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        pass

    def set_using_port(self, port_id):  # another function name to set the active port
        self.set_active_port(port_id)

    def get_status(self, pid): # !!!!!!!!!!!!!!!!! need to include for ethernet
        if pid in self.available_port_ids.keys():
            return self.available_port_ids[pid]["instance"].get_status()
        else:
            return "Status Error, port ID {} not available".format(pid)

#    def get_available_ports(self, pid): # !!!!!!!!!!!!!!!!! need to include for ethernet
#        if pid in self.available_port_ids.keys():
#            return self.available_port_ids[pid]["instance"].get_available_ports()
#        else:
#            return "get_available_ports Error, port ID {} not available".format(pid)

    def get_portid_instance(self, pid):
        if pid in self.available_port_ids.keys():
            return self.available_port_ids[pid]["instance"]
        else:
            return None

if __name__ == "__main__":
    def print_log(message):
        print(message)

    cm = CommunicationsManager()
    cm.register_log(print_log)

    if True:
        result, mess = cm.connect(con_type="ethernet",
                                  port_id=0, protocol_class_name="NetworkNoProtocol",
                                  protocol_module_name="NetworkNoProtocol",
                                  IP="192.168.1.4", networkPort=23)  # IP="127.0.0.1", networkPort=23)
        print("result: {}, with message: {}".format(result, mess))
    else:
        result, mess = cm.connect(con_type="serial",
                                  port_id=0, protocol_class_name="SerialNoProtocol",
                                  protocol_module_name="SerialNoProtocol",
                                  comport="COM1", baudrate=57600)
        print("result: {}, with message: {}".format(result, mess))
        pid_instance = cm.get_portid_instance(0)
        print(cm.get_status(0))
        print(pid_instance.get_available_ports())

    pid_instance = cm.get_portid_instance(0)
    pid_instance.ending = "\n" # "\n" for raspberry pi TrafficLights.py using os.linesep instead of "\r\n"
    print("?state1: " + cm.send("?state", 0))
    print("CHANGE1: " + cm.send("CHANGE", 0))
    print("?state2: " + cm.send("?state", 0))
    print("CHANGE2: " + cm.send("CHANGE", 0))
    print("?state3: " + cm.send("?state", 0))
    print("CHANGE3: " + cm.send("CHANGE", 0))
    print("?state4: " + cm.send("?state", 0))
    print("CHANGE4: " + cm.send("CHANGE", 0))
    print("?state5: " + cm.send("?state", 0))
    print("CHANGE5: " + cm.send("CHANGE", 0))
    print("Expect error with this command ->menu: " + cm.send("menu", 0))
    pid_instance.set_data_wait_ms(4000) # need more time for menu command
    time1 = time.clock()
    val = cm.send("?menu", 0)
    time2 = time.clock()
    print("time1: {}".format(time1))
    print("time2: {}".format(time2))
    val.replace('\b', "\r\n")
    print("val: " + val)
    #print("?menu: " + val)
    print("?state6: " + cm.send("?state", 0))
    print("CHANGE6: " + cm.send("CHANGE", 0))

    print("disconnect ------------------")
    pid_instance.disconnect()
    print("stop_Thread ------------------")
    pid_instance.stop_Thread()

    print("Done ------------------")


