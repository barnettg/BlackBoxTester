# test for the BlackBoxTesterModel class
# open a new project and new project configuration
import sys
sys.path.append('..')
import BlackBoxTesterModel

class ControllerDummy(object):
    def communManager_obsrv(self, message):
        print("ControllerDummy->communManager_obsrv-> "+ message)

    def scriptManager_obsrv(self, **kwargs):
        print("ControllerDummy->scriptManager_obsrv-> "+ str(kwargs))

    def scriptManager_obsrv_log(self, message):
        print("ControllerDummy->scriptManager_obsrv_log-> "+ message)

    def helperClass_log_obsrv(self, message):
        print("ControllerDummy->helperClass_log_obsrv-> "+ message)

    def helperClass_mess_obsrv(self, message):
        print("ControllerDummy->helperClass_mess_obsrv-> "+ message)

    def configManager_log_obsrv(self, message):
        print("ControllerDummy->configManager_log_obsrv-> "+ message)


cd = ControllerDummy()
model = BlackBoxTesterModel.Model(cd)

# register for configuration manager log
#model.register_for_configurationManager_observer()
model.register_for_configurationManager_observer(cd.configManager_log_obsrv)

# register for communications log
model.register_for_communicationsManager_observer()
model.register_for_communicationsManager_observer(cd.communManager_obsrv)

# register for script manager log
model.register_for_script_log(cd.scriptManager_obsrv_log)

# register for script manager notify
model.register_for_script_observer()
model.register_for_script_observer(cd.scriptManager_obsrv)

# register for helper class log
model.register_for_helperclass_log_observer()
model.register_for_helperclass_log_observer(cd.helperClass_log_obsrv)
model.register_for_helperclass_message_observer()
model.register_for_helperclass_message_observer(cd.helperClass_mess_obsrv)

# open a new project
#model.create_new_project('c:\\', 'temporaryTestDirectory')
model.create_new_project('c:\\Users\\glen\\Documents\\', 'temporaryTestDirectory')
model.create_new_project_configuration('config_temp_1.txt')  # sets default project configuration to be uses when saving

# save bbt configuration
model.save_bbt_configuration()

# set comports and open --------------
print("set comports and open -------")
ser_avail_list = model.get_available_serial_ports()
print(str(ser_avail_list))
# select first com port
ser_prt = ser_avail_list[1]
model.project_configuration_add_serial_port_id("0", comport=ser_prt, baud='57600')
model.project_configuration_add_network_port_id("1", ip="127.0.0.1", network_port='502')

# save configuration
print("save configuration -------")
model.save_configuration()  # saves default project configuration

# create new scripts
print("create new scripts -------")
contents = (
'''# python test scripts

def run(HC):
    HC.write_message("message 1")
    HC.write_message("message 2")
    result = HC.send("?state", 0)
    HC.write_message("port ID 0 ?state result:" + result)
    result = HC.send("CHANGE", 0)
    HC.write_message("port ID 0 CHANGE result:" + result)
    result = HC.send("?state", 1)
    HC.write_message("port ID 1 ?state result:" + result)
    result = HC.send("CHANGE", 1)
    HC.write_message("port ID 1 CHANGE result:" + result)
    return True, "PASS "
''')
model.create_new_script("group1","firstScript.py", contents)

# script run configuration
print("set script configuration -------")
script_name = "scripts\\group1\\firstScript.py"
model.add_script_to_configuration(script_name)
model.set_script_configurations(script_name, selected_to_run="True", priority_level=1)

# get available communication ports

# save configuration
print("save configuration -------")
model.save_configuration() # default config file should be used

# run scripts
# open application using serial ports
com_string = ser_avail_list[0]
# ------ print "Open a test system program using " + com_string
# wait for <cr>
resp = input("Open TrafficLights.py to test on " + com_string + "  at 57600 baud")
resp = input("Open TrafficLights.py ethernet to test on 127.0.0.1")
model.run_scripts(10)# run down to level 10

# close project
model.close_project()

# try to run things with a closed project -- not crash and notify
print("Try to run things with a closed project")
print("run scripts -------")
model.run_scripts(10)# run down to level 10
print("save configuration -------")
model.save_configuration() # default config file should be used
print("open new configuration -------")
model.create_new_project_configuration('config_temp_x.txt')


# open project
model.open_project('c:\\Users\\glen\\Documents\\temporaryTestDirectory')

# open configuration
model.open_project_config('config_temp_1.txt')

# run scripts
model.run_scripts(10)# run down to level 10

# model.check_project_validity('c:','temporaryTestDirectory')

# remove the temporary project (optional)



