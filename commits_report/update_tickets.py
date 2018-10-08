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
    prompt_result = prompt.confirm(message)

    if prompt_result == True : 
        return True
    print("Aborting operation....")
    exit()    

def main():    

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

    #version number to be updated JIRA tickets.
    current_version = args.version

    ticket_helper = Ticket_Helper()
    
    #list of commits exist in B and not A using git expression A..B
    commits = ticket_helper.get_commits(compare)

    #group commits to ticket using ticket number as the unique key 
    ticket_list = ticket_helper.get_grouped_tickets(commits)

    #REST API call to JIRA to verify if each tickets contain 'current_version' in the list of ticket fix versions
    failed_tickets = ticket_helper.get_failed_tickets(ticket_list, current_version)

    #Print list of failed tickets and its commits.
    print("========================== FAILED TICKETS =========================")    
    for ticket_key in failed_tickets:
        ticket = failed_tickets[ticket_key]["data"]
        commit_count = len(ticket)
        print(ticket_key + " - Commits: " + str(commit_count))
        for commit in ticket : 
            print("+" + commit["commit"] + " - " + commit["author"] )
    
    csv_logger = Csv_Logger(current_version)
    csv_logger.log(failed_tickets)

    print("=============================== END ===============================")    

    if prompt_handler("Are you sure you want to update above tickets to fix version " + current_version) :
        for ticket_key in failed_tickets:
            ticket_helper.update_ticket(ticket_key, current_version)
            #TODO: add logging to csv when this returns true

if __name__ == '__main__':
    	main()
        