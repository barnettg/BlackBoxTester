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

# config file format
# files: { -- script data --}
# communications: { -- com setup --}
# misc: { -- email -- }
# GUI: {-- editor ---}


#to do:
#   docs for each method and class
#   method or class to make path names depending on OS
#   try to make crash
#   use forward slash in rel path names -> filename = os.path.join(dir, '/relative/path/to/file/you/want')
#   try on linux and mac
#   allow for configuration file to have other things
#      besides 'files', should also have communication ports, GUI settings, etc
#   remove all prints except in debugging_print

#>>> import os
#>>> import os.path
#>>> os.path.join(os.sep, 'home', 'user', 'work')
#'/home/user/work'
#>>> os.path.split('/usr/bin/python')
#('/usr/bin', 'python')

import json
import os.path
import ConfigurationManager
import sys
import importlib

class ScriptManager(object):
    def __init__(self, sys_model):
        self.project_path = ""
        self.scriptList=[]
        self.scripts_dict = {}
        self.system_model = sys_model
        self.configuration = ConfigurationManager.ConfigurationManager()

    def set_project_path(self, path):
        self.project_path  = path

    def read_configuration_file(self, config_filename):
        # config file format
        # 'files' : {
        # 'rel_filepath|filename' : {
        #           'engine' : 'path|engine_name' # or default for default based on extension
        #           'selected_to_run': 'True'
        #           'priority_level': '1'
        #           'helper_class': 'path|helpername'  # or default for default based on extension
        #           },
        #           ...
        #       }
        writeFlag = False
        #dir_path_and_filename = self.project_path + "\\configurations\\" + config_filename #
        dir_path_and_filename = os.path.join(self.project_path, 'configurations', config_filename)
        self.debugging_print("set configuration file to: " + dir_path_and_filename)
        self.debugging_print("self.configuration: " + str(self.configuration))
        self.configuration.set_configuration_file(dir_path_and_filename)

        self.scripts_dict['files'] = self.configuration.read_configuration_file()['files']
        self.debugging_print("self.scripts_dict['files']: " + str(self.scripts_dict['files']))
        # get list of all available and compare
        new_total = self.get_script_file_names()
        self.debugging_print("total of files: " + str(new_total))
        for item in new_total:
            if item not in list(self.scripts_dict['files'].keys()):
                writeFlag = True
                tempDic = {}
                tempDic['engine'] = 'default'
                tempDic['selected_to_run'] = 'True'
                tempDic['priority_level'] = 1
                tempDic['helper_class'] = 'default'
                self.scripts_dict['files'][item] = tempDic

        self.debugging_print("total of configuration files: " + str(self.scripts_dict['files']))

        for item in self.scripts_dict['files'] :
            if item not in new_total:
                writeFlag = True
                pass #remove the item from self.scripts_dict['files']

        if writeFlag == True:
            self.write_configuration_file(config_filename)

        self.debugging_print("Total scripts dictionary")
        self.debugging_print(str(self.scripts_dict))

    def write_configuration_file(self, config_filename):
        #dir_path_and_filename = self.project_path + "\\configurations\\"+config_filename
        dir_path_and_filename = os.path.join(self.project_path, 'configurations', 'config_filename')
        print('dir_path_and_filename: ' + dir_path_and_filename)
        self.configuration.write_configuration_file()
        #with open(dir_path_and_filename, 'w') as outfile:
        #    json.dump(self.scripts_dict, outfile, indent=4, sort_keys=True)

    def generate_script_list(self, level=10):
        " generate an alphabetized list of scripts enables to run and level enabled"
        self.scriptList=[]
        keys = self.scripts_dict['files'].keys()
        #keys.sort()
        for item in keys:
            if self.scripts_dict['files'][item]['selected_to_run'] \
                    and self.scripts_dict['files'][item]['priority_level'] <= level :
                self.scriptList.append(item)
        self.scriptList.sort() # alphabetize

    def add_script_to_configuration(self, script_name_to_add):
        tempDic = {}
        tempDic['engine'] = 'default'
        tempDic['selected_to_run'] = 'False'
        tempDic['priority_level'] = 10
        tempDic['helper_class'] = 'default'
        self.scripts_dict['files'][script_name_to_add] = tempDic

    def remove_script_from_configuration(self, script_name_to_remove):
        if script_name_to_remove in self.scripts_dict['files']:
            del self.scripts_dict['files'][script_name_to_remove]

    def run_scripts(self): # needs to be in thread
        for item in self.scriptList:
            # get engine and helper class:
            engine = self.scripts_dict['files'][item]['engine']
            helper = self.scripts_dict['files'][item]['helper_class']
            if helper == 'default':
                helper = 'HelperClassPy'
            __import__(helper)
            helper_class = getattr(sys.modules[helper], 'HelperClassPy')()
            if engine == 'default' :
                import PythonScriptEngine
                script_engine = PythonScriptEngine.PythonScriptEngine()
                path, name = os.path.split(item)
                path = os.path.join(os.sep,self.project_path,path)
                self.debugging_print("Run Script:")
                self.debugging_print(path + "  " + name + " with helper: " + helper)
                passed, message = script_engine.execute_script(path, name, helper_class) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.debugging_print("passed: " + str(passed))
                self.debugging_print("message: " + message)
            else:
                pass

    def run_single_script(self, rel_script_name):
        pass

    def set_script_engine(self, rel_script_name, script_engine_relative_path_and_name):
        if rel_script_name in self.scripts_dict['files']:
            self.scripts_dict['files'][rel_script_name]['engine'] = script_engine_relative_path_and_name
            return True
        return False

    def set_script_helper(self, rel_script_name, helper_relative_path_and_name):
        if rel_script_name in self.scripts_dict['files']:
            self.scripts_dict['files'][rel_script_name]['helper_class'] = helper_relative_path_and_name
            return True
        return False

    def set_script_priority(self, rel_script_name, level):
        if rel_script_name in self.scripts_dict['files']:
            self.scripts_dict['files'][rel_script_name]['priority_level'] = level
            return True
        return False

    def set_script_selection(self, rel_script_name, selection):
        if rel_script_name in self.scripts_dict['files']:
            self.scripts_dict['files'][rel_script_name]['selected_to_run'] = selection
            return True
        return False

    def get_script_engine(self, rel_script_name):
        if rel_script_name in self.scripts_dict['files']:
            return self.scripts_dict['files'][rel_script_name]['engine']
        return None

    def get_script_helper(self, rel_script_name):
        if rel_script_name in self.scripts_dict['files']:
            return self.scripts_dict['files'][rel_script_name]['helper_class']
        return None

    def get_script_priority(self, rel_script_name):
        if rel_script_name in self.scripts_dict['files']:
            return self.scripts_dict['files'][rel_script_name]['priority_level']
        return None

    def get_script_selection(self, rel_script_name):
        if rel_script_name in self.scripts_dict['files']:
            return self.scripts_dict['files'][rel_script_name]['selected_to_run']
        return None

    def get_scripts(self):
        "return an alphabetized list of available scripts"
        keys = list(self.scripts_dict['files'].keys())
        keys.sort()
        self.debugging_print("get_scripts----" + str(keys))
        return keys

    def get_script_file_names(self):
        "return an alphabetized list of scripts in the script directories"
        returnList= []
        self.debugging_print("Method: get_script_file_names")
        filesDic = {}
        #files_path = self.project_path + r'\scripts'
        files_path = os.path.join(self.project_path, 'scripts')
        #get directories
        dirsList = os.listdir(files_path)
        self.debugging_print(str(dirsList))
        for item in dirsList:
            if os.path.isdir(os.path.join(files_path,item)):
                self.debugging_print("found directory: " + str(item))
                #relpath =  'scripts\\' + item
                relpath = os.path.join('scripts', item)
                filesList = os.listdir(os.path.join(files_path,item))
                self.debugging_print(str(filesList))
                for file_item in filesList:
                    # check if a file then add to dictionary
                    #if os.path.isfile(self.project_path+"\\"+relpath+"\\"+file_item):
                    if os.path.isfile(os.path.join(self.project_path, relpath, file_item)):
                        returnList.append(relpath+"\\" + file_item)

        returnList.sort()
        return returnList


    def debugging_print(self, message):
        " print out messages during development"
        if __name__ == '__main__':
            print("ScriptManager---"+message)


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
    print ("python path ----"+sys.executable)
    this_script_path = os.path.realpath(__file__)
    this_script_path = os.path.dirname(this_script_path)
    print ("path ----" + this_script_path)
    file_path = os.path.join(this_script_path, 'SampleProject')
    print ("file_path ----" + file_path)

    sm.set_project_path(file_path)
    print("Available files:" + str(sm.get_script_file_names()))
    sm.read_configuration_file("configFiles3.txt")
    sm.generate_script_list(level=10)

    sm.run_scripts()
    # wait until thread done????????????????????


    print("sm.get_scripts: " + str(sm.get_scripts()))
    script_name = sm.get_scripts()[0]
    sm.remove_script_from_configuration(script_name)
    if script_name in sm.get_scripts():
        print("FAIL to remove " + script_name )
    else:
        print("removed " + script_name )
    sm.add_script_to_configuration(script_name)

    if not sm.set_script_engine(script_name, 'script_engine_relative_path_and_name'):
        print("FAIL to set engine ")
    if not sm.set_script_helper(script_name, 'helper_relative_path_and_name'):
        print("FAIL to set helper ")
    if not sm.set_script_priority(script_name, 5):
        print("FAIL to set level ")
    if not sm.set_script_selection(script_name, 'True'):
        print("FAIL to set selection ")
    if sm.get_script_engine(script_name) != 'script_engine_relative_path_and_name':
        print("FAIL to compare engine ")
    if sm.get_script_helper(script_name) != 'helper_relative_path_and_name':
        print("FAIL to compare engine ")
    if sm.get_script_priority(script_name) != 5:
        print("FAIL to compare priority ")
    if sm.get_script_selection(script_name) != 'True':
        print("FAIL to compare selection ")

    #sm.add_script_to_script_list(["name1", "path1", "engine1", "level1", "False", "helper1"])
    #sm.write_configuration_file()

    # def read_configuration_file(self, config_filename):
        # # config file format
        # # 'files' : {
        # # 'rel_filepath|filename' : {
        # #           'engine' : 'path|engine_name' # or default for default based on extension
        # #           'selected_to_run': 'True'
        # #           'priority_level': '1'
        # #           'helper_class': 'path|helpername'  # or default for default based on extension
        # #           },
        # #           ...
        # #       }
        # dir_path_and_filename = self.project_path + "\\configurations\\" + config_filename #
        # #if file exists then read-- otherwise create
        # if os.path.isfile(dir_path_and_filename):
        #     self.debugging_print("found configuration file at: " + dir_path_and_filename)
        #     with open(dir_path_and_filename) as json_file:
        #         self.scripts_dict = json.load(json_file)
        #     self.debugging_print("Total scripts dictionary")
        #     self.debugging_print(str(self.scripts_dict))
        # else:
        #     self.debugging_print("did not find configuration file at: " + dir_path_and_filename)
        #     filesDic = {}
        #     self.scripts_dict['files'] = {}
        #     files_path = self.project_path + r'\scripts'
        #     #get directories
        #     dirsList = os.listdir(files_path)
        #     self.debugging_print(str(dirsList))
        #     for item in dirsList:
        #         if os.path.isdir(os.path.join(files_path,item)):
        #             self.debugging_print("found directory: " + str(item))
        #             relpath =  'scripts\\' + item
        #             filesList = os.listdir(os.path.join(files_path,item))
        #             self.debugging_print(str(filesList))
        #             for file_item in filesList:
        #                 # check if a file then add to dictionary
        #                 if os.path.isfile(self.project_path+"\\"+relpath+"\\"+file_item):
        #                     tempDictKey = relpath+"\\"+file_item
        #                     tempDic = {}
        #                     tempDic['engine'] = 'default'
        #                     tempDic['selected_to_run'] = 'True'
        #                     tempDic['priority_level'] = 1
        #                     tempDic['helper_class'] = 'default'
        #                     self.scripts_dict['files'][tempDictKey] = tempDic
        #
        #             #self.debugging_print("incremental scripts dictionary")
        #             #self.debugging_print(str(self.scripts_dict))
        #         else:
        #             self.debugging_print("not a directory: " + str(item))
        #
        #     self.debugging_print("Total scripts dictionary")
        #     self.debugging_print(str(self.scripts_dict))
        #     self.write_configuration_file(config_filename)
        #
        # #http://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
        # #for p in data['people']:
        # #    print('Name: ' + p['name'])
        # #    print('Website: ' + p['website'])
        # #    print('From: ' + p['from'])
        # #   print('')

            #http://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
        #for p in data['people']:
        #    print('Name: ' + p['name'])
        #    print('Website: ' + p['website'])
        #    print('From: ' + p['from'])
        #   print('')