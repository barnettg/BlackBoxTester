# serial port without protocol
# send data and add ending char(s) to
# send with wait for response or not
# set timeout for waiting
# any data received outside of a waiting send is discarded

# receive data with ending char(s)

# to do:
# use properties for:
#       self.ending
#       self.wait_time_ms
#       self.run_d_thread

# complete
#   __repr__
#   __str__

from CommunicationsBase import Communications
import serial
import time
import threading

class SerialNoProtocol(Communications):
    def __init__(self):
        super().__init__()
        self.ser = serial.Serial()
        self.run_d_thread = True
        self.ending = "\r\n"
        self.response_ready = False
        self.response = ""
        self.wait_time_ms = 1000 # 1 second
        self.t = threading.Thread(target=self.read_thread, name="read_thread")
        self.t.start()

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def send_data(self, data): # test if can send non-printable char
        return_data = ""
        self.response_ready = False
        if self.ser.is_open:
            self.ser.write(data.encode('utf-8')+self.ending.encode('utf-8'))
            #get time
            start = time.clock()
            while True: # loop until timeout or
                #get time
                #if time out then return
                end = time.clock()
                if (end-start)*1000 > self.wait_time_ms :
                    break
                # check for data
                if self.response_ready:
                    return_data = self.response
                    self.response_ready = False
                    break

        return return_data

    def stop_Thread(self):
        self.run_d_thread = False
        self.t.join(2)
        print("Thread alive: " + str(self.t.is_alive()))


    def set_data_ending(self, end):
        self.ending = end

    def get_data_ending(self):
        return self.ending

    def clear_rec_buffer(self):
        self.response_ready = False
        self.response = ""

    def set_data_wait_ms(self, ms):
        self.wait_time_ms = ms

    def get_data_wait_ms(self):
        return self.wait_time_ms

    def select_port(self, **kwargs): # kwargs- include info for serial port or network port
        # 'comport' : comx or /dev/ttyx   depending on system
        # 'baudrate' : '9600'
        # 'IP' : '192.168.1.1'
        # 'networkPort' : '502'
        # 'parity' : none , odd, even
        # 'stopbits' : 1, 1.5, 2

        try:
            self.ser.timeout = 1 # timeout in 1 second
            #print(dir(self.ser))
            if 'baudrate' in kwargs:
                print('found baudrate')
                self.ser.baudrate = kwargs['baudrate']
            if 'comport' in kwargs:
                print('found comport')
                self.ser.port = kwargs['comport']

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

            if 'stop' in kwargs:
                print('found stop')
                self.ser.stopbits = kwargs['stop']
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
                    print("read_thread: " + str(dta))
                    #line = self.ser.readline() # read \n terminated line
                    if len(dta) >0 :
                        accumulated = accumulated + dta
                        if self.ending in accumulated:
                            self.response = accumulated # assume ending at end-- need to verify that??
                            accumulated = ""
                            self.response_ready = False
                            self.notify_rx (dta)
                except:
                    pass



    def connect(self):
        if self.ser != None and not self.ser.is_open:
            self.ser.open()

    def disconnect(self):
        if self.ser != None and self.ser.is_open:
            self.ser.close()

    def reconnect(self):
        if self.ser != None and self.ser.is_open:
            self.ser.close()
            self.ser.open()

    def register_rx(self, observ):
        self.rec_observers.append(observ)

    def unsubscribe_rx(self, observ):
        if observ in self.rec_observers:
            self.rec_observers.remove(observ)

    def notify_rx(self, data):
        for item in self.rec_observers:
            item(data)

    def register_log(self, observ):
        self.log_observers.append(observ)

    def unsubscribe_log(self, observ):
        if observ in self.log_observers:
            self.log_observers.remove(observ)

    def notify_log(self, data):
        for item in self.log_observers:
            item(data)

    def get_status(self):
        # return connection status and port info
        pass

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

if __name__ == '__main__':
    snp = SerialNoProtocol()
    available_ports = snp.get_available_ports()
    print(str(available_ports))
    print('serial.PARITY_EVEN =' + serial.PARITY_EVEN)
    print('serial.PARITY_ODD =' + serial.PARITY_ODD)
    print('serial.PARITY_NONE =' + serial.PARITY_NONE)
    print('serial.STOPBITS_ONE=' + str(serial.STOPBITS_ONE))
    print('serial.STOPBITS_ONE_POINT_FIVE =' + str(serial.STOPBITS_ONE_POINT_FIVE))
    print('serial.STOPBITS_TWO =' + str(serial.STOPBITS_TWO))

    snp.select_port(baudrate = 19200, comport = available_ports[0])
    snp.connect()
    snp.send_data("Hello\n")
    snp.disconnect()
    snp.stop_Thread()