# Network port without protocol
#
#

from CommunicationsBase import Communications
import socket
import threading
import sys
import time
import string


class NetworkNoProtocol(Communications):
    def __init__(self, prt_id):
        super().__init__()
        self.ser = None
        self.run_d_thread = True
        self.is_open = False
        self.host = '127.0.0.1'
        self.port = 62
        self.BUFFER_SIZE = 1024
        self.port_id = prt_id
        self.t = None
        self.ending = "\r\n"
        self.wait_time_ms = 1000 # 1 second
        self.response_ready = False
        self.response = ""
        self.printable = string.ascii_letters + string.digits + string.punctuation + ' '

    def __del__(self):
        self.notify_log('NetworkNoProtocol -- destructor')
        self.run_d_thread = False
        if self.ser is not None:
            self.ser.close()

    def __repr__(self):
        pass

    def __str__(self):
        return 'NetworkNoProtocol portID:{} IP:{} Port:{}'.format(self.port_id,self.host,self.port)

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

    def send_data(self, data):  # not done !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # test if can send nonprintable char
        return_data = "Error, no data received within timeout from Ethernet com with port ID {}".format(self.port_id)
        self.response_ready = False
        if self.is_open:
            self.ser.send(data.encode('utf-8') + self.ending.encode('utf-8'))
            # get time
            start = time.clock()
            while True: # loop until timeout or
                # get time
                # if time out then return
                end = time.clock()
                if (end-start)*1000 > self.wait_time_ms :
                    break
                # check for data
                if self.response_ready:
                    return_data = self.response
                    self.response_ready = False
                    break
        else:
            return_data = "Error, Ethernet com with port ID {} not open".format(self.port_id)

        return return_data

    def send_data_async(self, data):
        # test if can send non printable char
        if self.is_open:
            self.ser.send(data.encode('utf-8'))
        else:
            return "Error, port ID {} not open".format(self.port_id)

    def select_port(self, **kwargs):  # kwargs- include info for serial port or network port
        # 'comport' : comx or /dev/ttyx   depending on system
        # 'baudrate' : '9600'
        # 'IP' : '192.168.1.1'
        # 'networkPort' : '502'
        # 'parity' : none , odd, even
        # 'stopbits' : 1, 1.5, 2
        self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print(dir(self.ser))
        if 'IP' in kwargs:
            self.notify_log('found IP')
            self.host = kwargs['IP']
        else:
            return False
        if 'networkPort' in kwargs:
            self.notify_log('found networkPort')
            self.port = kwargs['networkPort']
        else:
            return False
        return True

    def read_thread(self):  # need to do !!!!!!!!!!check traffic.py for accumulating data line!!!!!!!!!!!!!!!!!!!!!!!!
        # self.response_ready = False
        # self.response = ""
        self.notify_log("Start Thread " + str(self.port_id))
        self.ser.setblocking(0)
        accumulated = ""
        while self.run_d_thread:
            if self.is_open:
                try:
                    dta = self.ser.recv(self.BUFFER_SIZE)
                    # print("SerialNoProtocol read_thread: " + str(dta))
                    # line = self.ser.readline() # read \n terminated line
                    if len(dta) >0 :
                        rec = dta.decode()
                        raw_rec = dta.decode()
                        accumulated = accumulated + str(rec)
                        raw_rec = self.hex_escape(accumulated)
                        #print("NetworkNoProtocol->read_thread Accumulated: " + str(accumulated))
                        #print("NetworkNoProtocol->read_thread Accumulated Hex: " + str(raw_rec))
                        if self.ending in accumulated:
                            #raw_rec = self.hex_escape(accumulated)
                            self.response = accumulated.strip() # assume ending at end-- need to verify that??
                            # print("SerialNoProtocol->read_thread  self.response: " + self.response)
                            # print("SerialNoProtocol->read_thread  raw_rec: " + raw_rec)
                            accumulated = ""
                            self.response_ready = True
                            self.notify_rx (self.response)
                    #self.notify_rx(data.decode())
                except TypeError:
                    print("read_thread Unexpected error:", sys.exc_info()[0])
                    error_type, error_message, error_traceback = sys.exc_info()
                    print(error_message)
                    print(error_traceback)
                except ConnectionAbortedError:
                    print("read_thread Unexpected error:", sys.exc_info()[0])
                    error_type, error_message, error_traceback = sys.exc_info()
                    print(error_message)
                    print(error_traceback)
                except OSError:
                    pass

        self.notify_log("End Thread " + str(self.port_id))

    def hex_escape(self, s):
        return ''.join(c if c in self.printable else r'\x{0:02x}'.format(ord(c)) for c in s)

    def stop_Thread(self):
        self.run_d_thread = False
        self.t.join(2)

    def connect(self):  # need to detect errors
        if self.ser is not None:
            self.notify_log('connect: ' + str(self.ser.connect((self.host, self.port))))
            self.t = threading.Thread(target=self.read_thread,
                                      name="NetworkNoProtocol read_thread " + str(self.port_id))
            self.t.start()
            self.is_open = True
        return True

    def disconnect(self):
        if self.ser is not None:
            self.run_d_thread = False
            self.t.join(5)
            self.ser.close()
            self.ser = None
            self.is_open = False

    def reconnect(self):
        if self.ser is not None:
            self.ser.close()
        self.ser.connect((self.host, self.port))

    def register_rx(self, observ):
        self.rec_observers.append(observ)

    def unsubscribe_rx(self, observ):
        if observ in self.rec_observers:
            self.rec_observers.remove(observ)

    def notify_rx(self, data):
        self.notify_log("notify_rx -- received data: " + data)
        for item in self.rec_observers:
            item(data)

    def register_log(self, observ):
        self.log_observers.append(observ)

    def unsubscribe_log(self, observ):
        if observ in self.log_observers:
            self.log_observers.remove(observ)

    def notify_log(self, data):
        for item in self.log_observers:
            item("NetworkNoProtocol::" + data)

    def get_status(self):
        return {"open":self.is_open, "port_id":self.port_id, "IP":self.host, "port":self.port}

    def get_available_ports(self):  # not needed for network connection
        avail_list = []
        return avail_list

if __name__ == '__main__':
    # to test, run a server on port 80 --  Server2Thread.py
    def rec_date(data):
        print("rec_data -- " + data)

    def log_rec_message(message):
        print("log_rec_message -- " + message)

    nnp = NetworkNoProtocol(0)
    nnp.register_rx(rec_date)
    nnp.register_log(log_rec_message)
    nnp.select_port(IP='192.168.1.4', networkPort=23)  # IP='127.0.0.1', networkPort=80)
    nnp.connect()
    print(str(nnp.get_status()))
    nnp.send_data("Hello\n")
    time.sleep(2)
    nnp.send_data("World\n")
    time.sleep(2)
    nnp.send_data("Quick\n")
    time.sleep(2)
    nnp.send_data("\n")
    time.sleep(2)
    nnp.disconnect()
    print("Main Done")