import requests, json
from sys_logger import Sys_Logger
logger = Sys_Logger()

class Jira : 
    def __init__(self, jira_config):
        self.jira_config = jira_config

    def update_ticket_version(self, ticket_id, version): 
        jira_config = self.jira_config
        username = jira_config['username']
        password = jira_config['password']
        base_url = jira_config['base_url']

        request_url = base_url + "/rest/api/2/issue/" + ticket_id

        #test
        logger.log_print("Updating ticket " + ticket_id + " to version " + version + " ...")
        logger.log_print("Request URL: " + request_url)
        
        body = {
            "update": {
                    "fixVersions": [{
                        "add": {
                            "name": version
                        }
                    }]
                }
        }

        headers = {'Content-type': 'application/json'}
        try:
            response = requests.put(request_url, data=json.dumps(body), headers=headers, auth=(username, password))
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            logger.log_print("Update Failed.")
            logger.log_print("JIRA UPDATE API ERROR: " + e)
            return False

        if(response.status_code == 204) :
            logger.log_print("Update completed.")
            return True
        else : 
            logger.log_print("Update Failed - Status Code: " + response.status_code)
            return False

    def get_ticket_versions(self, ticket_id) :
        jira_config = self.jira_config
        username = jira_config['username']
        password = jira_config['password']
        base_url = jira_config['base_url']

        request_url = base_url + "/rest/api/latest/issue/" + ticket_id + "?fields=fixVersions&fields=summary";
        response = requests.get(request_url, auth=(username, password))

        if(response.status_code == 200) :
            response_obj = response.json()
            response_fix_versions = response_obj['fields']['fixVersions']
            
            result = {
                "summary" : response_obj['fields']['summary']
            }
            fix_versions = []
            for version in response_fix_versions:
                fix_versions.append(version['name'])
            result["fix_versions"] = fix_versions
            return result
        else: 
            return False