import sys
import json
import shutil, errno, os

#copies the file
def copy_dir(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def remove_dir(path) : 
    shutil.rmtree(path)

script_dir = os.path.dirname(os.path.realpath(__file__))
fileName = script_dir + '/config.json'

#reads the file
with open(fileName) as f:
    data = json.load(f)

config = data['config']

project_name = config['project_name']
site_template_source = config['site_template_source']
build_suite_source = config['build_suite_source']
build_suite_source_build_dir = build_suite_source + '/output' + '/' + project_name + '/site_import'

source_dir = site_template_source + '/common'
destination_dir = build_suite_source_build_dir + '/site_init'

#Verify if destination path exists, if yes > delete path
if os.path.isdir(destination_dir) and os.path.exists(destination_dir) : 
    remove_dir(destination_dir)

copy_dir(source_dir, destination_dir)

os_command = "grunt --base " + build_suite_source + " importSite"

#add project parameter from command line
if len(sys.argv) > 1 : 
    os_command = os_command + ' --project=' + sys.argv[1]

os.system(os_command)

remove_dir(build_suite_source_build_dir) #clean up dir when completed

