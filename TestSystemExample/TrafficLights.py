# This is a traffic light simulation
# There is a traffic light for north to south traffic and
# a traffic light for east to west traffic
# there are car sensor at appropriate points in the road to detect waiting cars
# There is a train sensor  for a train that crosses N to S traffic
# E to W traffic takes priority
# operation changes depending on the time of day
# a state machine keeps track of the system state
# the system can communicate by serial or network


# this is to be used as a sample system for evaluating the black box tester
#

# states
# NsGreenEwRedState
# NsYellowEwRedState
# NsRedEwRedToEwGreenState
# NsRedEwGreenState
# NsRedEwYellowState
# NsRedEwRedToNsGreenState
# NsRedFlashEwRedFlashState

#operations
# car sensor NS                     a car is waiting on the North-South path
# car sensor EW                     a car is waiting on the East-West path
# train                             a train is in the area
# lights_operating_error            there is an error go to flashing red
# change light                      go to the next state in the sequence

#
# Commands:
# ?readstate  -> returns the state
# traincoming
# traingone
# carwaitingNS
# carwaitingEW
# seterror
# clearerror
# change


import socket
import threading
import select
import sys
import os
import serial
import time

class IState(object):
    
    """Interface for state"""
    def change( self ):
        raise NotImplementedError( "Must Implement change method" )
    def train( self ):
        raise NotImplementedError( "Must Implement train method" )
    def car_at_NS (self ):
        raise NotImplementedError( "Must Implement car at North-South method" )
    def car_at_EW( self ):
        raise NotImplementedError( "Must Implement car at East-West method" )
    def lights_operating_error( self ):
        raise NotImplementedError( "Must Implement lights_error method" )
    def lights_operating_error_resolved( self ):
        raise NotImplementedError( "Must Implement lights_error method" )
    
class NsGreenEwRedState(IState):
    def __init__(self, trafic_machine):
        self.trafic_machine = trafic_machine
        self.name = "NS Green and EW Red State"
        
    def change( self ):
        if self.trafic_machine.light_error:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_Flash_EW_red_Flash_state() )
            return
        if self.trafic_machine.train_coming:
            self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() )
            return
        if self.trafic_machine.carwaitingEW:
            self.trafic_machine.setState(self.trafic_machine.get_NS_yellow_EW_red_state() )
            return
        if self.trafic_machine.carwaitingNS:
            self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() )
            return
        self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() ) # stay in NS priority if no sensors active
    
class NsYellowEwRedState(IState):
    def __init__(self, trafic_machine):
        self.trafic_machine = trafic_machine
        self.name = "NS Yellow and EW Red State"
        
    def change( self ):
        if self.trafic_machine.light_error:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_Flash_EW_red_Flash_state() )
            return
        if self.trafic_machine.train_coming:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_EW_green_state() )
            return
        if self.trafic_machine.carwaitingEW:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_EW_green_state() )
            return
        if self.trafic_machine.carwaitingNS:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_EW_green_state() )
            return
        self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_EW_green_state() ) #
    

class NsRedEwRedToEwGreenState(IState):
    def __init__(self, trafic_machine):
        self.trafic_machine = trafic_machine
        self.name = "NS Red and EW Red To EW Green State"
        
    def change( self ):
        if self.trafic_machine.light_error:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_Flash_EW_red_Flash_state() )
            return
        if self.trafic_machine.train_coming:
            self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() )
            return
        if self.trafic_machine.carwaitingEW:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_green_state() )
            return
        if self.trafic_machine.carwaitingNS:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_green_state() )
            return
        self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_green_state() ) #

class NsRedEwGreenState(IState):
    def __init__(self, trafic_machine):
        self.trafic_machine = trafic_machine
        self.name = "NS Red and EW Green State"
        
    def change( self ):
        if self.trafic_machine.light_error:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_Flash_EW_red_Flash_state() )
            return
        if self.trafic_machine.train_coming:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_yellow_state() )
            return
        if self.trafic_machine.carwaitingEW:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_yellow_state() )
            return
        if self.trafic_machine.carwaitingNS:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_yellow_state() )
            return
        self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_yellow_state() ) #

