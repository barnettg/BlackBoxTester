
import ScriptManager
import HelperClassPy
import ConfigurationManager
import LogManager
import CommunicationsManager

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

        self.setup_last_known_project_configuration()

    def setup_last_known_project_configuration(self):
        pass

    def create_new_project(self):
        pass

    def create_new_project_configuration(self):
        pass

    def copy_existing_project_configuration_to_new_config(self):
        pass

    def copy_existing_project_to_new(self):
        pass




if __name__ == '__main__':
    class ControllerDummy(object):
        pass

    cd = ControllerDummy()
    model = Model(cd)