# Handles reading and writing configurations
# assumes proper directory structure but also check

import json
import os.path

# config file format
# 'files' : { -- script data --
#       }
# 'communications' : { -- com setup --
#       }
# 'misc' : { -- email --
#       }
# 'GUI' : { -- editor ---
#       }

class ConfigurationManager(object):
    def __init__(self):
        self.configuration_file = None
        self.configuration_content = {}

    def set_configuration_file(self, path):
        self.configuration_file = path # project_path + "\\configurations\\" + config_filename #

    def read_configuration_file(self, config_filename = None):
        if config_filename == None :
            config_filename = self.configuration_file

        dir_path_and_filename = self.configuration_file #project_path + "\\configurations\\" + config_filename #
        #if file exists then read-- otherwise create
        if os.path.isfile(dir_path_and_filename):
            self.debugging_print("found configuration file at: " + dir_path_and_filename)
            with open(dir_path_and_filename) as json_file:
                self.configuration_content = json.load(json_file)
            self.debugging_print("Total scripts dictionary")
            self.debugging_print(str(self.configuration_content))
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

    def write_configuration_file(self, config_filename = None):
        if config_filename == None :
            config_filename = self.configuration_file

        dir_path_and_filename = config_filename #project_path + "\\configurations\\"+config_filename
        self.debugging_print('dir_path_and_filename: ' + dir_path_and_filename)
        with open(dir_path_and_filename, 'w') as outfile:
            json.dump(self.configuration_content, outfile, indent=4, sort_keys=True)

    def debugging_print(self, message):
        " print out messages during development"
        if __name__ == '__main__':
            print(message)

    def get_files_config(self):
        return self.configuration_content.get('files',default = {})

    def set_files_config(self, files_content):
        self.debugging_print("set files: " +str(files_content))
        self.configuration_content['files'] = files_content
        self.debugging_print("all: " +str(self.configuration_content))

    def get_communications_config(self):
        return self.configuration_content.get('communications',default = {})

    def set_communications_config(self, communications_content):
        self.configuration_content['communications'] = communications_content

    def get_misc_config(self):
        return self.configuration_content.get('misc',default = {})

    def set_misc_config(self, misc_content):
        self.configuration_content['misc'] = misc_content

    def get_GUI_config(self):
        return self.configuration_content.get('GUI',default = {})

    def set_GUI_config(self, GUI_content):
        self.configuration_content['GUI'] = GUI_content

if __name__ == '__main__':
    cm = ConfigurationManager()
    cm.set_configuration_file(r'C:\Users\glen\Documents\Projects\CoherentPythonProjects\PythonVersion\BlackBoxTester\SampleProject\configurations\tst1.txt')
    cm.set_files_config({"file1":{'engine':'default', 'selected_to_run': True, 'priority_level': 1,'helper_class': 'default'  }})
    cm.write_configuration_file()
    cm.read_configuration_file()
