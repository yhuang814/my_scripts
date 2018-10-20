import os.path
import json

class Config :
    def __init__(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        fileName = script_dir + '/config.json'

        #reads the file
        with open(fileName) as f:
            data = json.load(f)
            self.config_data = data

    def get_repo_dir(self) :
        config = self.config_data
        if config['repo_dir'] : 
            return config['repo_dir']
        return

    def get_base_url(self) :
        config = self.config_data
        if config['jira']['base_url'] : 
            return config['jira']['base_url']
        return

    def get_jira_config(self) : 
        config = self.config_data
        return config['jira']