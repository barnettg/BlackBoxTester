# Handles reading and writing configurations
# assumes proper directory structure but also check

import json
import os.path
import sys

# config file format
# 'files' : { -- script data --
#       }
# 'communications' : { 'ports' :{ 'port_id': {}}
   # port_id = 0, 1, 2 ...
        # 'type' : serial or ethernet

        # 'IP' : '192.168.1.1'
        # 'networkPort' : '502'

        # 'comport' : comx or /dev/ttyx   depending on system
        # 'baudrate' : '9600'
        # 'parity' : none , odd, even
        # 'stopbits' : 1, 1.5, 2
#       }
# 'misc' : { -- email --
#       }
# 'GUI' : { -- editor ---
#       }

class ConfigurationManager(object):
    """The summary line for a class docstring should fit on one line.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    """
    def __init__(self):
        """Example of docstring on the __init__ method.

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            param1 (str): Description of `param1`.
            param2 (:obj:`int`, optional): Description of `param2`. Multiple
                lines are supported.
            param3 (:obj:`list` of :obj:`str`): Description of `param3`.

        """
        self.ObserverList = []

    def empty_configuration(self):
        self.configuration_file = None
        self._configuration_content = {}
        self._configuration_content['files'] = {}
        self._configuration_content['communications'] = {}
        self._configuration_content['misc'] = {}
        self._configuration_content['GUI'] = {}

    def get_configuration_content(self):
        return self._configuration_content

    def set_configuration_content(self, value):
        self._configuration_content = value

    def set_configuration_file(self, path):
        self.debugging_print("set_configuration_file-path: " + path )
        self.configuration_file = path # project_path + "\\configurations\\" + config_filename #

    def read_configuration_file(self, config_filename = None):
        if config_filename == None :
            config_filename = self.configuration_file

        dir_path_and_filename = config_filename #project_path + "\\configurations\\" + config_filename #
        self.debugging_print("read_configuration_file-dir_path_and_filename: " + dir_path_and_filename )
        #if file exists then read-- otherwise create
        if os.path.isfile(dir_path_and_filename):
            self.debugging_print("found configuration file at: " + dir_path_and_filename)
            with open(dir_path_and_filename) as json_file:
                self.configuration_content = json.load(json_file)
            self.debugging_print("Total scripts dictionary")
            self.debugging_print(str(self.configuration_content))
            if 'files' not in self.configuration_content:
                self.configuration_content['files'] = {}
        else:
            self.debugging_print("did not find configuration file at: " + dir_path_and_filename)
            filesDic = {}
            self.configuration_content['files'] = {}
            self.configuration_content['communications'] = {}
            self.configuration_content['misc'] = {}
            self.configuration_content['GUI'] = {}

            self.debugging_print("Total scripts dictionary")
            self.debugging_print(str(self.configuration_content))
            self.write_configuration_file(config_filename)
        return self.configuration_content

    def write_configuration_file(self, config_filename = None):
        #self.logging_message("write_configuration_file " + str(config_filename))

        if config_filename == None :
            config_filename = self.configuration_file

        self.logging_message("write_configuration_file " + str(config_filename))
        self.logging_message("content: " + str(self.configuration_content))

        dir_path_and_filename = config_filename #project_path + "\\configurations\\"+config_filename
        self.debugging_print('dir_path_and_filename: ' + dir_path_and_filename)
        with open(dir_path_and_filename, 'w') as outfile:
            json.dump(self.configuration_content, outfile, indent=4, sort_keys=True)

    def debugging_print(self, message):
        " print out messages during development"
        if __name__ == '__main__':
            print("ConfigurationManager--" + message)

    # methods replaced by get_config_item and  set_config_item
    # def get_files_config(self):
    #     return self.configuration_content.get('files',default = {})
    #
    # def set_files_config(self, files_content):
    #     self.debugging_print("set files: " +str(files_content))
    #     self.configuration_content['files'] = files_content
    #     self.debugging_print("all: " +str(self.configuration_content))
    #
    # def get_communications_config(self):
    #     return self.configuration_content.get('communications',default = {})
    #
    # def set_communications_config(self, communications_content):
    #     self.configuration_content['communications'] = communications_content
    #
    # def get_misc_config(self):
    #     return self.configuration_content.get('misc',default = {})
    #
    # def set_misc_config(self, misc_content):
    #     self.configuration_content['misc'] = misc_content
    #
    # def get_GUI_config(self):
    #     return self.configuration_content.get('GUI',default = {})
    #
    # def set_GUI_config(self, GUI_content):
    #     self.configuration_content['GUI'] = GUI_content

    def get_config_item(self, item):
        return self.configuration_content.get(item,default = {})

    def set_config_item(self, item, content):
        self.configuration_content[item] = content

    def get_item_list(self):
        return ['files','communications', 'misc', 'GUI']

    ### vvvvvvvvv   Communications configuration  4/2018  working here begin!!!!!!!!!!!
    def get_communications_port_id_list(self) -> list:
        """
        Get a list of specified ports
        """
        if self.configuration_content['communications']["ports"]:
            prt_dictionary = self.configuration_content['communications']["ports"]
            # format { port_id0: {}, ... port_idn: {}}
            return list(prt_dictionary.keys())
        return None

    def get_communications_port_id_info(self, identification: str) -> dict:
        """
        Get the configuration parameters for a specific port
        :param identification: The port
        :return: A dictionary of the port parameters
        """
        if self.configuration_content['communications']["ports"][identification]:
            prt_dictionary = self.configuration_content['communications']["ports"][identification]
            return prt_dictionary
        return None

    def add_communications_port_id(self, identification: str, data_dictionary: dict) -> bool:
        """
        Add port parameters for specified port to the configuration file
        :param identification: port id
        :param data_dictionary: dictionary of parameters for the port
            'type' : serial                 'type' : ethernet
            'comport' : comx or /dev/ttyx   'IP' : '192.168.1.1'
            'baudrate' : '9600'             'networkPort' : '502'
        :return: True if data_dictionary has correct format otherwise False
        """
        ## data_dictionary format
        # 'type' : serial or ethernet
        # if ethernet:
        #   'IP' : '192.168.1.1'
        #   'networkPort' : '502'
        # if serial:
        #   'comport' : comx or /dev/ttyx   depending on system
        #   'baudrate' : '9600'  (optional - default 9600)
        #   'parity' : none , odd, even (optional - default none )
        #   'stopbits' : 1, 1.5, 2  (optional - default 1)
        looks_good = False
        if "ports" not in self.configuration_content['communications']:
            self.configuration_content['communications'] = {"ports": {}}

        if data_dictionary["type"]:
            if data_dictionary["type"] == "serial":
                if 'comport' in data_dictionary:
                    looks_good = True
            elif data_dictionary["type"] == "ethernet":
                if 'IP' in data_dictionary and 'networkPort'in data_dictionary:
                    looks_good = True
        if looks_good:
            self.configuration_content['communications']["ports"][identification] = data_dictionary
            return True
        return False

    def remove_communications_port_id(self, identification) -> bool:
        """
        Remove port parameters from the configuration file
        :param identification: specified port
        :return: returns True if removed the port
        """
        if self.configuration_content['communications']["ports"][id]:
            self.configuration_content['communications']["ports"].pop(id, None)
            return True
        return False

    def register_log(self, obs):
        self.ObserverList.append(obs)

    def unsubscribe_log(self, obs):
        if obs in self.ObserverList:
            self.ObserverList.remove(obs)

    def logging_message(self, message):
        for item in self.ObserverList:
            item("ConfigurationManager log-> "+message)

    def clear_communications_ports(self):
        """
        Removes all port configurations
        :return: None
        """
        self.configuration_content['communications']["ports"] = {}

    ### ^^^^^^^   Communications configuration  4/2018  working here end!!!!!!!!!!!!
    configuration_content = property(get_configuration_content, set_configuration_content)

