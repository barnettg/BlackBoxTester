
import ScriptManager
import HelperClassPy
import ConfigurationManager
import LogManager
import CommunicationsManager
import os
import json
import os.path
import sys
import shutil
import pprint

class Model():

    def __init__(self, cntrlr):
        self.controller = cntrlr
        self.script_manager = ScriptManager.ScriptManager()
        self.helper_class = HelperClassPy.HelperClassPy()
        self.configuration_manager = ConfigurationManager.ConfigurationManager()
        self.logging_manager = LogManager.LogManager()
        self.communications_manager = CommunicationsManager.CommunicationsManager()

        # pass pointers to helper class
        self.helper_class.model = self
        self.helper_class.communications = self.communications_manager
        self.helper_class.configuration = self.configuration_manager
        self.helper_class.controller = self.controller
        self.helper_class.logging = self.logging_manager

        #self.setup_last_known_project_configuration()
        self.revision_major = 0
        self.revision_minor = 0
        self.revision_build = 0

        self.project_directory = None
        self.project_configuration = None
        self.bbt_configuration_content = {}
        self.bbt_configuration_content['current project'] = None  # project path
        self.bbt_configuration_content['current project config'] = None  # config file name
        self.bbt_configuration_content['configurations history'] = [ ]  # list of dictionaries
        self.history_size = 10
        self.bbt_configuration_content['history size'] = self.history_size

    # --------- project/configuration -------------
    def initialize(self):
        results = self.read_bbt_configuration()

    def open_project(self, proj_path):
        # set the project directory
        if os.path.exists(proj_path):
            if self.verify_project_structure(proj_path):
                print("open project dir: " + proj_path)
                self.project_directory = proj_path
                self.bbt_configuration_content['current project'] = self.project_directory
                self.set_helper_project_directory()
                # do something to manager classes ?????? !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                return True
        return False

    def verify_project_structure(self, proj_path):
            directories = ["configurations", "lib", "logs",  "plugins", "scripts", "userfiles"]
            for item in directories:
                x_dir = os.path.join(proj_path, "configurations")
                if not os.path.exists(x_dir):
                    return False
            return True

    def open_project_config(self, config_name):
        # set the project directory
        total_path = os.path.join(self.project_directory, "configurations", config_name)
        if os.path.isfile(total_path):
            print("configuration found: " + os.path.basename(total_path))
            self.project_configuration = config_name
            self.bbt_configuration_content['current project config'] = self.project_configuration
            self.add_to_history()
            # do something with new info ?????? !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return True
        return False

    def add_to_history(self):
        # if self.project_directory  and self.project_configuration not in history then add
        # to  self.bbt_configuration_content['configurations history']
        # if history too big then pop off one
        found = False
        for item in self.bbt_configuration_content['configurations history']:
            if item['project path'] == self.project_directory and \
                            item['config file name'] == self.project_configuration:
                found = True
        if not found:
            temp_dict = {'project path': self.project_directory,'config file name': self.project_configuration}
            self.bbt_configuration_content['configurations history'].append(temp_dict)
            size = len(self.bbt_configuration_content['configurations history'])
            if self.history_size < 0:
                self.history_size = 0
            while size > self.history_size:
                self.bbt_configuration_content['configurations history'].pop(0)
                size = len(self.bbt_configuration_content['configurations history'])

    def create_new_project(self, proj_path, proj_name):
        if os.path.isdir(proj_path):
            p_dir = os.path.join(proj_path, proj_name)
            if not os.path.exists(p_dir):
                os.makedirs(p_dir)
            new_path = os.path.join(proj_path, proj_name)
            # create directory configurations
            conf_dir = os.path.join(new_path, "configurations")
            if not os.path.exists(conf_dir):
                print("make dir " + conf_dir)
                os.makedirs(conf_dir)
            # create directory lib
            lib_dir = os.path.join(new_path, "lib")
            if not os.path.exists(lib_dir):
                print("make dir " + lib_dir)
                os.makedirs(lib_dir)
            # create directory logs
            logs_dir = os.path.join(new_path, "logs")
            if not os.path.exists(logs_dir):
                print("make dir " + logs_dir)
                os.makedirs(logs_dir)
            # create directory plugins
            plugins_dir = os.path.join(new_path, "plugins")
            if not os.path.exists(plugins_dir):
                print("make dir " + plugins_dir)
                os.makedirs(plugins_dir)
            # create directory scripts
            scripts_dir = os.path.join(new_path, "scripts")
            if not os.path.exists(scripts_dir):
                print("make dir " + scripts_dir)
                os.makedirs(scripts_dir)
            # create directory userfiles
            userfiles_dir = os.path.join(new_path, "userfiles")
            if not os.path.exists(userfiles_dir):
                print("make dir " + userfiles_dir)
                os.makedirs(userfiles_dir)

        else:
            return "Error", "Path does not exist"

    def create_new_project_configuration(self, file_name):
        raise ValueError('create_new_project_configuration not completed')

    def copy_existing_project_configuration_to_new_config(self, src_file_name, dst_file_name):
        src = self.project_directory + os.sep + "configurations"+ os.sep + src_file_name
        if os.path.isfile(src):
            dst = self.project_directory + os.sep + "configurations"+ os.sep + dst_file_name
            try:
                shutil.copyfile(src,dst)
            except:
                print("ERROR: Model::copy_existing_project_configuration_to_new_config")
                return False
        return True

    def copy_existing_project_to_new(self, directory_for_existing_project, directory_for_new_project, overwrite=False):
        src = directory_for_existing_project
        dst = directory_for_new_project
        if os.path.isdir(src):
            if os.path.isdir(dst) and overwrite:
                shutil.rmtree(dst) # remove existing empty directory before using shutil.copytree

            if (os.path.isdir(dst) and overwrite) or (not os.path.isdir(dst)):
                try:
                    shutil.copytree(src, dst)
                except:
                    print("ERROR: Model::copy_existing_project_to_new")
                    return False
            return True
        return False

    def check_project_validity(self):
        raise ValueError('check_project_validity not completed')

    def get_history_of_projects(self):
        return self.bbt_configuration_content['configurations history']

    def verify_available_ports(self):
        # get ports used in configuration
        # get available ports
        # verify ports used are available
        raise ValueError('verify_available_ports not completed')

    def set_helper_project_directory(self):
         self.helper_class.project_directory = self.project_directory

    # ------------- Black Box tester configuration -----------
    def read_bbt_configuration(self):
        # file format
        # 'current project' : '' , # project path
        # 'current project config' : '', # config file name
        # 'configurations history' : [ { 'project path' : '' , 'config file name' : '' } ... {} ] list of dictionaries
        # 'history size' : 10
        #
        # check for file bbt_config.txt
        total_path = os.path.join(os.getcwd(), "bbt_config.txt")
        if os.path.isfile(total_path):
            with open(total_path) as json_file:
                self.bbt_configuration_content = json.load(json_file)
                #print(str(self.bbt_configuration_content))
            if 'current project' in self.bbt_configuration_content:
                if self.open_project( self.bbt_configuration_content['current project']):
                    if 'current project config' in self.bbt_configuration_content:
                        self.open_project_config(self.bbt_configuration_content['current project config'])
            if 'history size' in self.bbt_configuration_content:
                self.history_size= self.bbt_configuration_content['history size']
            return self.bbt_configuration_content

    def save_bbt_configuration(self):
        total_path = os.path.join(os.getcwd(), "bbt_config.txt")
        with open(total_path, 'w') as outfile:
            json.dump(self.bbt_configuration_content, outfile, indent=4, sort_keys=True)

    # ------------- script  configuration -----------
    def get_estimated_configuration_runtime(self, config_name):
        raise ValueError('get_estimated_configuration_runtime not completed')

    # ---------- logging ----------------------
    def register_logging_manager_as_observer(self):
        raise ValueError('register_logging_manager not completed')

    # ---------- communications -----------------
    def register_with_communications_as_observer(self):
        raise ValueError('register_with_communications_as_observer not completed')

    def set_communications_configurations(self):
        raise ValueError('set_communications_configurations not completed')

    # ---------- scripts -----------------
    def run_scripts(self):
        raise ValueError('run_scripts not completed')

    def run_single_script_in_debug(self):
        raise ValueError('run_scripts not completed')

    def pause_scripts(self):
        raise ValueError('pause_scripts not completed')

    def stop_scripts(self):
        raise ValueError('stop_scripts not completed')

    def step_script_in_debug(self):
        raise ValueError('stop_scripts not completed')

    def restart_script_in_debug(self):
        raise ValueError('restart_script_in_debug not completed')

    def skip_to_final_in_currently_running_script(self):
        raise ValueError('skip_to_final_in_currently_running_script not completed')

    def set_script_running_time_max(self):
        raise ValueError('set_script_running_time_max not completed')

    def get_script_running_time_max(self):
        raise ValueError('get_script_running_time_max not completed')

    def set_script_configurations(self):
        raise ValueError('set_script_configurations not completed')

    # ---------- notifications -----------------
    def configure_email_notification(self):
        raise ValueError('configure_email_notification not completed')

    def configure_text_notification(self):
        raise ValueError('configure_text_notification not completed')

    # ---------- results -----------------
    def register_for_script_observer(self):
        raise ValueError('register_for_script_observer not completed')