class NsRedEwYellowState(IState):
    def __init__(self, trafic_machine):
        self.trafic_machine = trafic_machine
        self.name = "NS Red and EW Yellow State"
        
    def change( self ):
        if self.trafic_machine.light_error:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_Flash_EW_red_Flash_state() )
            return
        if self.trafic_machine.train_coming:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() )
            return
        if self.trafic_machine.carwaitingEW:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() )
            return
        if self.trafic_machine.carwaitingNS:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() )
            return
        self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() ) #

class NsRedEwRedToNsGreenState(IState):
    def __init__(self, trafic_machine):
        self.trafic_machine = trafic_machine
        self.name = "NS Red EW Red To NS Green State"
        
    def change( self ):
        if self.trafic_machine.light_error:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_Flash_EW_red_Flash_state() )
            return
        if self.trafic_machine.train_coming:
            self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() )
            return
        if self.trafic_machine.carwaitingEW:
            self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() )
            return
        if self.trafic_machine.carwaitingNS:
            self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() )
            return
        self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() ) #

class NsRedFlashEwRedFlashState(IState):
    def __init__(self, trafic_machine):
        self.trafic_machine = trafic_machine
        self.name = "NS Red Flash and EW Red Flash State"
        
    def change( self ):
        if self.trafic_machine.light_error:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_Flash_EW_red_Flash_state() )
            return
        if self.trafic_machine.train_coming:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() )
            return
        if self.trafic_machine.carwaitingEW:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() )
            return
        if self.trafic_machine.carwaitingNS:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() )
            return
        self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() ) #  

#-------------------------------------

class TrafficMachine():
    def __init__(self):
        self.light_error = False
        self.train_coming = False
        self.carwaitingEW = False
        self.carwaitingNS = False

            
        self.NS_green_EW_red_state = NsGreenEwRedState(self)
        self.NS_yellow_EW_red_state = NsYellowEwRedState(self)
        self.NS_red_EW_red_to_EW_green_state = NsRedEwRedToEwGreenState(self)
        self.NS_red_EW_green_state = NsRedEwGreenState(self)
        self.NS_red_EW_yellow_state = NsRedEwYellowState(self)
        self.NS_red_EW_red_to_NS_green_state = NsRedEwRedToNsGreenState(self)
        self.NS_red_Flash_EW_red_Flash_state = NsRedFlashEwRedFlashState(self)
        
        # initial state
        self.state = self.NS_red_Flash_EW_red_Flash_state

    def setState(self, newState):
        self.state = newState
        #print(self.state.name)
        
    def change(self):
        self.state.change()

    def get_NS_green_EW_red_state(self):
        return self.NS_green_EW_red_state

    def get_NS_yellow_EW_red_state(self):
        return self.NS_yellow_EW_red_state

    def get_NS_red_EW_red_to_EW_green_state(self):
        return self.NS_red_EW_red_to_EW_green_state

    def get_NS_red_EW_green_state(self):
        return self.NS_red_EW_green_state

    def get_NS_red_EW_yellow_state(self):
        return self.NS_red_EW_yellow_state

    def get_NS_red_EW_red_to_NS_green_state(self):
        return self.NS_red_EW_red_to_NS_green_state

    def get_NS_red_Flash_EW_red_Flash_state(self):
        return self.NS_red_Flash_EW_red_Flash_state

    
