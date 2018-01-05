# dummy serial port without protocol
#
#

from CommunicationsBase import Communications

class SerialDummy(Communications):
    def __init__(self):
        super().__init__()
        self.ser = None
        self.run_d_thread = True

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def send_data(self,data): # return data sent
        self.notify_rx (data)

    def select_port(self, **kwargs): # kwargs- include info for serial port or network port
        # 'comport' : comx or /dev/ttyx   depending on system
        # 'baudrate' : '9600'
        # 'IP' : '192.168.1.1'
        # 'networkPort' : '502'
        # 'parity' : none , odd, even
        # 'stopbits' : 1, 1.5, 2
        self.ser = ser_dumb()
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
                self.ser.parity = 'E'
            elif kwargs['parity'] == 'O':
                self.ser.parity = 'O'
            elif kwargs['parity'] == 'N':
                self.ser.parity = 'N'
            else:
                pass #error

        if 'stop' in kwargs:
            print('found stop')
            self.ser.stopbits = kwargs['stop']

    def read_thread(self):
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
        avail_list = ['COM1', 'COM2']
        return (avail_list)

class ser_dumb:
    def __init__(self):
        self.baudrate = 9600
        self.is_open = False
        self.stopbits = 1
        self.port = 'COM1'
        self.parity = 1

    def close(self):
        is_open = False

    def open(self):
        is_open = True



if __name__ == '__main__':
    def get_data(data):
        print(data)

    snp = SerialDummy()
    available_ports = snp.get_available_ports()
    print(str(available_ports))
    snp.select_port(baudrate = 19200, comport = available_ports[0])
    snp.register_rx(get_data)
    snp.connect()
    snp.send_data("Hello\n")
    snp.disconnect()