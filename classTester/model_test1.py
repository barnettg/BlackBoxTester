# test for the BlackBoxTesterModel class
# open a new project and new project configuration
import sys
sys.path.append('..')
import BlackBoxTesterModel

class ControllerDummy(object):
    def communManager_obsrv(self, message):
        print("ControllerDummy->communManager_obsrv-> "+ message)

    def scriptManager_obsrv(self, message):
        print("ControllerDummy->scriptManager_obsrv-> "+ message)

    def helperClass_log_obsrv(self, message):
        print("ControllerDummy->helperClass_log_obsrv-> "+ message)

    def helperClass_mess_obsrv(self, message):
        print("ControllerDummy->helperClass_mess_obsrv-> "+ message)


cd = ControllerDummy()
model = BlackBoxTesterModel.Model(cd)

# register for communications log
model.register_for_communicationsManager_observer()
model.register_for_communicationsManager_observer(cd.communManager_obsrv)
# register for script manager log
model.register_for_script_observer()
model.register_for_script_observer(cd.scriptManager_obsrv)
# register for helper class log
model.register_for_helperclass_log_observer()
model.register_for_helperclass_log_observer(cd.helperClass_log_obsrv)
model.register_for_helperclass_message_observer()
model.register_for_helperclass_message_observer(cd.helperClass_mess_obsrv)

# open a new project
model.create_new_project('c:\\', 'temporaryTestDirectory')
model.create_new_project_configuration('config_temp_1.txt')  # sets default project configuration to be uses when saving

# save bbt configuration
model.save_bbt_configuration()

# set comports and open --------------
ser_avail_list = model.get_available_serial_ports()
print(str(ser_avail_list))
# select first com port
ser_prt = ser_avail_list[0]
model.project_configuration_add_serial_port_id("0", comport=ser_prt, baud='9600')

# save configuration
model.save_configuration() # saves default project configuration

# connect script manager to communications manager

# create new scripts

# script run configuration

# save configuration

# run scripts

# model.check_project_validity('c:','temporaryTestDirectory')

# remove the temporary project (optional)



