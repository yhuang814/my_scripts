import csv
import os.path
from time import strftime

class Csv_Logger :
    
    def __init__(self, fix_version):
        self.fix_version = fix_version

    def log(self, tickets):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        log_dir = script_dir + '/logs'

        if not os.path.isdir(log_dir) : 
            self.make_directory(log_dir)

        timestamp = strftime("%m%d%Y_%H%M%S")

        fileName = log_dir + '/log_' + timestamp + ".csv"

        with open(fileName, 'wb') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #header
            filewriter.writerow(['ticket', 'Current Versions', 'Version Added', 'Details'])

            #content
            for ticket_key in tickets : 
                ticket = tickets[ticket_key]
                self.write_row(filewriter, ticket)

    def write_row(self, filewriter, ticket) :             
        commits = [] #add all commit id and author into array
        for commit in ticket["data"]:
            commits.append(commit["commit"] + " - " + commit["author"])
                    
        filewriter.writerow( [ticket["id"], ticket["versions"], self.fix_version, ''])

    def make_directory(self, path):
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else :
            print("Successfully created the directory %s" % path)