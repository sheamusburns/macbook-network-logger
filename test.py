#!/usr/bin/env python

# pip3 install requests if you don't have it. 


import os
import requests
from datetime import datetime

now = datetime.now()

dir_path = os.getcwd() #figure out which directory python is running in
print(dir_path)
os.chdir('/users/sburns/code/mblocator/')

# dir_path = os.getcwd() #figure out which directory python is running in
# print(dir_path)

r = requests.get('https://api.ipify.org?format=json');


f = open('/Users/sburns/Code/mblocator/log.txt','a')
jsonIP = r.json()
f.write('\n' + str(now) + ' - IP: ' + jsonIP['ip'])
f.close()