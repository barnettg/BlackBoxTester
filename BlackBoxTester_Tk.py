# Start Black Box Tester using Tkinter for the GUI
#
#
import BlackBoxTesterView
import BlackBoxTesterModel
import BlackBoxTesterControl

import sys
print("Python Version {}.{}".format(sys.version_info[0],sys.version_info[1]))

controller = BlackBoxTesterControl.Controller(BlackBoxTesterModel, BlackBoxTesterView)
controller.run()