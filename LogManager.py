
import datetime
import os
import glob
import time

class LogManager:
    def __init__(self):
        self.using_file_name = ""
        self.clean_old_files_in_days = 30 # default: delete log file older than 30 day
    
    def set_new_file_name(self, timestamp = True, f_name = "", f_path = ""):
        now = datetime.datetime.now()
        file_name = ""
        if timestamp :
            file_name = now.strftime("%Y-%m-%d_%H-%M-%S")

        file_name = f_name + file_name + ".txt"
        file_name = os.path.join(f_path, file_name)
        print(file_name)
        self.using_file_name = file_name
        # clean old files out of path
        if os.path.isdir(f_path):
            print("get files")
            now = time.time()
            #print ("now: " + str(now))
            filelist = glob.glob(os.path.join(f_path, '*.txt'))
            for filename in filelist:
                #print(filename)
                filetime = os.path.getmtime(filename)
                #print(str(filetime))
                difference = (now-filetime)/60.0 / 60.0 / 24.0
                #print("difference: " + str(difference))
                if difference >= self.clean_old_files_in_days:
                    #delete file
                    #print("deleting file: " + filename )
                    self.write_log_message("deleting file: " + filename )
                    os.remove(filename)


    def write_log_message(self, message):
        now = datetime.datetime.now()
        log_message = str(now) + " " + message + "\n"
        print(log_message)
        with open(self.using_file_name, 'a') as outfile:
            outfile.write(log_message)

if __name__ == "__main__":
    lm = LogManager()
    lm.set_new_file_name(True, "this_new_file_", os.path.join("SampleProject", "logs"))
    lm.write_log_message("this is a message")
    lm.write_log_message("this is another message")

        
    
