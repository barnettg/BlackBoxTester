# serial port without protocol
#
#

from CommunicationsBase import Communications
import serial

class SerialNoProtocol(Communications):
    def __init__(self):
        super().__init__()
        self.ser = None
        self.run_d_thread = True

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def send_data(self,data): # test is can send nonprintable char
        if self.ser.is_open:
            self.ser.write(data.encode('utf-8'))

    def select_port(self, **kwargs): # kwargs- include info for serial port or network port
        # 'comport' : comx or /dev/ttyx   depending on system
        # 'baudrate' : '9600'
        # 'IP' : '192.168.1.1'
        # 'networkPort' : '502'
        # 'parity' : none , odd, even
        # 'stopbits' : 1, 1.5, 2
        self.ser = serial.Serial()
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

    def read_thread(self):
        while self.run_d_thread:
            if self.ser.is_open:
                try:
                    self.notify_rx (self.ser.read())
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