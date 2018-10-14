# Abstract base class for the GUI
#
#
from abc import ABC, abstractmethod

class ViewBaseAbstract(ABC):

    #### Main window
    @abstractmethod
    def setProjectLabel(self, val):
        pass

    @abstractmethod
    def setConfigurationLabel(self, val):
        pass

    @abstractmethod
    def setStatusLabel(self, val):
        pass

    #### Menus
    @abstractmethod
    def setMenuFileExitCall(self, method):
        pass

    @abstractmethod
    def set_menu_project_new_call(self, method):
        pass

    @abstractmethod
    def set_menu_project_open_call(self, method):
        pass

    @abstractmethod
    def set_menu_project_save_call(self, method):
        pass

    @abstractmethod
    def set_menu_project_saveas_call(self, method):
        pass

    @abstractmethod
    def set_menu_project_close_call(self, method):
        pass

    @abstractmethod
    def set_menu_project_open_configuration_call(self, method):
        pass

    @abstractmethod
    def set_menu_project_save_configuration_call(self, method):
        pass

    @abstractmethod
    def set_menu_project_save_configuration_as_call(self, method):
        pass

    @abstractmethod
    def set_menu_about_about_call(self, method):
        pass

    @abstractmethod
    def set_menu_about_manual_call(self, method):
        pass


    #### Scripts Tab
    @abstractmethod
    def setTabScriptDebugButtonCall(self, method):
        pass

    @abstractmethod
    def setTabScriptEditButtonCall(self, method):
        pass

    @abstractmethod
    def setTabScriptTree(self, tree):
        pass

    #### Ports Tab
    @abstractmethod
    def setTabPortsAddButtonCall(self,method):
        pass

    @abstractmethod
    def setTabPortsEditButtonCall(self,method):
        pass

    @abstractmethod
    def setTabPortsRemoveButtonCall(self,method):
        pass

    @abstractmethod
    def setTabPortsListbox(self, lb):
        pass

    #### Plugins Tab
    @abstractmethod
    def setTabPluginsAddButtonCall(self,method):
        pass

    @abstractmethod
    def setTabPluginsRemoveButtonCall(self,method):
        pass

    @abstractmethod
    def setTabPluginsListbox(self, lb):
        pass

    #### Project Settings Tab
    @abstractmethod
    def setTabProjOpenDirectoryButtonCall(self,method):
        pass

    @abstractmethod
    def setTabProjShowConfSettingsButtonCall(self,method):
        pass

    @abstractmethod
    def setTabProjShowProjSettingsButtonCall(self,method):
        pass

    @abstractmethod
    def setTabProjSelectEditorButtonCall(self,method):
        pass

    @abstractmethod
    def setMessagingMethod(self, method):
        pass