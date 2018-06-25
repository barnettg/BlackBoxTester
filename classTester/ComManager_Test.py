# test for the CommunicationsManager.py class
import sys
sys.path.append('..')
import CommunicationsManager


if __name__ == "__main__":
    def print_log(message):
        print(message)

    cm = CommunicationsManager.CommunicationsManager()
    cm.register_log(print_log)
    print("available serial ports: " + str(cm.get_available_serial_ports()))
    #print(dir(cm))
    # methods to test: ['__doc__', '__repr__','__str__', 'active_port', 'assign_port', 'available_port_ids', 'connect',
    #  'disconnect', 'disconnect_all', 'get_async_data', 'get_available_ports', 'get_available_serial_ports',
    # 'get_portid_instance', 'get_status', 'is_async_data_ready', 'log_observers', 'module', 'notify_log',
    # 'proto_class', 'reconnect', 'register_log', 'send', 'send_async', 'set_active_port', 'set_using_port',
    # 'unassign_port', 'unsubscribe_log']
    print(help(cm.get_available_serial_ports))

    resp = input("Enter: select (S)erial or (E)thernet: ")

    if resp == "S" or resp == "s" :
        ser_avail_list = cm.get_available_serial_ports()
        com_string_0 = ser_avail_list[0]
        com_string_1 = ser_avail_list[1]
        resp = input("Open TrafficLights.py to test on " + com_string_0 + "  at 57600 baud")
        result, mess = cm.connect(con_type="serial",
                                   port_id=0, protocol_class_name="SerialNoProtocol",
                                   protocol_module_name="SerialNoProtocol",
                                   comport=com_string_1, baudrate=57600)
        print("result: {}, with message: {}".format(result, mess))
        pid_instance = cm.get_portid_instance(0)
        print(cm.get_status(0))
        print(pid_instance.get_available_ports())


    elif resp == "E" or resp == "e" :
        resp = input("Open TrafficLights.py ethernet to test on 127.0.0.1")
        result, mess = cm.connect(con_type="ethernet",
                                   port_id=0, protocol_class_name="NetworkNoProtocol",
                                   protocol_module_name="NetworkNoProtocol",
                                   IP="127.0.0.1", networkPort=23)  # IP="127.0.0.1", networkPort=23)
        print("result: {}, with message: {}".format(result, mess))


    #
    # pid_instance = cm.get_portid_instance(0)
    # pid_instance.ending = "\n" # "\n" for raspberry pi TrafficLights.py using os.linesep instead of "\r\n"
    # print("?state1: " + cm.send("?state", 0))
    # print("CHANGE1: " + cm.send("CHANGE", 0))
    # print("?state2: " + cm.send("?state", 0))
    # print("CHANGE2: " + cm.send("CHANGE", 0))
    # print("?state3: " + cm.send("?state", 0))
    # print("CHANGE3: " + cm.send("CHANGE", 0))
    # print("?state4: " + cm.send("?state", 0))
    # print("CHANGE4: " + cm.send("CHANGE", 0))
    # print("?state5: " + cm.send("?state", 0))
    # print("CHANGE5: " + cm.send("CHANGE", 0))
    # print("Expect error with this command ->menu: " + cm.send("menu", 0))
    # pid_instance.set_data_wait_ms(4000) # need more time for menu command
    # time1 = time.clock()
    # val = cm.send("?menu", 0)
    # time2 = time.clock()
    # print("time1: {}".format(time1))
    # print("time2: {}".format(time2))
    # val.replace('\b', "\r\n")
    # print("val: " + val)
    # #print("?menu: " + val)
    # print("?state6: " + cm.send("?state", 0))
    # print("CHANGE6: " + cm.send("CHANGE", 0))
    #
    # print("disconnect ------------------")
    # pid_instance.disconnect()
    # print("stop_Thread ------------------")
    # pid_instance.stop_Thread()

    print("Done ------------------")