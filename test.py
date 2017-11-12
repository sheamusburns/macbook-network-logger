#!/usr/bin/env python

# remember: pip3 install requests 

import config as config #fill out empty_config.py, and rename as config.py
import os
import requests
from datetime import datetime
import subprocess

homeIP = config.homeIP
project_path = config.project_path
log_filename = config.log_filename
warning_string = config.warning_string

get_wifi_on_mac_args = ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I']
now = datetime.now()
curr_dir_path = os.getcwd()

if curr_dir_path != project_path:
	os.chdir(project_path)

curr_wifi_request = subprocess.run(get_wifi_on_mac_args, stdout=subprocess.PIPE)
curr_wifi_info = curr_wifi_request.stdout.decode('utf-8')

r = requests.get('https://api.ipify.org?format=json');
jsonIP = r.json()

f = open(project_path + log_filename,'a')
f.write(str(now) + '\nReturned IP: ' + jsonIP['ip'] + '\n')
f.write(curr_wifi_info)

if jsonIP['ip'] != homeIP:
	f.write('Status: Wrong IP\n')
	r1 = requests.get('http://ip-api.com/json')
	json_wrong_ip = r1.json()
	f.write(str(json_wrong_ip) + '\n\n')
	alert = subprocess.run(["osascript", "-e", "tell app \"System Events\" to display dialog" + warning_string])
else:
	f.write('Status: OK\n\n')

f.close()

