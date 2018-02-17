# helper methods:
# reconnect(port)
# send(port,data)
# is_async_data_ready(port)
# get_async_data(port)
# write_message(message)
# write_message_log(message)

# C# methods avaialable in HelperClass:
# string Send(string data) :
#   Sends data to the serial or network port and
#   returns a string containing any response
# void WriteMessage(string data) :
#   Writes a message to the script terminal
# DialogResult OpenMessageBox(string title, string message) :
#   Opens a message box with OK and CANCEL
# WriteMessageSerialLog(string message) :
#   Writes a message to the serial log
# void WriteMessageLog(string message) :
#   Writes a message to BBTester log
# void SetUsingPort(string port) :
#   set the port to use. The port names are in the Ports List
# void Reconnect() :
#   reconnect to a port after rebooting
# void scriptWantsToStopAll() :
#   Stop running scripts
# This IronPython script is started with a call to function Run(HelperClass) that
#   returns a string starting with "PASS" or "FAIL"

class HelperClassPy:
    def __init__(self):
        self.log_message_list = []
        self.message_list = []
        self.communications = None

    def message_register(self, fnction):
        self.message_list.append(fnction)

    def message_unregister(self, fnction):
        if fnction in self.message_list:
            self.message_list.remove(fnction)

    def log_message_register(self, fnction):
        self.log_message_list.append(fnction)

    def log_message_unregister(self, fnction):
        if fnction in self.log_message_list:
            self.log_message_list.remove(fnction)

    def write_message(self, message):
        for item in self.message_list:
            item(message)

    def write_message_log(self, message):
        for item in self.log_message_list:
            item(message)

    def send(self, port, data):
        if self.communications is not None:
            return self.communications.send(port, data)

    def reconnect(self, port):
        if self.communications is not None:
            return self.communications.reconnect(port)

    def is_async_data_ready(self, port):
        # check if asynchronous data is available
        if self.communications is not None:
            return self.communications.is_data_ready(port)

    def get_async_data(self, port):
        # get asynchronous data
        if self.communications is not None:
            return self.communications.get_data(port)

if __name__ == "__main__":
    class DummyCommunications:
        def send(self, port, data):
            return "dummy data {} on port {} ".format(str(data), str(port))

        def is_data_ready(self, port):
            return True

        def get_data(self, port):
            return "dummy async data on port {} ".format(str(port))

        def reconnect(self, port):
            return "reconnect on port {} ".format(str(port))

    def dummy_message(message):
        print(message)

    def dummy_log_message(message):
        print(message)

    hc = HelperClassPy()
    hc.communications = DummyCommunications()
    print(hc.reconnect(0))
    print(hc.send(1, "hello"))
    print(hc.is_async_data_ready(2))
    print(hc.get_async_data(3))
    hc.message_register(dummy_message)
    hc.log_message_register(dummy_log_message)
    hc.write_message("A message")
    hc.write_message_log("A log message")
