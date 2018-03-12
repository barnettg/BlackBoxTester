# Base class for communications classes
#
#

from abc import ABCMeta, abstractmethod

class Communications(metaclass=ABCMeta):
    def __init__(self):
        self.rec_observers = []
        self.log_observers = []
    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def send_data(self, data):
        pass

    @abstractmethod
    def send_data_async(self, data):
        pass
    @abstractmethod
    def select_port(self, **kwargs): # kwargs- include info for serial port or network port
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def reconnect(self):
        pass

    @abstractmethod
    def register_rx(self, observ):
        pass

    @abstractmethod
    def notify_rx(self, data):
        pass

    @abstractmethod
    def register_log(self, observ):
        pass

    @abstractmethod
    def notify_log(self, data):
        pass

    @abstractmethod
    def get_status(self):
        # return connection status and port info
        pass

    @abstractmethod
    def get_available_ports(self):
        # return com port available
        pass

    @abstractmethod
    def stop_Thread(self):
        pass

if __name__ == '__main__':
    pass