# Network port without protocol
#
#

from CommunicationsBase import Communications
import socket
import threading
import sys
import time


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

    def __del__(self):
        self.notify_log('NetworkNoProtocol -- destructor')
        self.run_d_thread = False
        if self.ser is not None:
            self.ser.close()

    def __repr__(self):
        pass

    def __str__(self):
        return 'NetworkNoProtocol portID:{} IP:{} Port:{}'.format(self.port_id,self.host,self.port)

    def send_data(self, data):  # test if can send nonprintable char
        if self.is_open:
            self.ser.send(data.encode('utf-8'))

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
        if 'networkPort' in kwargs:
            self.notify_log('found networkPort')
            self.port = kwargs['networkPort']

    def read_thread(self):  # need to do
        self.notify_log("Start Thread " + str(self.port_id))
        self.ser.setblocking(0)
        while self.run_d_thread:
            if self.is_open:
                try:
                    data = self.ser.recv(self.BUFFER_SIZE)
                    self.notify_rx(data.decode())
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
    nnp.select_port(IP='127.0.0.1', networkPort=80)
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