class TrafficServer:
    # send cntrl-c to exit
    def __init__(self):
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 23 #80  # 23 telnet,502 modbus
        self.BUFFER_SIZE = 20  # Normally 1024, but we want fast response

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', self.TCP_PORT))
        self.s.listen(5)
        self.s.settimeout(0.2)
        self.count = 0
        self.keep_going = True
        self.conn = None
        self.addr = None
        self.trafficMachine = TrafficMachine()
        print("ServerClass : " + self.trafficMachine.state.name)


    def connect_thread(self, conn):
        print('Connection address:', self.addr)
        accumulated_data = ""
        while 1:
            try:
                conn.setblocking(0)
                ready = select.select([conn], [], [], 1)

                if ready[0]:
                    data = conn.recv(self.BUFFER_SIZE)
                    if not data:
                        break
                    print(threading.currentThread().getName() + " received data:", data)
                    if data == b'\x03': # cntrl-c
                        self.keep_going = False
                        print("exit " + threading.currentThread().getName())
                        break
                    # conn.send(data)  # echo
                    decoded_data = data.decode()
                    accumulated_data += decoded_data
                    # print("accumulated_data: " + accumulated_data)
                    if "\n" in decoded_data:
                        # print("found return ")
                        self.decode_data(str(accumulated_data))
                        accumulated_data = ""
                if not self.keep_going:
                    break
            except:
                print("exception "+ threading.currentThread().getName())
                print("read_thread Unexpected error:", sys.exc_info()[0])
                error_type, error_message, error_traceback = sys.exc_info()
                print(error_message)
                print(error_traceback)
                conn.close()
                break

        conn.close()

    def start_server(self):
        threading.Thread(target = self.start,name="Server").start()

    def start(self):
        while True:
            if not self.keep_going:
                break
            try:
                self.conn, self.addr = self.s.accept()
                self.count += 1
                thread_name = "thread"+str(self.count)
                threading.Thread(target = self.connect_thread,name=thread_name, args=(self.conn,)).start()
            except socket.timeout:
                pass
            except:
                pass

    def decode_data(self, data):
        line_ending = os.linesep
        stripped_data = data.upper().strip()
        print("rec " + stripped_data)
        if stripped_data == "CHANGE":
            print("traffic change ")
            self.trafficMachine.change()
            print("send back OK ")
            self.conn.send(b'OK' + line_ending.encode('utf-8'))
        elif stripped_data == "?STATE":
            print("traffic state ")
            state = self.trafficMachine.state.name
            print("send back " + state)
            self.conn.send(state.encode('utf-8') + line_ending.encode('utf-8'))
        elif stripped_data == "CAREW=1":
            self.trafficMachine.carwaitingEW = True
            self.conn.send(b'OK' + line_ending.encode('utf-8'))
        elif stripped_data == "CAREW=0":
            self.trafficMachine.carwaitingEW = False
            self.conn.send(b'OK' + line_ending.encode('utf-8'))

        elif stripped_data == "CARNS=1":
            self.trafficMachine.carwaitingNS = True
            self.conn.send(b'OK' + line_ending.encode('utf-8'))
        elif stripped_data == "CARNS=0":
            self.trafficMachine.carwaitingNS = False
            self.conn.send(b'OK' + line_ending.encode('utf-8'))

        elif stripped_data == "TRAIN=1":
            self.trafficMachine.train_coming = True
            self.conn.send(b'OK' + line_ending.encode('utf-8'))
        elif stripped_data == "TRAIN=0":
            self.trafficMachine.train_coming = False
            self.conn.send(b'OK' + line_ending.encode('utf-8'))

        elif stripped_data == "ERR=1":
            self.trafficMachine.light_error = True
            self.conn.send(b'OK' + line_ending.encode('utf-8'))
        elif stripped_data == "ERR=0":
            self.trafficMachine.light_error = False
            self.conn.send(b'OK' + line_ending.encode('utf-8'))

        elif stripped_data == "?MENU":
            out = ""
            out += "CAREW=0\t\tCar NOT waiting at EW intersection." + line_ending
            out += "CAREW=1\t\tCar waiting at EW intersection." + line_ending
            out += "CARNS=0\t\tCar NOT waiting at EW intersection." + line_ending
            out += "CARNS=1\t\tCar waiting at NS intersection." + line_ending
            out += "CHANGE\t\tInitiate a state change." + line_ending
            out += "ERR=0\t\tNo system error." + line_ending
            out += "ERR=1\t\tSystem error." + line_ending
            out += "?STATE\t\tRead the traffic state." + line_ending
            out += "TRAIN=0\t\tTrain NOT coming." + line_ending
            out += "TRAIN=1\t\tTrain coming." + line_ending

            out = (out + line_ending).encode('utf-8')
            self.conn.send(out)
        else:
            print("Don't recognize ")
            self.conn.send(b'Error , ' + data.encode('utf-8') + line_ending.encode('utf-8'))


