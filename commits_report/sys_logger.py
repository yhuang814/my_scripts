import logging
import os.path

class Sys_Logger : 
    def __init__(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        log_dir = script_dir + '/logs'

        if not os.path.isdir(log_dir) : 
            self.make_directory(log_dir)

        LOG_FILENAME = log_dir + '/commits.log'
        logging.basicConfig(filename=LOG_FILENAME, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    
    #logs the message as info level and prints on terminal
    def log_print(self, message) : 
        logging.info(message)
        print(message)
    
    #log without displaying
    def log(self, message) : 
        logging.info(message)
    
    def make_directory(self, path):
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else :
            print("Successfully created the directory %s" % path)
