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
        self.communications = None  # pointer to the communications manager
        self.configuration = None  # pointer to the configuration manager
        self.logging = None  # pointer to the logging manager
        self.script = None  # pointer to the script manager
        self.model = None  # pointer to the model class
        self.view = None  # pointer to the View class
        self.controller = None  # pointer to the controller class
        self.running_as_group = True # script can check if run as single execution or as a group of scripts
        self.project_directory = None # path to project

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
        return None

    def reconnect(self, port):
        if self.communications is not None:
            return self.communications.reconnect(port)
        return None

    def script_wants_to_stop_all(self, message):
        if self.script is not None:
            return self.script.script_ordered_stop(message)
        return None

    def is_async_data_ready(self, port):
        # check if asynchronous data is available
        if self.communications is not None:
            return self.communications.is_data_ready(port)
        return None

    def get_async_data(self, port):
        # get asynchronous data
        if self.communications is not None:
            return self.communications.get_data(port)
        return None

    def open_message_box(self, **kwargs):  # minimum message = "xxx" -> dialog with OK and Cancel buttons
        if self.controller is not None:
            return self.controller.script_messagebox(**kwargs)  # returns depending on kwarg options-> yes,no,ok,cancel
                                                                # and optional additional textbox entries
        return None

if __name__ == "__main__":
    class DummyScripts:
        def script_ordered_stop(self,message):
            print("STOP: "+message)

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
    print("Cannot send yet: " + hc.send(0, "123"))
    hc.communications = DummyCommunications()
    hc.script = DummyScripts()
    print(hc.reconnect(0))
    print(hc.send(1, "hello"))
    print(hc.is_async_data_ready(2))
    print(hc.get_async_data(3))
    hc.message_register(dummy_message)
    hc.log_message_register(dummy_log_message)
    hc.write_message("A message")
    hc.write_message_log("A log message")
    hc.script_wants_to_stop_all("need to stop")