class TrafficSerial():
    def __init__(self):
        super().__init__()
        self.ser = serial.Serial()
        self.comport = "Not specified"
        self.baudrate = "Not specified"
        self.keep_going = True
        self.run_d_thread = True
        self.ending = "\r\n"
        self.response_ready = False
        self.response = ""
        self.wait_time_ms = 1000 # 1 second
        self.trafficMachine = TrafficMachine()
        print("TrafficSerial : " + self.trafficMachine.state.name)
        self.t = threading.Thread(target=self.read_thread, name="SerialNoProtocol read_thread")
        self.t.start()

    def __repr__(self):
        pass

    def __str__(self):
        return 'TrafficSerial com port:{} Baud rate:{}'.format(self.comport, self.baudrate)

    def send_data(self, data): #
        if self.ser.is_open:
            self.ser.write(data.encode('utf-8')+self.ending.encode('utf-8'))
            #self.ser.write(data + self.ending)

    def stop_Thread(self):
        self.run_d_thread = False
        self.t.join(2)
        print("Thread alive: " + str(self.t.is_alive()))

    def select_port(self, **kwargs): # kwargs- include info for serial port or network port
        # 'comport' : comx or /dev/ttyx   depending on system
        # 'baudrate' : 9600
        # 'parity' : none , odd, even
        # 'stopbits' : 1, 1.5, 2

        try:
            self.ser.timeout = 1 # timeout in 1 second
            #print(dir(self.ser))
            if 'baudrate' in kwargs:
                print('found baudrate')
                self.baudrate = str(kwargs['baudrate'])
                self.ser.baudrate = kwargs['baudrate']
            else:
                self.ser.baudrate = 9600

            if 'comport' in kwargs:
                print('found comport '+ kwargs['comport'])
                self.comport = kwargs['comport']
                self.ser.port = kwargs['comport']
            else:
                return False  # must specify comport

            if 'parity' in kwargs:
                print('found parity')
                if kwargs['parity'] == 'E':
                    self.ser.parity = serial.PARITY_EVEN
                elif kwargs['parity'] == 'O':
                    self.ser.parity = serial.PARITY_ODD
                elif kwargs['parity'] == 'N':
                    self.ser.parity = serial.PARITY_NONE
                else:
                    pass #error
            else:
                self.ser.parity = serial.PARITY_NONE  # default

            if 'stop' in kwargs:
                print('found stop')
                self.ser.stopbits = kwargs['stop']
            else:
                self.ser.stopbits = 1  # default
        except :
            return False

        return True

    def read_thread(self):
        # set run_d_thread to False to kill thread
        accumulated = ""
        while self.run_d_thread:
            if self.ser.is_open:
                try:
                    dta = self.ser.read() # will timeout every second
                    # print("read_thread: " + str(dta))
                    # line = self.ser.readline() # read \n terminated line
                    # print("data len: " + str(len(dta)))
                    if dta == b'\x03': # cntrl-c
                        self.keep_going = False
                        print("exit " + threading.currentThread().getName())
                        break
                    if len(dta) >= 1:
                        accumulated = accumulated + dta.decode()
                        # print("accumulated: " + accumulated)
                        if self.ending in accumulated:
                            print("Serial read_thread found return ")
                            self.decode_data(accumulated) # assume ending at end-- need to verify that??
                            accumulated = ""

                except:
                    print("exception "+ threading.currentThread().getName())
                    print("read_thread Unexpected error:", sys.exc_info()[0])
                    error_type, error_message, error_traceback = sys.exc_info()
                    print(error_message)
                    print(error_traceback)

    def connect(self):
        if self.ser != None and not self.ser.is_open:
            self.ser.open()

    def disconnect(self):
        if self.ser != None and self.ser.is_open:
            self.ser.close()

    def get_available_ports(self):
        # return com port available
        import serial.tools.list_ports
        avail_list = []
        #print (dir(serial.tools.list_ports.comports()))
        for port in serial.tools.list_ports.comports():
            #print(dir(port))
            #print(str(port.device))
            avail_list.append(port.device)
        return (avail_list)

    def decode_data(self, data):
        time0 = time.clock()
        # line_ending = os.linesep
        line_seperation = '\v' # vertical tab
        stripped_data = data.upper().strip()
        print("rec " + stripped_data)
        if stripped_data == "CHANGE":
            print("traffic change ")
            self.trafficMachine.change()
            print("send back OK ")
            self.send_data('CHANGE OK')
        elif stripped_data == "?STATE":
            print("traffic state ")
            state = self.trafficMachine.state.name
            print("send back " + state)
            self.send_data("?STATE "+state )
        elif stripped_data == "CAREW=1":
            self.trafficMachine.carwaitingEW = True
            self.send_data('CAREW=1 OK')
        elif stripped_data == "CAREW=0":
            self.trafficMachine.carwaitingEW = False
            self.send_data('CAREW=0 OK' )

        elif stripped_data == "CARNS=1":
            self.trafficMachine.carwaitingNS = True
            self.send_data('CARNS=1 OK')
        elif stripped_data == "CARNS=0":
            self.trafficMachine.carwaitingNS = False
            self.send_data('CARNS=0 OK')

        elif stripped_data == "TRAIN=1":
            self.trafficMachine.train_coming = True
            self.send_data('TRAIN=1 OK')
        elif stripped_data == "TRAIN=0":
            self.trafficMachine.train_coming = False
            self.send_data('TRAIN=0 OK')

        elif stripped_data == "ERR=1":
            self.trafficMachine.light_error = True
            self.send_data('ERR=1 OK')
        elif stripped_data == "ERR=0":
            self.trafficMachine.light_error = False
            self.send_data('ERR=0 OK')

        elif stripped_data == "?MENU":
            time1 = time.clock()
            out = "?MENU" + line_seperation
            out += "CAREW=0\t\tCar NOT waiting at EW intersection." + line_seperation
            out += "CAREW=1\t\tCar waiting at EW intersection." + line_seperation
            out += "CARNS=0\t\tCar NOT waiting at EW intersection." + line_seperation
            out += "CARNS=1\t\tCar waiting at NS intersection." + line_seperation
            out += "CHANGE\t\tInitiate a state change." + line_seperation
            out += "ERR=0\t\tNo system error." + line_seperation
            out += "ERR=1\t\tSystem error." + line_seperation
            out += "?STATE\t\tRead the traffic state." + line_seperation
            out += "TRAIN=0\t\tTrain NOT coming." + line_seperation
            out += "TRAIN=1\t\tTrain coming." + line_seperation
            time2 = time.clock()
            self.send_data(out)
            time3 = time.clock()
            print("time0: {}".format(time0))
            print("time1: {}".format(time1))
            print("time2: {}".format(time2))
            print("time3: {}".format(time3))
        else:
            print("Don't recognize ")
            self.send_data('Error , ' + data)

