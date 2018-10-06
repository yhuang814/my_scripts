import requests

class Jira : 
    def __init__(self, jira_config):
        self.jira_config = jira_config

    def get_ticket_versions(self, ticket_id) :
        jira_config = self.jira_config
        username = jira_config['username']
        password = jira_config['password']
        request_url = "https://borngroup.atlassian.net/rest/api/latest/issue/" + ticket_id + "?fields=fixVersions&fields=summary";
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