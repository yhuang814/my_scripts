import sys
import json
import shutil, errno, os
import os.path


tags = ["0.0", "0.5" ,"0.5.1" ,"0.5.2" ,"0.5.3" ,"0.6" ,"0.6.1" ,"0.6.2" ,"0.6.3" ,"0.6.4" ,"0.6.5" ,"0.7" ,"0.7.1" ,"0.7.2" ,"0.7.3" ,"0.8" ,"0.8.1" ,"0.8.2" ,"0.9" ,"0.9.1" ,"0.9.2" ,"0.9.3" ,"0.10" ,"0.10.1" ,"0.11" ,"0.11.1" ,"0.11.2" ,"0.12" ,"0.12.1" ,"0.12.2" ,"0.12.3" ,"0.13" ,"0.13.1" ,"0.13.2" ,"0.13.3" ,"0.13.4" ,"0.13.5" ,"0.14" ,"0.14.1" ,"0.14.2" ,"0.14.3" ,"0.15" ,"0.15.1" ,"0.15.2" ,"0.15.3" ,"0.16" ,"0.16.1" ,"0.16.2" ,"0.16.3" ,"0.16.4"]

index = 0
while index < len(tags) - 1: 
	os_command = "git log --pretty=format:'%h; - %ci; - %s' " + tags[index] + ".."  + tags[index + 1] + " > " + tags[index + 1] + ".txt"
	print(os_command)
	index += 1
	#index = len(tags) #test
	os.system(os_command)

#os.system(os_command)