if __name__ == '__main__':
    resp = input("Enter: select (S)erial or (E)thernet: ")

    if resp == "S" or resp == "s" :
        print("serial selected")
        com_port = input("Enter: Com port (COM1, COM2, etc.): ")
        com_port = com_port.upper()
        TS = TrafficSerial()
        print("start serial thread")
        TS.select_port(comport=com_port, baudrate=57600)
        TS.connect()
        while TS.keep_going:
            pass
        TS.disconnect()
        TS.run_d_thread = False
        TS.t.join()

    elif resp == "E" or resp == "e" :
        print("Ethernet selected")
        TS = TrafficServer()
        print("start server thread")
        TS.start_server()
        while TS.keep_going:
            pass

    else:
       print("Nothing selected")

    if False: # simple test
        trafficMachine = TrafficMachine()
        print(trafficMachine.state.name)

        trafficMachine.carwaitingEW = True
        for changes in range(0,8):
            trafficMachine.change()
            #print(str(trafficMachine.state))
            print(trafficMachine.state.name)

    if False: #network connection
        TS = TrafficServer()
        print("start server thread")
        TS.start_server()
        while TS.keep_going:
            pass

    if False:#serial connection
        print(len(sys.argv))
        print("The arguments are: ", str(sys.argv))
        com_port = "COM1"
        if(len(sys.argv) == 2):
            com_port=sys.argv[1]
        TS = TrafficSerial()
        print("start serial thread")
        TS.select_port(comport=com_port, baudrate=57600)
        TS.connect()
        while TS.keep_going:
            pass
        TS.disconnect()
        TS.run_d_thread = False
        TS.t.join()

    print("Program Done")

