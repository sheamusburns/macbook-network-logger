#!/usr/bin/env python

# remember: pip3 install requests 

import config as config #fill out empty_config.py, and rename as config.py
import os
import requests
from datetime import datetime
import subprocess
import json
import re

db_address = config.db_address
homeIP = config.homeIP
project_path = config.project_path
log_filename = config.log_filename
warning_string = config.warning_string

get_wifi_on_mac_args = ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I']
now = datetime.now()
curr_dir_path = os.getcwd()

if curr_dir_path != project_path:
	os.chdir(project_path)

hardware = subprocess.run(['system_profiler', 'SPHardwareDataType'], stdout=subprocess.PIPE)
hardware = hardware.stdout.decode('utf-8')
serial = re.findall('Serial\sNumber\s\(system\):\s(.+)', hardware)[0]
db_path = serial

curr_wifi_request = subprocess.run(get_wifi_on_mac_args, stdout=subprocess.PIPE)
curr_wifi_info = curr_wifi_request.stdout.decode('utf-8')
print(curr_wifi_info)


r = requests.get('https://api.ipify.org?format=json');
jsonIP = r.json()
ssid = re.findall('\sSSID:\s(.+)', curr_wifi_info)[0]
bssid = re.findall('\sBSSID:\s(.+)', curr_wifi_info)[0]

r1 = requests.get('http://ip-api.com/json')
json_wrong_ip = r1.json()
lat = json_wrong_ip['lat']
lon = json_wrong_ip['lon']
city = json_wrong_ip['city']



f = open(project_path + log_filename,'a')
f.write(str(now) + '\nReturned IP: ' + jsonIP['ip'] + '\n')

if jsonIP['ip'] != homeIP:
	status = 'BAD IP'
	f.write('Status: BAD IP\n')
	alert = subprocess.run(["osascript", "-e", "tell app \"System Events\" to display dialog" + warning_string])
else:
	status = 'OK'
	f.write('Status: OK\n\n')
f.write(curr_wifi_info)
f.write(str(json_wrong_ip) + '\n\n')
f.close()



j = json.dumps({'time':str(now), 'status': status, 'ip':jsonIP['ip'], 'ssid': ssid, 'bssid': bssid, 'city': city, 'lat': lat, 'lon': lon, 'serial': serial})
l = requests.post(db_address + db_path + '.json', data=j)

