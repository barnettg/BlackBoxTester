# Network port without protocol
#
#

from CommunicationsBase import Communications
import socket

class NetworkNoProtocol(Communications):
    def __init__(self):
        super().__init__()
        self.ser = None
        self.run_d_thread = True
        self.is_open = False

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def send_data(self,data): # test if can send nonprintable char
        if self.is_open:
            self.ser.send(data.encode('utf-8'))

    def select_port(self, **kwargs): # kwargs- include info for serial port or network port
        # 'comport' : comx or /dev/ttyx   depending on system
        # 'baudrate' : '9600'
        # 'IP' : '192.168.1.1'
        # 'networkPort' : '502'
        # 'parity' : none , odd, even
        # 'stopbits' : 1, 1.5, 2
        self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print(dir(self.ser))
        if 'IP' in kwargs:
            print('found IP')
            self.host = kwargs['IP']
        if 'networkPort' in kwargs:
            print('found networkPort')
            self.port = kwargs['networkPort']


    def read_thread(self): # need to do
        while self.run_d_thread:
            if self.is_open:
                try:
                    pass
                    #self.notify_rx (self.ser.read())
                except:
                    pass



    def connect(self): # need to detect errors
        if self.ser != None :
            print('connect: ' + str(self.ser.connect((self.host, self.port))))
            self.is_open = True
        return True

    def disconnect(self):
        if self.ser != None:
            self.ser.close()
            self.ser = None
            self.is_open = False

    def reconnect(self):
        if self.ser != None:
            self.ser.close()
            self.ser.connect((self.host, self.port))

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

    def get_available_ports(self): # not needed for network connection
        avail_list = []
        return (avail_list)

if __name__ == '__main__':
    nnp = NetworkNoProtocol()
    nnp.select_port(IP = '127.0.0.1', networkPort = 80)
    nnp.connect()
    nnp.send_data("Hello\n")
    nnp.disconnect()