import sys
import json
import shutil, errno, os
import os.path
import requests

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

def main():
    repo_dir = get_repo_dir() 
    git_file = repo_dir + '/.git'

    os_command = 'git --git-dir ' + git_file + ' log master..hotfix_0.17.2 --pretty=\"%ci\",\"%h\",\"%an\",\"%s\"'
    os_output = os.popen(os_command).read()
    print(os_output)

if __name__ == '__main__':
    	main()
        