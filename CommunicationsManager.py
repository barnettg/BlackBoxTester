# CommunicationsManager.py
# - configure and control ports
# -- select port and assign port_id
# -- read and write port data

import importlib
import sys
import time


class CommunicationsManager:
    """
    Configure and control communication ports

    Methods available to scripts via helper class:
        reconnect(port_id:int)
        send(data:str, port_id:int)
        is_async_data_ready(port_id:int)
        get_async_data(port_id:int)
        set_using_port(port_id:int)
    """
    def __init__(self):
        """Example of docstring on the __init__ method.

        Attributes:
            available_port_ids  (dict) : dictionary keys of the port numeric IDs(i.e. 0, 1, etc.)
                                                The value is another dictionary containing:
                                                "protocol_class_name": "name"
                                                "description": " desc"
                                                "instance": the instance of the protocol class used for this ID

            active_port (int) : the port that will be used for default communications when the ID is not specified
                                example: send(data)  will use the default active port

            log_observers (list) : list of methods to be called for logging

        """
        self.active_port = 0  # default to fist one
        self.available_port_ids = {}  #
        # self.ports_connected = []
        self.log_observers = []
        self.proto_class = None  # don't need to be class attribute?
        self.module = None  # don't need to be class attribute?

    def get_available_ports(self) -> dict:
        """
        returns the available ports dictionary
        """
        return self.available_port_ids

    def set_active_port(self, prt_id: int):
        """
        Set the default port to use (one of the available ports in the available_port_ids dictionary

        Args:
            prt_id (int): This is the first param.

        Returns:
            None

        """
        self.active_port = prt_id

    def assign_port(self, prt_id: int,
                    protocol_module_name: str,
                    protocol_class_name: str) -> bool:  #
        """
        Add an ID to the available_port_ids dictionary

        Args:
            prt_id (int): Port dictionary key
            protocol_module_name (str): relative path and name of file containing the class to use
            protocol_class (str): Protocol class name

        Returns:
            (bool) True if added, False if ID already exists
        """
        if prt_id in self.available_port_ids.keys():
            return False

        try:
            module = importlib.__import__(protocol_module_name)
            my_class = getattr(module, protocol_class_name)
            proto_class = my_class(prt_id)   #
            self.notify_log(str(self.proto_class))
            descrip = str(self.proto_class)
            # save to port ID list
            self.available_port_ids[prt_id] = {
                "protocol_class_name": protocol_class_name,
                "instance": proto_class,
                "description": descrip}

        except Exception as e:
            print("assign_port Exception !!!!")
            self.notify_log(str(e) + str(sys.exc_info()[0]))

        return True

    def unassign_port(self, prt_id: int) -> bool:
        """
        Removes a port from the available_port_ids dictionary

        Args:
            prt_id (int): Port dictionary key

        Returns:
            (bool) Returns True if ID in dictionary

        """
        if prt_id in self.available_port_ids.keys():
            self.closedown_port(prt_id)
            del self.available_port_ids[prt_id]
            # check if self.active_port should be set to None
            if self.active_port == prt_id:
                self.active_port = 0
            return True
        return False

    def disconnect(self, port_id: int=None) ->str:
        """
        Calls the disconnect method of the protocol class

        Args:
           prt_id (int): Port dictionary key

        Returns:
            A message string from the disconnect method of the protocol class used

        """
        pid = port_id

        if port_id is None:  # use default port
            pid = self.active_port

        if pid in self.available_port_ids.keys():
            response = self.available_port_ids[pid]["instance"].disconnect()
            return response
        else:
            return "Error, port ID {} not available".format(pid)

    def disconnect_all(self):
        for item in self.available_port_ids.keys():
            self.disconnect(item)

    def connect(self, **kwargs)->(bool, str):
        """
        Loads protocol class and applies connection protocol over the specified communications type

        Args:
            **kwargs:
            'type' : serial or ethernet
            'port_id' : any unused number
            'protocol_module_name ' : python file containing class of protocol to use, includes relative path to project
            'protocol_class_name': name of class in file
            'IP' : '192.168.1.1'
            'networkPort' : '502'
            'comport' : comx or /dev/ttyx   depending on system
            'baudrate' : '9600'
            'parity' : none , odd, even
            'stopbits' : 1, 1.5, 2

        Returns:
            True or false with a additional string message

        """
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
                self.available_port_ids[port_id] = {
                    "protocol_class_name": protocol_class_name,
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
        """
        Register a method to be sent logging information string

        Args:
            param1: method with string argument

        Returns:
            None
        """
        self.log_observers.append(observ)

    def unsubscribe_log(self, observ):
        """
        Remove a method from receiving logging information string

        Args:
            param1:  method with string argument

        Returns:
            None

        """
        if observ in self.log_observers:
            self.log_observers.remove(observ)

    def notify_log(self, data: str):
        """
        Calls registered methods and passes message string

        Args:
            param1: Data string to log

        Returns:
            None
        """
        for item in self.log_observers:
            item("CommunicationsManager::" + data)

    def reconnect(self, prt_id: int=None)-> bool:
        """
        Helper class calls this method to use the reconnect in the protocol class to
        initiate a reconnect in case connection is lost

        Args:
            param1: Port ID to use to connect to- if not specified then the active ID is used

        Returns:
            True if connects
        """
        if prt_id is None:  # default to active port
            prt_id = self.active_port

        # try to reconnect
        if prt_id in self.available_port_ids.keys():
            response = self.available_port_ids[prt_id]["instance"].reconnect()
            return response
        else:
            return False

    def send(self, data, port_id=None)-> str:  #
        """
        Helper class calls this method to send data through the protocol class

        Args:
            param1: Port ID to send data to
            param2: Port ID to send data to- if not specified then the active ID is used

        Returns:
            String message from the protocol

        """
        # send data and wait for response
        pid = port_id

        if port_id is None:  # use default port
            pid = self.active_port

        if pid in self.available_port_ids.keys():
            response = self.available_port_ids[pid]["instance"].send_data(data)
            return response
        else:
            return "Error, port ID {} not available".format(pid)

    def send_async(self, data: str, port_id: int=None) -> str:  # called from script (helper class)
        """
        Helper class calls this method to send data through the protocol class that does not expect data returned
         protocol may not necessarily use this

        Args:
            param1: Port ID to send data to
            param2: Port ID to send data to- if not specified then the active ID is used

        Returns:
            String message of OK or Error

        """
        # send data but don't wait for response
        pid = port_id

        if port_id is None:  # use default port
            pid = self.active_port

        if pid in self.available_port_ids.keys():
            self.available_port_ids[pid]["instance"].send_data_async(data)
            return "OK"
        else:
            return "Error, port ID {} not available".format(pid)

    def is_async_data_ready(self, port_id: int=None):  # called from script (helper class)
        """
        Helper class calls this method to check for available asynchronous data - protocol may not necessarily use this

        Args:
            port_id (int): Port dictionary key - if not specified then the active ID is used

        Returns:
            True if data is available
        """
        raise ValueError('not done!')
        pass

    def get_async_data(self, port_id=None) -> str:  # called from script (helper class)
        """
        Helper class calls this method to get all available communications data - protocol may not necessarily use this

        Args:
            port_id (int): Port dictionary key - if not specified then the active ID is used

        Returns:
            (str) Get all available communications data
        """
        raise ValueError('not done!')
        pass

    def set_using_port(self, port_id: int):  # called from script (helper class)
        """
        Set the (default)port the script is using

        Args:
            port_id (int): Port dictionary key
        """
        self.set_active_port(port_id)

    def get_status(self, pid: int)-> str:
        """
        calls the status method of the port ID class instance.

        Args:
            pid (int): Port dictionary key
        Returns:
            (str) result of class instance Status method

        """
        if pid in self.available_port_ids.keys():
            return self.available_port_ids[pid]["instance"].get_status()
        else:
            return "Status Error, port ID {} not available".format(pid)

    def get_portid_instance(self, pid: int):
        """
        Get the instance for the specified port ID

        Args:
            pid (int): Port dictionary key

        Returns:
            Returns the class instance of the port ID or None if not available.
        """
        if pid in self.available_port_ids.keys():
            return self.available_port_ids[pid]["instance"]
        else:
            return None

    def get_available_serial_ports(self):
        """
        Get a list of the availble system serial ports

        Returns:
            (list) A list of system serial port names (example "COM1").
        """
        # return com port available
        import serial.tools.list_ports
        avail_list = []
        # print (dir(serial.tools.list_ports.comports()))
        for port in serial.tools.list_ports.comports():
            # print(dir(port))
            # print(str(port.device))
            avail_list.append(port.device)
        return avail_list

    def closedown_port(self, port_id: int) -> bool:
        """
        Close the com port and stop threads

        Args:
            port_id (int): Port dictionary key
        """
        if port_id in self.available_port_ids.keys():
            self.available_port_ids[port_id]["instance"].disconnect()
            self.available_port_ids[port_id]["instance"].stop_Thread()
            return True
        return False

    def set_data_wait_ms(self, port_id: int, ms: int) -> bool:  #
        """
        Set the time to wait for a response in ms after sending data.

        Args:
            port_id (int): Port dictionary key
            ms (int) : The milliseconds.

        Returns:
            True if ID exists
        """
        if port_id in self.available_port_ids.keys():
            self.available_port_ids[port_id]["instance"].set_data_wait_ms(ms)
            return True
        return False

if __name__ == "__main__":
    def print_log(message):
        print(message)

    cm = CommunicationsManager()
    cm.register_log(print_log)
    print("available serial ports: " + str(cm.get_available_serial_ports()))

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
    pid_instance.ending = "\n"  # "\n" for raspberry pi TrafficLights.py using os.linesep instead of "\r\n"
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
    pid_instance.set_data_wait_ms(4000)  # need more time for menu command
    time1 = time.clock()
    val = cm.send("?menu", 0)
    time2 = time.clock()
    print("time1: {}".format(time1))
    print("time2: {}".format(time2))
    val.replace('\b', "\r\n")
    print("val: " + val)
    # print("?menu: " + val)
    print("?state6: " + cm.send("?state", 0))
    print("CHANGE6: " + cm.send("CHANGE", 0))

    print("disconnect ------------------")
    pid_instance.disconnect()
    print("stop_Thread ------------------")
    pid_instance.stop_Thread()

    print("Done ------------------")
