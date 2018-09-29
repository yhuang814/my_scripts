import sys
import json
import shutil, errno, os
import os.path

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


def main():
    repo_dir = get_repo_dir() 
    git_file = repo_dir + '/.git'
    os_command = 'git --git-dir ' + git_file + ' log'
    os_output = os.popen(os_command).read()
    #git log --pretty="%ci","%h","%an","%s"    

if __name__ == '__main__':
    	main()
        