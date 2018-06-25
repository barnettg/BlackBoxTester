
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

# to do:
# add close project - just undo project configuration and remove
# #     project/project configuration from current project in BBtester config file


class Model():
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

    def __init__(self, cntrlr):
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
        self.controller = cntrlr
        self.helper_class = HelperClassPy.HelperClassPy()
        self.configuration_manager = ConfigurationManager.ConfigurationManager()
        self.script_manager = ScriptManager.ScriptManager(self.configuration_manager)
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
                self.script_manager.set_project_path(self.project_directory)
                return True
        return False

    def close_project(self):
        self.project_directory = None
        self.project_configuration = None
        self.bbt_configuration_content['current project'] = None  # project path
        self.bbt_configuration_content['current project config'] = None  # config file name
        self.set_helper_project_directory()
        self.configuration_manager.empty_configuration()
        self.script_manager.set_project_path("")
        self.communications_manager.disconnect_all() # close communications

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
            # send to configuration manager to open
            self.configuration_manager.read_configuration_file(total_path)
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
            self.project_directory = new_path
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
            # set up managers for a new project !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.set_helper_project_directory()
            self.script_manager.set_project_path(self.project_directory)

        else:
            return False, "Path does not exist"

    def create_new_project_configuration(self, file_name):
        total_file_name = os.path.join(self.project_directory, "configurations", file_name )
        self.configuration_manager.set_configuration_file(total_file_name)
        self.configuration_manager.read_configuration_file(total_file_name)

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
        config_specified_ports = self.configuration_manager.get_communications_port_id_list()

        # get available ports
        avail_serial_ports = self.communications_manager.get_available_serial_ports()
        # verify ports used are available
        for item in config_specified_ports:
            port_with_specific_id = self.configuration_manager.get_communications_port_id_info(item)
            if 'type' in port_with_specific_id:
                if port_with_specific_id['type']=='serial':
                    if 'comport' in port_with_specific_id:
                        com_prt = port_with_specific_id['comport']
                        if com_prt not in avail_serial_ports:
                            return False, "Serial port " + com_prt + " not available"


        return True , "All project specified serial ports are available"

    def get_available_serial_ports(self):
        return self.communications_manager.get_available_serial_ports()

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


    #----------- project configuration -------
    def project_configuration_add_serial_port_id(self, identification: str,
                                                 comport: str,
                                                 baud: str,
                                                 parity='none',
                                                 stop=1 ) -> bool:

        temp_dictionary = {'type':'serial', 'comport': comport, 'baudrate': baud, 'parity': parity, 'stopbits': stop }
        return self.configuration_manager.add_communications_port_id(identification, temp_dictionary )

    def project_configuration_add_network_port_id(self, identification: str,
                                                 ip: str,
                                                 network_port: str,
                                                  ) -> bool:
        temp_dictionary = {'type':'ethernet', 'IP': ip, 'networkPort': network_port }
        return self.configuration_manager.add_communications_port_id(identification, temp_dictionary )

    def save_configuration(self):
        self.configuration_manager.write_configuration_file()  # writes default

    # ---------- scripts -----------------
    def create_new_script(self, group_name, file_name, contents):
        self.script_manager.set_project_path(self.project_directory)
        self.script_manager.create_new_script(group_name, file_name, contents)

    def run_scripts(self, level):
        print("model ->run script ")
        self.script_manager.generate_script_list(level)
        self.script_manager.run_scripts()

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

    def set_script_configurations(self, rel_script_name, **kwargs):
        if 'engine' in kwargs:
            self.script_manager.set_script_engine(rel_script_name, kwargs['engine'])
        if 'helper_class' in kwargs:
            self.script_manager.set_script_helper(rel_script_name, kwargs['helper_class'])
        if 'priority_level' in kwargs:
            self.script_manager.set_script_priority(rel_script_name, kwargs['priority_level'])
        if 'selected_to_run' in kwargs:
            self.script_manager.set_script_selection(rel_script_name, kwargs['selected_to_run'])

    def add_script_to_configuration(self, script_name_to_add):
        self.script_manager.add_script_to_configuration(script_name_to_add)

    # ---------- notifications -----------------
    def configure_email_notification(self):
        raise ValueError('configure_email_notification not completed')

    def configure_text_notification(self):
        raise ValueError('configure_text_notification not completed')

    # ---------- results -----------------
    def register_for_script_observer(self, method=None):
        if method:
            self.script_manager.registerObserver(method)
        else:
            self.script_manager.registerObserver(self.scriptManager_message_observer_method)

    def register_for_script_log(self, method=None):
        if method:
            self.script_manager.register_log(method)
        else:
            self.script_manager.register_log(self.scriptManager_log_observer_method)

    def scriptManager_message_observer_method(self, **kwargs):
        print("model->script Manager->notify " + str(kwargs))

    def scriptManager_log_observer_method(self, message):
        print("model->script Manager->log " + message)

    def register_for_helperclass_log_observer(self, method=None):
        if method:
            self.helper_class.log_message_register(method)
        else:
            self.helper_class.log_message_register(self.helperclass_log_observer_method)

    def helperclass_log_observer_method(self, log):
        print("model->helperclass->log  " + log)

    def register_for_helperclass_message_observer(self, method=None):
        if method:
            self.helper_class.log_message_register(method)
        else:
            self.helper_class.log_message_register(self.helperclass_message_observer_method)

    def helperclass_message_observer_method(self, message):
        print("model->helperclass->message " + message)

    def register_for_communicationsManager_observer(self, method=None):
        if method:
            self.communications_manager.register_log(method)
        else:
            self.communications_manager.register_log(self.communicationsManager_log_observer_method)

    def register_for_configurationManager_observer(self, method=None):
        if method:
            self.configuration_manager.register_log(method)
        else:
            self.configuration_manager.register_log(self.configurationManager_log_observer_method)


    def communicationsManager_log_observer_method(self, log):
        print("model->communications Manager->log " + log)

    def configurationManager_log_observer_method(self, log):
        print("model->configuration Manager->log " + log)



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