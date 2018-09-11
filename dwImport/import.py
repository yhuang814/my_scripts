import sys
import json
import shutil, errno, os
import os.path

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

def get_config() : 
    script_dir = os.path.dirname(os.path.realpath(__file__))
    fileName = script_dir + '/config.json'

    #reads the file
    with open(fileName) as f:
        data = json.load(f)

    config = data['config']

    return config

def is_template_allowed(template_type, allowed_types) : 
    for allowed_type in allowed_types:
        if template_type == allowed_type : 
            return True
    return False

#determine the import type
# if not specificed by user, use common import type
def get_template_path() : 
    if len(sys.argv) > 1 : 
        if  is_template_allowed(sys.argv[1], config.get('site_template_paths')) : 
            return sys.argv[1]
        else : 
            print("Invalid template type")
            sys.exit()
    else: 
        template_path = 'common'
    return template_path

def get_grunt_file_path() :
    #check if file exist
    grunt_file_path = build_suite_source + '/Gruntfile.js'
    if(os.path.isfile(grunt_file_path)) : 
        return grunt_file_path
    else :
        print('ERROR - ' + grunt_file_path + ' NOT FOUND!')
        sys.exit()


#retrieve data from config.json file
config = get_config()

project_name = config.get('project_name')
site_template_source = config.get('site_template_source')
build_suite_source = config.get('build_suite_source')

build_suite_grunt_file_path = get_grunt_file_path()

#assemble required build directories
build_suite_source_build_dir = build_suite_source + '/output' + '/' + project_name + '/site_import'
destination_dir = build_suite_source_build_dir + '/site_init'
os_command = "grunt --base " + build_suite_source + " --gruntfile " + build_suite_grunt_file_path + " importSite"

source_dir = site_template_source + '/' + get_template_path()

#Verify if destination path exists, if yes > delete path
if os.path.isdir(destination_dir) and os.path.exists(destination_dir) : 
    remove_dir(destination_dir)

#copy site template files from project to import staging folder
copy_dir(source_dir, destination_dir)

#add project parameter from command line
if len(sys.argv) > 2 : 
    os_command = os_command + ' --project=' + sys.argv[2]

#execute grunt command to upload and import files
os.system(os_command)

remove_dir(build_suite_source_build_dir) #clean up dir when completed