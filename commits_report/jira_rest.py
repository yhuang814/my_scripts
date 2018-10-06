import requests, json

class Jira : 
    def __init__(self, jira_config):
        self.jira_config = jira_config

    def update_ticket_version(self, ticket_id, version): 
        jira_config = self.jira_config
        username = jira_config['username']
        password = jira_config['password']

        request_url = "https://borngroup.atlassian.net/rest/api/2/issue/CNV-3481"
        
        body = {
            "update": {
                    "fixVersions": [{
                        "add": {
                            "name": "0.17.2"
                        }
                    }]
                }
        }

        headers = {'Content-type': 'application/json'}
        try:
            response = requests.put(request_url, data=json.dumps(body), headers=headers, auth=(username, password))
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print("lol" + e)
            exit()

        if(response.status_code == 204) :
            return True
        else : 
            return False

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