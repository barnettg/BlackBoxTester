# test for the BlackBoxTesterView class
import sys
sys.path.append('..')
import BlackBoxTesterView

print("Python Version {}.{}".format(sys.version_info[0],sys.version_info[1]))


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

#main window --------------------------------------
view = BlackBoxTesterView.View()
view.setConfigurationLabel("This sets the configuration label")
view.setProjectLabel("This sets the project label")
view.setStatusLabel("This sets the status label")


#TAB scripts ----------------------------
view.setTabScriptDebugButtonCall(scriptTab_debugCallback)
view.setTabScriptEditButtonCall(scriptTab_editCallback)

#TAB ports ----------------------------
view.setTabPortsAddButtonCall(communicationsTab_addCallback)
view.setTabPortsEditButtonCall(communicationsTab_editCallback)
view.setTabPortsRemoveButtonCall(communicationsTab_removeCallback)
view.setTabPortsListbox(None) ## to do-> add list box data

#TAB plugins----------------------------
view.setTabPluginsAddButtonCall(pluginsTab_addCallback)
view.setTabPluginsRemoveButtonCall (pluginsTab_removeCallback)
view.setTabPluginsListbox(None) ## to do-> add list box data

#TAB projects ----------------------------
view.setTabProjOpenDirectoryButtonCall(projSetTab_openDirCallback)
view.setTabProjSelectEditorButtonCall(projSetTab_selectEditorCallback)
view.setTabProjShowConfSettingsButtonCall(projSetTab_showConfSettingsCallback)
view.setTabProjShowProjSettingsButtonCall(projSetTab_showProjSettingsCallback)

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