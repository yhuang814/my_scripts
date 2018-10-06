import sys
import json
import shutil, errno, os
import os.path
import requests
import re

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
    request_url = "https://borngroup.atlassian.net/rest/api/latest/issue/" + ticket_id + "?fields=fixVersions";
    response = requests.get(request_url, auth=(username, password))

    if(response.status_code == 200) :
        response_obj = response.json()
        response_fix_versions = response_obj['fields']['fixVersions']
        fix_versions = []
        for version in response_fix_versions:
            fix_versions.append(version['name'])
        return fix_versions
    return []

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

        tickets = get_ticket_num(commit_message)
        if tickets : 
            for ticket in tickets : 
                if ticket is not None : 
                    if ticket not in ticket_list :
                        ticket_list[ticket] = {
                            "authors" : [],
                            "commits" : []
                        }
                    if commit_author not in ticket_list[ticket]["authors"]:
                        ticket_list[ticket]["authors"].append(commit_author)
                    
                    if commit_id not in ticket_list[ticket]["commits"]:
                        ticket_list[ticket]["commits"].append(commit_id)
        
    return ticket_list


def main():
    os_command = []
    os_command.append("git2json");

    repo_dir = get_repo_dir() #--git-dir
    if repo_dir : 
        os_command.append("--git-dir=" + repo_dir + '/.git')
    os_command.append("--compare=0.16.9..0.17")
    os_command = " ".join(os_command)
    
    os_output = os.popen(os_command).read()
    commits = json.loads(os_output);

    ticket_list = get_grouped_tickets(commits)
    
    check_version = "0.17"
    base_url = get_base_url()

    for ticket in ticket_list: 
        fix_versions = get_ticket_versions(ticket)
        if check_version in fix_versions :
            result = {
                "success" : True,
                "message" : "Passed"
            }
        else : 
            result = {
                "success" : False,
                "message" : "Failed"
            }
        if result["success"] is False : 
            ticket_url = base_url + "/browse/" + ticket
            print("ticket #: " + ticket + " - " + " ".join(fix_versions) + " - " + result["message"] + " - " + ticket_url)

if __name__ == '__main__':
    	main()
        