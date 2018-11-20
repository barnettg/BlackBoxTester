# test for the BlackBoxTesterView class
import sys
sys.path.append('..')
import BlackBoxTesterView

print("Python Version {}.{}".format(sys.version_info[0],sys.version_info[1]))

available_addin_list = ["line 1", "line 2","line 3", "line 4","line 5", "line 6", "line 7"]
selected_addin_list = ["line 1", "line 2","line 3", "line 4"]

available_ports_list = ["COM1", "COM2", "COM3"]
selected_ports_list = ["COM1 9600 8N1", "10.12.34.56 port:23","COM2 9600 8N1", "10.12.34.56 port:24","COM3 9600 8N1", "10.12.34.56 port:25"]

def scriptTab_debugCallback():
    print("scriptTab_debugCallback got a call")

def scriptTab_editCallback():
    print("scriptTab_editCallback got a call")

def communicationsTab_addCallback():
    print("communicationsTab_addCallback got a call")

def communicationsTab_removeCallback():
    print("communicationsTab_removeCallback got a call")

def communicationsTab_editCallback():
    print("communicationsTab_editCallback got a call")

def pluginsTab_addCallback():
    print("pluginsTab_addCallback got a call")

def pluginsTab_removeCallback():
    print("pluginsTab_removeCallback got a call")

def projSetTab_openDirCallback():
    print("projSetTab_openDirCallback got a call")

def projSetTab_showConfSettingsCallback():
    print("projSetTab_showConfSettingsCallback got a call")

def projSetTab_showProjSettingsCallback():
    print("projSetTab_showProjSettingsCallback got a call")

def projSetTab_selectEditorCallback():
    print("projSetTab_selectEditorCallback got a call")


def viewMessages(val):
    print(val)

#### menus
def menuFileExit():
    print("Menu File Exit got a call")

def menu_project_new():
    print("menu_project_new got a call")

def menu_project_open():
    print("menu_project_open got a call")

def menu_project_save():
    print("menu_project_save got a call")

def menu_project_saveas():
    print("menu_project_saveas got a call")

def menu_project_close():
    print("menu_project_close got a call")

def menu_project_open_configuration():
    print("menu_project_open_configuration got a call")

def menu_project_save_configuration():
    print("menu_project_save_configuration got a call")

def menu_project_save_configuration_as():
    print("menu_project_save_configuration_as got a call")

def menu_about_about():
    print("menu_about_about got a call")

def menu_about_manual():
    print("menu_about_manual got a call")

def method_for_email_test():
    print("email test")

def method_for_texting_test():
    print("texting test")
#main window --------------------------------------
view = BlackBoxTesterView.View()
view.setConfigurationLabel("This sets the configuration label")
view.setProjectLabel("This sets the project label")
view.setStatusLabel("This sets the status label")


#TAB scripts ----------------------------
#view.setTabScriptDebugButtonCall(scriptTab_debugCallback) # removed
view.setTabScriptEditButtonCall(scriptTab_editCallback)
# ------ > need to load scripts in list view !!!!!!!!!!!!!

#TAB ports ----------------------------
view.setTabPortsAddButtonCall(communicationsTab_addCallback)
view.setTabPortsEditButtonCall(communicationsTab_editCallback)
view.setTabPortsRemoveButtonCall(communicationsTab_removeCallback)

#available_ports_list = ["COM1", "COM2", "COM3"]
#selected_ports_list = ["COM1 9600 8N1", "10.12.34.56 port:23"]
view.setTabPortsListbox_available(available_ports_list)
view.setTabPortsListbox_selected(selected_ports_list)
view.setTabPortsListbox_selected(selected_ports_list)

#TAB plugins----------------------------
view.setTabPluginsAddButtonCall(pluginsTab_addCallback)
view.setTabPluginsRemoveButtonCall (pluginsTab_removeCallback)
view.setTabPluginsListbox_available(available_addin_list)
view.setTabPluginsListbox_selected(selected_addin_list)

#TAB projects ----------------------------
view.setTabProjOpenDirectoryButtonCall(projSetTab_openDirCallback)
#view.setTabProjSelectEditorButtonCall(projSetTab_selectEditorCallback) # removed
view.setTabProjShowConfSettingsButtonCall(projSetTab_showConfSettingsCallback)
view.setTabProjShowProjSettingsButtonCall(projSetTab_showProjSettingsCallback)

#TAB pnotifications ----------------------------
#email ---
view.set_tab_notifications_cb_email_enable(True)
result = view.get_tab_notifications_cb_email_enable()
print("email tab: cb_email_enable- " + str(result))

view.set_tab_notifications_cb_email_attach_report(True)
result = view.get_tab_notifications_cb_attach_report()
print("email tab: _cb_email_attach_report- " + str(result))

view.set_tab_notifications_text_email_addresses("address1@yahoo.com")
result = view.get_tab_notifications_text_email_addresses()
print("email tab: text_email_addresses- " + str(result))

view.set_tab_notifications_text_email_subject("test results")
result = view.get_tab_notifications_text_email_subject()
print("email tab: text_email_subject- " + str(result))

view.set_tab_notifications_text_email_smpt_host("smpt host")
result = view.get_tab_notifications_text_email_smpt_host()
print("email tab: text_email_smpt_host- " + str(result))

view.set_tab_notifications_text_email_port("email port")
result = view.get_tab_notifications_text_email_port()
print("email tab: text_email_portt- " + str(result))

view.set_tab_notifications_text_email_from_address("from1@yahoo.com")
result = view.get_tab_notifications_text_email_from_address()
print("email tab: text_email_from_address- " + str(result))

view.set_tab_notifications_test_email_button_call(method_for_email_test)

#texting ---
view.set_tab_notifications_cb_texting_enable(True)
result = view.get_tab_notifications_cb_texting_enable()
print("text tab: cb_texting_enable " + str(result))

view.set_tab_notifications_entry_texting_phonenumbers("1-123-456-7890")
result = view.get_tab_notifications_entry_texting_phonenumbers()
print(str(result))

view.set_tab_notifications_entry_texting_account_sid("account sid")
result = view.get_tab_notifications_entry_texting_account_sid()
print(str(result))

view.set_tab_notifications_entry_texting_account_token("token")
result = view.get_tab_notifications_entry_texting_account_token()
print(str(result))

view.set_tab_notifications_entry_texting_from_number("1-987-654-3210")
result = view.get_tab_notifications_entry_texting_from_number()
print(str(result))

view.set_tab_notifications_test_texting_button_call(method_for_texting_test)

# tab passed
passed_list = []
for index in range(0,40):
    passed_list.append("test passed " + str(index))
view.set_tab_passed_list(passed_list)

# tab failed
failed_list = []
for index in range(0,40):
    failed_list.append("test failed " + str(index))
view.set_tab_failed_list(failed_list)


#Menu --------------------------------------
view.setMenuFileExitCall(menuFileExit)

view.set_menu_project_new_call(menu_project_new)
view.set_menu_project_open_call(menu_project_open)
view.set_menu_project_save_call(menu_project_save)
view.set_menu_project_saveas_call(menu_project_saveas)
view.set_menu_project_close_call(menu_project_close)
view.set_menu_project_open_configuration_call(menu_project_open_configuration)
view.set_menu_project_save_configuration_call(menu_project_save_configuration)
view.set_menu_project_save_configuration_as_call(menu_project_save_configuration_as)

view.set_menu_about_about_call(menu_about_about)
view.set_menu_about_manual_call(menu_about_manual)


view.run()