import sys
import json
import shutil, errno, os
import os.path
import requests
import re
from csv_logger import Csv_Logger

def get_config() : 
    script_dir = os.path.dirname(os.path.realpath(__file__))
    fileName = script_dir + '/config.json'

    #reads the file
    with open(fileName) as f:
        data = json.load(f)
    return data

def get_repo_dir() :
    config = get_config()
    if config['repo_dir'] : 
        return config['repo_dir']
    return

def get_base_url() :
    config = get_config()
    if config['jira']['base_url'] : 
        return config['jira']['base_url']
    return

def get_ticket_versions(ticket_id) : 
    config = get_config()
    jira_config = config['jira']
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

def get_failed_tickets(ticket_list, check_version) :
    failed_tickets = {}
    print("Checking fix version: " + check_version)
    print("Checking " + str(len(ticket_list)) + " tickets...")

    for key in ticket_list: 
        ticket = ticket_list[key]
        api_result = get_ticket_versions(key)
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
            print(result["message"] + " - Ticket: " + key)
        else : 
            print(result["message"] + " - Ticket: " + key + " - Versions: " + " ".join(api_result["fix_versions"]))
    
    print("TOTAL PASSED: " + str(len(ticket_list) - len(failed_tickets)))
    print("TOTAL FAILED: " + str(len(failed_tickets)))
    return failed_tickets

#get JIRA ticket number from the commit message using regular expression
def get_ticket_num(commit_message) : 
    regex = r"((?!([A-Z0-9a-z]{1,10})-?$)[A-Z]{1}[A-Z0-9]+-\d+)"
    matches = re.search(regex, commit_message)
    
    if matches:
        return matches.groups()
    
    return

def get_grouped_tickets(commits):
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
        tickets = get_ticket_num(commit_message)
        if tickets : 
            for ticket in tickets : 
                if ticket is not None : 
                    if ticket not in ticket_list :
                        ticket_list[ticket] = []
                    
                    ticket_list[ticket].append(commit_dict)
        
    return ticket_list


def main():
    os_command = []
    os_command.append("git2json");

    repo_dir = get_repo_dir() #--git-dir
    if repo_dir : 
        os_command.append("--git-dir=" + repo_dir + '/.git')
    os_command.append("--compare=origin/master..origin/hotfix_0.17.2")
    os_command = " ".join(os_command)
    
    os_output = os.popen(os_command).read()
    commits = json.loads(os_output);

    ticket_list = get_grouped_tickets(commits)
    
    check_version = "0.17"
    base_url = get_base_url()

    failed_tickets = get_failed_tickets(ticket_list, check_version)

    print("=================================================================")
    print("====================FAILED TICKETS===============================")
    print("=================================================================")

    for ticket_key in failed_tickets:
        ticket = failed_tickets[ticket_key]["data"]
        commit_count = len(ticket)
        print(ticket_key + " - Commits: " + str(commit_count))
        for commit in ticket : 
            print("+" + commit["commit"] + " - " + commit["author"] )
    
    csv_logger = Csv_Logger(check_version)
    csv_logger.log(failed_tickets)

if __name__ == '__main__':
    	main()
        