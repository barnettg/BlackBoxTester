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
    #@abstractmethod
    #def setTabScriptDebugButtonCall(self, method):
    #    pass

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
    def setTabPortsListbox_available(self, lb):
        pass

    @abstractmethod
    def setTabPortsListbox_selected(self, lb):
        pass

    #### Plugins Tab
    @abstractmethod
    def setTabPluginsAddButtonCall(self,method):
        pass

    @abstractmethod
    def setTabPluginsRemoveButtonCall(self,method):
        pass

    @abstractmethod
    def setTabPluginsListbox_available(self, lb):
        pass

    @abstractmethod
    def setTabPluginsListbox_selected(self, lb):
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

    #@abstractmethod
    #def setTabProjSelectEditorButtonCall(self,method):
    #    pass

    #### Notifications tab
    @abstractmethod
    def set_tab_notifications_cb_email_enable(self, enable):
        pass

    @abstractmethod
    def get_tab_notifications_cb_email_enable(self):
        pass

    @abstractmethod
    def set_tab_notifications_cb_email_attach_report(self, enable):
        pass

    @abstractmethod
    def get_tab_notifications_cb_attach_report(self):
        pass

    @abstractmethod
    def set_tab_notifications_text_email_addresses(self, value):
        pass

    @abstractmethod
    def get_tab_notifications_text_email_addresses(self):
        pass

    @abstractmethod
    def set_tab_notifications_text_email_subject(self, value):
        pass

    @abstractmethod
    def get_tab_notifications_text_email_subject(self):
        pass

    @abstractmethod
    def set_tab_notifications_text_email_smpt_host(self, value):
        pass

    @abstractmethod
    def get_tab_notifications_text_email_smpt_host(self):
        pass

    @abstractmethod
    def set_tab_notifications_text_email_port(self, value):
        pass

    @abstractmethod
    def get_tab_notifications_text_email_port(self):
        pass

    @abstractmethod
    def set_tab_notifications_text_email_from_address(self, value):
        pass

    @abstractmethod
    def get_tab_notifications_text_email_from_address(self):
        pass

    @abstractmethod
    def set_tab_notifications_test_email_button_call(self, method):
        pass

    #texting ---
    @abstractmethod
    def set_tab_notifications_cb_texting_enable(self, value):
        pass

    @abstractmethod
    def get_tab_notifications_cb_texting_enable(self):
        pass

    @abstractmethod
    def set_tab_notifications_entry_texting_phonenumbers(self, value):
        pass

    @abstractmethod
    def get_tab_notifications_entry_texting_phonenumbers(self):
        pass

    @abstractmethod
    def set_tab_notifications_entry_texting_account_sid(self, value):
        pass

    @abstractmethod
    def get_tab_notifications_entry_texting_account_sid(self):
        pass

    @abstractmethod
    def set_tab_notifications_entry_texting_account_token(self, value):
        pass

    @abstractmethod
    def get_tab_notifications_entry_texting_account_token(self):
        pass

    @abstractmethod
    def set_tab_notifications_entry_texting_from_number(self, value):
        pass

    @abstractmethod
    def get_tab_notifications_entry_texting_from_number(self):
        pass

    @abstractmethod
    def set_tab_notifications_test_texting_button_call(self, method):
        pass

    #### passed tab
    @abstractmethod
    def set_tab_passed_list(self, lst):
        pass

    #### failed tab
    def set_tab_failed_list(self, lst):
        pass

    #### misc -----
    @abstractmethod
    def setMessagingMethod(self, method):
        pass