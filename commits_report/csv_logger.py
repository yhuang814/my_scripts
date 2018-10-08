import csv
import os.path
from time import strftime
import datetime

class Csv_Logger :
    
    def __init__(self, fix_version):
        self.fix_version = fix_version
        self.write_items = []

    #TODO: implement error handling
    def log(self) : 
        script_dir = os.path.dirname(os.path.realpath(__file__))
        log_dir = script_dir + '/logs'

        if not os.path.isdir(log_dir) : 
            self.make_directory(log_dir)

        file_creation_timestamp = strftime("%m%d%Y_%H%M%S")

        fileName = log_dir + '/log_' + file_creation_timestamp + ".csv"

        print("Creating csv log file...")

        with open(fileName, 'wb') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            #header
            filewriter.writerow(['Ticket','Summary', 'Current Versions', 'Version Added', 'Ticket URL', 'Details', 'Updated Time'])
            
            for item in self.write_items :
                filewriter.writerow( [item["ticket_id"], item["summary"], item["current_versions"], item["version_added"], item["url"],item["details"], item["timestamp"]  ])
        
        print("Successfully created the CSV log file: " + fileName)

        return True

    def add(self, ticket_id, summary, current_versions, version_added, url, details) :       
        timestamp = datetime.datetime.now()
        write_item = {
            "timestamp" : timestamp,
            "ticket_id" : ticket_id,
            "summary" : summary,
            "current_versions" : current_versions,
            "version_added" : version_added,
            "url" : url,
            "details" : details
        }
        self.write_items.append(write_item)
        

    def make_directory(self, path):
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else :
            print("Successfully created the directory %s" % path)