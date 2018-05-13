# Handles running python scripts
import importlib
import sys

# to do:
#   pass helper class                               DONE
#   pass script directory to run                    DONE
#   import the run method and execute in thread
#   try/except on running script                    DONE
#       report exceptions                           DONE
#   report when done                                DONE
#   able to stop
#   queues??
#   debug stepping etc.

# can script make a new window?
# how to kill script -- run finally
# pause script?
# run script on network?

class PythonScriptEngine:

    def __init__(self):
        self.module = None

    def execute_script(self, script_path, script_name, helper_class):
        """
        :param script_path: directory containing the script
        :param script_name: name of script
        :param helper_class: class for the script to use to interface with Black Box tester
        :return: returns true is script executed correctly  or false if not and return a string message
        """

        print ("script_path: " + script_path)
        print ("sys.path: " + str(sys.path))

        #append path to script directory
        sys.path.append(script_path) #

        print ("sys.path: " + str(sys.path))

        new_script = script_name
        if new_script[-3:] == ".py":
            new_script = new_script[:-3]
        print ("new_script:" + new_script)
        print ("Helper class: " + str(helper_class))
        #passed = False
        returnDictionary = {}
        passed = False
        message = "Fail: exception error with " + script_name + " -> "
        returnDictionary['message'] = message
        #self.module = importlib.__import__(new_script, fromlist =['run'])
        #passed , message = self.module.run(helper_class)
        try:
            #self.module = importlib.__import__(new_script, fromlist =['run'])  # works
            self.module = __import__(new_script)    #works
            passed, message = self.module.run(helper_class)

        except Exception as e:
            message += str(e) + str(sys.exc_info()[0])
            returnDictionary['message'] = message

        sys.path.remove(script_path)

        return passed , message

class HelperClass:
    def __init__(self):
        pass

    def write_message(self, message):
        print(message)

    def write_message_log(self, message):
        print(message)


if __name__ == '__main__':
    helper_class = HelperClass()
    script_engine = PythonScriptEngine()
    print (script_engine.execute_script(
        r'C:\Users\glen\Documents\Projects\CoherentPythonProjects\PythonVersion\BlackBoxTester\SampleProject\scripts\group1',
        'TestScript.py', helper_class))


# Graveyard ----------------------------------------------------------------
    #sys.path.remove(r'\\network\path')
    #import module
    #import SampleProject.scripts.group1.TestScript as ts
    #module = importlib.__import__("SampleProject.scripts.group1.TestScript", fromlist =['run'])
    #print (script_engine.execute_script("SampleProject.scripts.group1.TestScript", "TestScript.py", helper_class))
    #print (script_engine.execute_script("SampleProject.scripts.group1", "TestScript.py", helper_class))
    #print (script_engine.doesThisWorkToo(helper_class))
    #print (script_engine.execute_script(r'C.Users.glen.Documents.Projects.CoherentPythonProjects.PythonVersion.BlackBoxTester.SampleProject.scripts.group1.TestScript', helper_class))

    #def doesThisWorkToo(self,helper_class):
    #   self.module.run(helper_class)