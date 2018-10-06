import sys
import json
import shutil, errno, os

from csv_logger import Csv_Logger
from prompt import Prompt
from config import Config
from ticket_helper import Ticket_Helper

#global config
config = Config() #config class to provide config.json file data

def main():
    ticket_helper = Ticket_Helper()

    os_command = []
    os_command.append("git2json");

    repo_dir = config.get_repo_dir() #--git-dir
    if repo_dir : 
        os_command.append("--git-dir=" + repo_dir + '/.git')
    os_command.append("--compare=origin/master..origin/hotfix_0.17.2")
    os_command = " ".join(os_command)
    
    os_output = os.popen(os_command).read()
    commits = json.loads(os_output);

    ticket_list = ticket_helper.get_grouped_tickets(commits)
    
    check_version = "0.17"

    failed_tickets = ticket_helper.get_failed_tickets(ticket_list, check_version)

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

    prompt = Prompt()
    prompt_result = prompt.confirm("Are you sure you want to update above tickets to fix version " + check_version)
    print(prompt_result)

if __name__ == '__main__':
    	main()
        