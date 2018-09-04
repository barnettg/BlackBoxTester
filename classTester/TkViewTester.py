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

view = BlackBoxTesterView.View()
view.setConfigurationLabel("This sets the configuration label")
view.setProjectLabel("This sets the project label")
view.setStatusLabel("This sets the status label")
view.setTabScriptDebugButtonCall(scriptTab_debugCallback)
view.setTabScriptEditButtonCall(scriptTab_editCallback)

view.setTabPortsAddButtonCall(communicationsTab_addCallback)
view.setTabPortsEditButtonCall(communicationsTab_editCallback)
view.setTabPortsRemoveButtonCall(communicationsTab_removeCallback)
view.setTabPortsListbox(None) ## to do-> add list box data

view.setTabPluginsAddButtonCall(pluginsTab_addCallback)
view.setTabPluginsRemoveButtonCall (pluginsTab_removeCallback)
view.setTabPluginsListbox(None) ## to do-> add list box data

view.setTabProjOpenDirectoryButtonCall(projSetTab_openDirCallback)
view.setTabProjSelectEditorButtonCall(projSetTab_selectEditorCallback)
view.setTabProjShowConfSettingsButtonCall(projSetTab_showConfSettingsCallback)
view.setTabProjShowProjSettingsButtonCall(projSetTab_showProjSettingsCallback)


view.setMessagingMethod(viewMessages)

view.run()