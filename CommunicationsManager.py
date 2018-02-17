# CommunicationsManager.py
# - configure and control ports
# -- select port and assign part_id
# -- read and write port data

# called from helper class:
# reconnect(port_id)
# send(port_id,data)
# is_async_data_ready(port_id)
# get_async_data(port_id)
# set_using_port(string port_id)


class CommunicationsManager:
    def __init__(self):
        self.active_port = None
        self.available_port_ids = {}  # format "port_id":{ "protocol_class_name": "name", "description": " desc"}
        self.ports_connected = []

    def get_available_ports(self):
        return self.available_port_ids

    def set_active_port(self, prt_id):
        self.active_port = prt_id

    def assign_port(self, prt_id,  protocol_class):
        pass

    def unassign_port(self, prt_id):
        pass
        # check if self.active_port should be set to None

    def connect(self, port_id=None):  # not completed yet
        if port_id is None and self.active_port is None:
            raise ValueError('When trying to connect, a port is not specified')

        ret_val = False
        if port_id is None:  # default to active port
            port_id = self.active_port

        # try to connect
        return ret_val

    def reconnect(self, port_id=None):  # not completed yet
        if port_id is None and self.active_port is None:
            raise ValueError('When trying to reconnect, a port is not specified')

        ret_val = False
        if port_id is None:  # default to active port
            port_id = self.active_port

        # try to reconnect

        return ret_val

    def send(self, data, port_id=None):
        if port_id is None and self.active_port is None:
            raise ValueError('When trying to send data, a port is not specified')

    def is_async_data_ready(self, port_id=None):
        if port_id is None and self.active_port is None:
            raise ValueError('When checking for available asynchronous data, a port is not specified')

    def get_async_data(self, port_id=None):
        if port_id is None and self.active_port is None:
            raise ValueError('When trying to get asynchronous data, a port is not specified')

    def set_using_port(self, port_id):
        pass


if __name__ == "__main__":
    pass