if __name__ == '__main__':
    cm = ConfigurationManager()
    print ("python path ----"+sys.executable)
    this_script_path = os.path.realpath(__file__)
    this_script_path = os.path.dirname(this_script_path)
    print ("path ----" + this_script_path)
    file_path = os.path.join(this_script_path, 'SampleProject','configurations','tst1.txt')
    print ("file_path ----" + file_path)
    cm.set_configuration_file(file_path)
    #cm.set_files_config({"file1":{'engine':'default', 'selected_to_run': True, 'priority_level': 1,'helper_class': 'default'  }})

    item_list = cm.get_item_list()
    print(item_list)

    # files configuration
    cm.set_config_item('files', {"file2":{'engine':'default', 'selected_to_run': True, 'priority_level': 1,'helper_class': 'default'  }})
    cm.write_configuration_file()
    cm.read_configuration_file()

    # communications configuration
    cm.clear_communications_ports()
    result = cm.add_communications_port_id("0",{'type':'ethernet', 'IP' : '192.168.1.1', 'networkPort' : '502'})
    print("Adding port 0: "+ str(result))
    result = cm.add_communications_port_id("1",{'type':'serial', 'comport': 'COM1', 'baudrate': '57600'})
    print("Adding port 1: "+ str(result))

    cm.write_configuration_file()
    cm.read_configuration_file()
