import re, os, json
from jira_rest import Jira
from config import Config

from sys_logger import Sys_Logger
logger = Sys_Logger()

class Ticket_Helper : 
    def __init__(self):
        self.config = Config() #config class to provide config.json file data
        self.jira = Jira(self.config.get_jira_config())
        
    def get_commits(self, compare) :
        os_command = []
        os_command.append("git2json");

        repo_dir = self.config.get_repo_dir() #--git-dir
        if repo_dir : 
            os_command.append("--git-dir=" + repo_dir + '/.git')

        os_command.append("--compare=" + compare)
        os_command = " ".join(os_command)
        
        os_output = os.popen(os_command).read()
        commits = json.loads(os_output);
        return commits
    def get_grouped_tickets(self, commits):
        ticket_list = {}

        #group commits by ticket #
        for commit in commits : 

            commit_author = commit['author']['name']
            commit_id = commit['commit']
            commit_message = commit['message']

            commit_dict = {
                "author" : commit_author,
                "commit" : commit_id,
                "message" : commit_message
            }
            tickets = self.get_ticket_num(commit_message)
            if tickets : 
                for ticket in tickets : 
                    if ticket is not None : 
                        if ticket not in ticket_list :
                            ticket_list[ticket] = []
                        
                        ticket_list[ticket].append(commit_dict)
            
        return ticket_list
    #get JIRA ticket number from the commit message using regular expression
    def get_ticket_num(self, commit_message) : 
        regex = r"((?!([A-Z0-9a-z]{1,10})-?$)[A-Z]{1}[A-Z0-9]+-\d+)"
        matches = re.search(regex, commit_message)
        
        if matches:
            return matches.groups()
        
        return
    def get_failed_tickets(self, ticket_list, check_version) :
        failed_tickets = {}
        logger.log_print("Checking fix version: " + check_version)
        logger.log_print("Checking " + str(len(ticket_list)) + " tickets...")

        for key in ticket_list: 
            ticket = ticket_list[key]
            api_result = self.jira.get_ticket_versions(key)
            result = {}
            if api_result is False:
                result = {
                    "success" : False,
                    "error" : True,
                    "message" : "ERROR"
                }
            elif "fix_versions" in api_result and check_version in api_result["fix_versions"] :
                result = {
                    "success" : True,
                    "message" : "PASSED"
                }
            elif "fix_versions" in api_result and check_version not in api_result["fix_versions"]: 
                failed_tickets[key] = {
                    "data" : ticket,
                    "id" : key,
                    "versions" : " ".join(api_result["fix_versions"]),
                    "summary" : api_result["summary"]
                } 
                    
                result = {
                    "success" : False,
                    "message" : "FAILED"
                }
            
            if "error" in result and result["error"] is True:
                logger.log_print(result["message"] + " - Ticket: " + key)
            else : 
                logger.log_print(result["message"] + " - Ticket: " + key + " - Versions: " + " ".join(api_result["fix_versions"]))
        
        logger.log_print("TOTAL PASSED: " + str(len(ticket_list) - len(failed_tickets)))
        logger.log_print("TOTAL FAILED: " + str(len(failed_tickets)))
        return failed_tickets
    
    def update_ticket(self, ticket_id, version) : 
        return self.jira.update_ticket_version(ticket_id, version)
    
    #retrieve the store front JIRA ticket URL
    def get_jira_url(self, ticket_id) :
        base_url = self.config.get_base_url()
        if base_url and ticket_id : 
            return base_url + "/browse/" + ticket_id
        return ''
        
        