# Handles running python scripts
# assumes proper directory structure but also check

# Keep list of scripts
#       location
#       type (python etc.)
#       priority level
#       selected to run
#       execution time
# run selected scripts
# run single script
# debug single script
#   reset, stop, step, run to break, set break, monitor variables
# send helper class to script to run
#   dynamically get a helper class
# record execution times
# dynamically get script engine

# directory structure

# project_path
#       scripts
#               group_1
#               ...
#               group_n
#       userfiles
#       configurations
#       libraries
#       logs
#       plugins

import json

class ScriptManager(object):
    def __init__(self, sys_model):
        self.project_path = ""
        self.scripts_dict = {}
        self.script_list = []
        self.scripts_dict["scripts"] = self.script_list
        self.system_model = sys_model

    def set_project_path(self, path):
        self.project_path  = path

    def read_configuration_file(self):
        dir_path_and_filename = self.project_path + r'\configurations\scriptsConfig.txt'
        with open(dir_path_and_filename) as json_file:
            data = json.load(json_file)
        #http://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
        #for p in data['people']:
        #    print('Name: ' + p['name'])
        #    print('Website: ' + p['website'])
        #    print('From: ' + p['from'])
        #   print('')

    def write_configuration_file(self):
        dir_path_and_filename = self.project_path + r'\configurations\scriptsConfig.txt'
        print('dir_path_and_filename: ' + dir_path_and_filename)
        with open(dir_path_and_filename, 'w') as outfile:
            json.dump(self.scripts_dict, outfile)

    def generate_script_list(self):
        pass

    def add_script_to_script_list(self, script_property):
        self.script_list.append(script_property)

    def remove_script_from_script_list(self, script_name_to_remove):
        pass

    def run_scripts(self):
        pass

    def run_single_script(self, script_name):
        pass

    def set_script_engine(self, script_name, script_path, script_engine_relative_path_and_name):
        pass

    def set_script_helper(self, script_name, script_path, helper_relative_path_and_name):
        pass

    def set_script_priority(self, script_name, script_path, level):
        pass

    def set_script_selection(self, script_name, script_path, selection):
        pass


class ScriptProperties(object):
    def __int__(self):
        self.script_name = ""
        self.script_path = ""  # relative to project directory
        self.script_engine = "default"
        self.script_priority_level = 1
        self.script_selected = False
        self.script_helper_class = "default"

class ModelDummy(object):
    pass


if __name__ == '__main__':
    dummy = ModelDummy()
    sm = ScriptManager(dummy)
    sm.set_project_path(
        r'C:\Users\glen\Documents\Projects\CoherentPythonProjects\PythonVersion\BlackBoxTester\SampleProject')
    s1 = ScriptProperties()
    s1.script_name = "Hello.py"
    sm.add_script_to_script_list(["name1", "path1", "engine1", "level1", "False", "helper1"])
    sm.write_configuration_file()