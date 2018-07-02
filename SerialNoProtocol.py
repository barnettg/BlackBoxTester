# serial port without protocol
# send data and add ending char(s) to
#   send with wait for response or not
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
import string


class SerialNoProtocol(Communications):
    def __init__(self, prt_id):
        """
        Serial protocol with a simple carriage return to identify end of packet

        Args:
            port_id (int): Assigned ID, used for reference only

        Returns:
            None
        """
        super().__init__()
        self.ser = serial.Serial()              # serial port instance
        self.comport = "Not specified"          # string of com port "COMx"
        self.baudrate = 9600                    #
        self.port_id = prt_id                   # ID reference
        self.run_d_thread = True                # Set to False to stop thread
        self.ending = "\r\n"                    # data packet end to look for. Windows '\r\n' , Linux '\n'
        self.response_ready = False             # True if a data packet has been received
        self.response = ""                      # Class variable to hold received data packet
        self.wait_time_ms = 1000                # Millisecond to wait for a response after a send
        self.printable = string.ascii_letters + string.digits + string.punctuation + ' '
        self.t = threading.Thread(target=self.read_thread, name="SerialNoProtocol read_thread")  # read thread
        self.t.start()

    def __repr__(self):
        return '{self.__class__.__name__}({self.port_id})'.format(self=self)

    def __str__(self):
        """
        Returns string representation for class
        """
        return 'SerialNoProtocol port ID:{}, com port:{}, Baud rate:{}'.format(self.port_id,
                                                                               self.comport,
                                                                               self.baudrate)

    def send_data(self, data: str)-> str:  # NOTE: test if can send non-printable char
        """
        Call this method to send data through serial port and wait for an answer. Generally called by Helper class.

        Args:
            data (str): String data

        Returns:
            String Message response to sent data or an Error message
        """
        return_data = "Error, no data received within timeout from serial com with port ID {}".format(self.port_id)
        self.response_ready = False
        if self.ser.is_open:
            self.ser.write(data.encode('utf-8')+self.ending.encode('utf-8'))
            # get time
            start = time.clock()
            while True:  # loop until timeout or
                # get time
                # if time out then return
                end = time.clock()
                if (end-start)*1000 > self.wait_time_ms:
                    # print("SerialNoProtocol send_data :timeout break")
                    # print("start:{} end:{}".format(start, end))
                    break
                # check for data
                if self.response_ready:
                    # print("SerialNoProtocol ->send_data-> response_ready-> start:{} end:{}  diff: {}".format(start,
                    #                                                                                   end,
                    #                                                                                   end-start))
                    return_data = self.response
                    self.response_ready = False
                    break
        else:
            return_data = "Error, serial com with port ID {} not open".format(self.port_id)

        return return_data

    def send_data_async(self, data: str) -> bool:
        """
        Call this method to send data through serial port and NOT wait for an answer. Generally called by Helper class.

        Args:
            data (str): String data

        Returns:
            True if port is open
        """
        self.response_ready = False
        if self.ser.is_open:
            self.ser.write(data.encode('utf-8')+self.ending.encode('utf-8'))
            return True
        return False

    def stop_Thread(self) -> None:
        """
        Stops the read thread. Will wait until thread stops or 2 seconds

        Args:
            None

        Returns:
            None
        """
        self.run_d_thread = False
        self.t.join(2)
        # print("Thread alive: " + str(self.t.is_alive()))

    def set_data_ending(self, end: str) -> None:  # NOTE: change to property ?
        """
        Set the ending for sending and receiving strings.

        Args:
            end (str) : Usually either \r\n or \n.

        Returns:
            None
        """
        self.ending = end

    def get_data_ending(self) -> str:  # NOTE: change to property ?
        """
        Get the ending for sending and receiving strings.

        Args:
            None

        Returns:
            The ending string usually either \r\n or \n.
        """
        return self.ending

    def clear_rec_buffer(self):
        """
        Empties the receive buffer

        Args:
            None

        Returns:
            None
        """
        self.response_ready = False
        self.response = ""

    def set_data_wait_ms(self, ms: int) -> None:  # NOTE: change to property ?
        """
        Set the time to wait for a response in ms after sending data.

        Args:
            ms (int) : The milliseconds.

        Returns:
            None
        """
        self.wait_time_ms = ms

    def get_data_wait_ms(self) -> int:  # NOTE: change to property ?
        """
        Get the ending for sending and receiving strings.

        Args:
            None

        Returns:
            The milliseconds wait time
        """
        return self.wait_time_ms

    def select_port(self, **kwargs) -> bool:  # kwargs- include info for serial port or network port
        """
        Get the ending for sending and receiving strings.

        Args:
            kwargs : Serial port configurations. Any combination of comport, baudrate,  parity, stopbits.

        Returns:
            True if
        """

        # 'comport' : comx or /dev/ttyx   depending on system
        # 'baudrate' : 9600
        # 'IP' : '192.168.1.1'
        # 'networkPort' : '502'
        # 'parity' : none , odd, even
        # 'stopbits' : 1, 1.5, 2

        try:
            self.ser.timeout = 1  # timeout in 1 second
            # print(dir(self.ser))
            if 'baudrate' in kwargs:
                # print('found baudrate')
                self.baudrate = str(kwargs['baudrate'])
                self.ser.baudrate = kwargs['baudrate']
            else:
                self.baudrate = 9600
                self.ser.baudrate = 9600

            if 'comport' in kwargs:
                # print('found comport')
                self.comport = kwargs['comport']
                self.ser.port = kwargs['comport']
            else:
                return False  # must specify comport

            if 'parity' in kwargs:
                # print('found parity')
                if kwargs['parity'] == 'E':
                    self.ser.parity = serial.PARITY_EVEN
                elif kwargs['parity'] == 'O':
                    self.ser.parity = serial.PARITY_ODD
                elif kwargs['parity'] == 'N':
                    self.ser.parity = serial.PARITY_NONE
                else:
                    pass  # error
            else:
                self.ser.parity = serial.PARITY_NONE  # default

            if 'stop' in kwargs:
                # print('found stop')
                self.ser.stopbits = kwargs['stop']
            else:
                self.ser.stopbits = 1  # default

            if 'line_ending' in kwargs:
                # print('found line_ending')
                self.ending = kwargs['line_ending']

        except:
            return False

        return True

    def read_thread(self):
        """
        The serial port read thread looks for ending char string and places all received data in a class variable.

        Args:
            None

        Returns:
            None
        """
        # set run_d_thread to False to kill thread
        accumulated = ""
        while self.run_d_thread:
            if self.ser.is_open:
                try:
                    dta = self.ser.read()  # will timeout every second
                    # print("SerialNoProtocol read_thread: " + str(dta))
                    # line = self.ser.readline() # read \n terminated line
                    if len(dta) > 0:
                        rec = dta.decode()
                        # raw_rec = dta.decode()
                        accumulated = accumulated + rec
                        # print("SerialNoProtocol->read_thread Accumulated: "+ accumulated)
                        if self.ending in accumulated:
                            # raw_rec = self.hex_escape(accumulated)
                            self.response = accumulated.strip()  # assume ending at end-- need to verify that??
                            # print("SerialNoProtocol->read_thread  self.response: " + self.response)
                            # print("SerialNoProtocol->read_thread  raw_rec: " + raw_rec)
                            accumulated = ""
                            self.response_ready = True
                            self.notify_rx(dta)
                except:
                    pass

    def hex_escape(self, s) -> str:
        """
        Converts non printable data to two digit hex format

        Args:
            s (str): Input string.

        Returns:
            Converted string.
        """
        return ''.join(c if c in self.printable else r'\x{0:02x}'.format(ord(c)) for c in s)

    def connect(self):
        """
        Connects to the target. In this protocol there is not a connection protocol so it verifies the port is open.

        Args:
            None

        Returns:
            True if the serial port is open.
        """
        if self.ser is not None and not self.ser.is_open:
            self.ser.open()
            # print("Serial port try to open: " + str(self.ser.is_open))
        return self.ser.is_open

    def disconnect(self):
        """
        Disconnects from the target. In this protocol there is not a disconnect protocol so it will only close the port.

        Args:
            None

        Returns:
            None
        """
        if self.ser is not None and self.ser.is_open:
            self.ser.close()

    def reconnect(self):
        """
        Reconnects to the target.
        In this protocol there is not a reconnect protocol so it will only close and open the port.

        Args:
            None

        Returns:
            True if the serial port is open.
        """
        if self.ser is not None and self.ser.is_open:
            self.ser.close()
            self.ser.open()
        return self.ser.is_open

    def register_rx(self, observ) -> None:
        """
        Register a method to be called when a complete data packet is received

        Args:
            observ :  A method

        Returns:
            None
        """
        self.rec_observers.append(observ)

    def unsubscribe_rx(self, observ) -> None:
        """
        Remove a method to be called when a complete data packet is received

        Args:
            observ :  A method

        Returns:
            None
        """
        if observ in self.rec_observers:
            self.rec_observers.remove(observ)

    def notify_rx(self, data: str) -> None:
        """
        Calls all registered methods when a complete data packet is received

        Args:
            data (str)  :  Message string.

        Returns:
            None
        """
        for item in self.rec_observers:
            item(data)

    def register_log(self, observ):
        """
        Register a method to be called when logging information

        Args:
            observ :  A method

        Returns:
            None
        """
        self.log_observers.append(observ)

    def unsubscribe_log(self, observ):
        """
        Remove a method to be called when logging information

        Args:
            observ :  A method

        Returns:
            None
        """
        if observ in self.log_observers:
            self.log_observers.remove(observ)

    def notify_log(self, data):
        """
        Calls all registered methods when logging information

        Args:
            data (str)  :  Message string.

        Returns:
            None
        """
        for item in self.log_observers:
            item(data)

    def get_status(self) -> dict:  #
        ret_dict = {
            'ID': self.port_id,
            'type': 'serial',
            'comport': self.comport,
            'baudrate': self.ser.baudrate,
            'file_name': "SerialNoProtocol",
            'parity': self.ser.parity,
            'stopbits': self.ser.stopbits
        }

        return ret_dict

    def get_available_ports(self) -> list:
        """
        Get the available system serial ports

        Args:
            None

        Returns:
            A list of system serial ports
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

if __name__ == '__main__':
    snp = SerialNoProtocol(0)
    print(snp)
    print(repr(snp))
    available_ports = snp.get_available_ports()
    print(str(available_ports))
    print('serial.PARITY_EVEN =' + serial.PARITY_EVEN)
    print('serial.PARITY_ODD =' + serial.PARITY_ODD)
    print('serial.PARITY_NONE =' + serial.PARITY_NONE)
    print('serial.STOPBITS_ONE=' + str(serial.STOPBITS_ONE))
    print('serial.STOPBITS_ONE_POINT_FIVE =' + str(serial.STOPBITS_ONE_POINT_FIVE))
    print('serial.STOPBITS_TWO =' + str(serial.STOPBITS_TWO))

    snp.select_port(baudrate=19200, comport=available_ports[0])
    snp.connect()
    snp.send_data("Hello\n")
    snp.disconnect()
    snp.stop_Thread()