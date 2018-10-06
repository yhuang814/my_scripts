import sys
import shutil, errno
import argparse

from csv_logger import Csv_Logger
from prompt import Prompt
from config import Config
from ticket_helper import Ticket_Helper

#global config
config = Config() #config class to provide config.json file data
prompt = Prompt()

def prompt_handler(message) : 
    if prompt.confirm(message) == False : 
        print("Aborting operation....")
        exit()

def main():
    #test
        
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--start',
        default=None,
        required=True,
        help=('Compares two branches or two tag versions. eg.[start]..[end], "master..develop" OR "0.17"')
    )
    parser.add_argument(
        '--end',
        default=None,
        required=True,
        help=('Compares two branches or two tag versions. eg.[start]..[end], "master..develop" OR "0.17"')
    )
    parser.add_argument(
        '--branch',
        default='n',
        choices=['y', 'n'],
        help=('[n]/y, Indicate that it is a branch, and system will add "origin/" to branch name')
    )
    
    parser.add_argument(
        '--version',
        default=None,
        required=True,
        help=('The JIRA fix version you would like tickets the tickets to be updated to')
    )

    args = parser.parse_args()

    #compile string
    if args.branch is 'y' : 
        origin = "origin/"
        compare =  origin + args.start + ".." + origin + args.end
    else : 
        compare =  args.start + ".." + args.end 

    print("Compare Expression: " + compare)
    print("Fix Version: " + args.version)
    prompt_handler("Please confirm the above.")

    check_version = args.version
    ticket_helper = Ticket_Helper()
    commits = ticket_helper.get_commits()
    ticket_list = ticket_helper.get_grouped_tickets(commits)

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

    
    prompt_result = prompt.confirm("Are you sure you want to update above tickets to fix version " + check_version)
    print(prompt_result)

if __name__ == '__main__':
    	main()
        