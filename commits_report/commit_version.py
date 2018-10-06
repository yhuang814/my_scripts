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

def get_ticket_versions(ticket_id) : 
    config = get_config()
    jira_config = config['jira']
    username = jira_config['username']
    password = jira_config['password']
    request_url = "https://borngroup.atlassian.net/rest/api/latest/issue/" + ticket_id + "?fields=fixVersions";
    response = requests.get(request_url, auth=(username, password))

    if(response.status_code == 200) :
        response_obj = response.json()
        return response_obj['fields']['fixVersions']
    return

#get JIRA ticket number from the commit message using regular expression
def get_ticket_num(commit_message) : 
    regex = r"((?!([A-Z0-9a-z]{1,10})-?$)[A-Z]{1}[A-Z0-9]+-\d+)"
    matches = re.search(regex, commit_message)
    
    if matches:
        return matches.groups()
    
    return
        

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

    parsed_commits = []
    
    for commit in commits : 
        d = {
            "author" : commit['author']['name'],
            "commit" : commit['commit'],
            "message" : commit['message']
        }
        d["tickets"] = get_ticket_num(d['message'])
        parsed_commits.append(d)

if __name__ == '__main__':
    	main()
        