if __name__ == '__main__':
    class ControllerDummy(object):
        pass

    cd = ControllerDummy()
    model = Model(cd)
    model.project_directory = "one"
    model.project_configuration = "one_conf"
    model.add_to_history()
    model.project_directory = "two"
    model.project_configuration = "two_conf"
    model.add_to_history()
    model.project_directory = "three"
    model.project_configuration = "three_conf"
    model.add_to_history()
    model.project_directory = "four"
    model.project_configuration = "four_conf"
    model.add_to_history()
    print(str(model.bbt_configuration_content['configurations history']))
    model.project_directory = "five"
    model.project_configuration = "five_conf"
    model.history_size = 2
    model.add_to_history()
    print(str(model.bbt_configuration_content['configurations history']))

    new_proj_path = "C:" + os.sep + "Users" + os.sep + "glen" + os.sep + "Documents" + os.sep + "TempBBtester"
    model.create_new_project(new_proj_path, "new_Project")
    # create project configuration
    project_name = "new_Project"
    src = os.getcwd() + os.sep +"SampleProject" + os.sep + "configurations"+ os.sep + "configFiles3.txt"
    dst = new_proj_path +os.sep + project_name + os.sep + "configurations"+ os.sep + "configFiles3.txt"
    print(os.path.isfile(src))
    shutil.copyfile(src,dst)

    # create dummy test scripts
    src = os.getcwd() + os.sep +"SampleProject" + os.sep + "scripts"
    dst = new_proj_path +os.sep + project_name + os.sep + "scripts"
    shutil.rmtree(dst)  # remove existing empty directory before using shutil.copytree
    shutil.copytree(src, dst)

    # open project
    result = model.open_project(new_proj_path +os.sep + project_name)
    print("opened a project: " + str(result))

    # open project configuration
    config_name = "configFiles3.txt"
    result = model.open_project_config(config_name)
    print("opened a project configuration: " + str(result))

    # save black box tester configuration
    result = model.save_bbt_configuration()
    print("save black box tester configuration: " + str(result))

    # read Black box tester configuration
    result = model.read_bbt_configuration()
    #print("read Black box tester configuration: " + str(result))
    pprint.pprint(result)

    # restart model and verify opens last project/configuration