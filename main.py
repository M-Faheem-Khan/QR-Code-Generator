#!/usr/bin/env python3

import os
import sys
import socket
import zipfile
import requests
from datetime import datetime

print("TIME: %s" % str(datetime.now().time())[:8])
print("Starting server\n")
# bind to port 5006
ip = ""
port = 5006

# trying to bind to port 5006
print("TIME: %s" % str(datetime.now().time())[:8])
print("Binding to port: %d" % port)
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind((ip, port))
except Exception as e:
    print("TIME: %s" % str(datetime.now().time())[:8])
    print("The following execption was raised while trying to bind to port %d \n%s" % (port, e))
    sys.exit(-1) # exit with error

print("TIME: %s" % str(datetime.now().time())[:8])
print("Sucessfully binded to port")
print("Listening for update URL")
while True:
    data, addr = sock.recvfrom(1024)
    url = data.decode("ASCII")
    print("TIME: %s" % str(datetime.now().time())[:8])
    print("URL: %s" % data)

    # trying to get the zip file from url
    try:
        response = requests.get(url)
        with open("/home/pi/upgrade.zip", 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print("TIME: %s" % str(datetime.now().time())[:8])
        print("The following exception was raised while trying to get zip file from url: %s \n%s" % (url, e))

    # stopping myScript.service
    # deleting all the file except for .json and hub_ctrl
    os.system("sudo systemctl stop myScript.service")

    ls = os.listdir("/home/pi/production/")
    for i in ls:
        if not "hub_ctrl" in i or not i.endswith(".json"):
            os.remove("/home/pi/production/%s" % (i))

    print("TIME: %s" % str(datetime.now().time())[:8])
    print("All files !(.json, hub-ctrl) have been deleted from /home/pi/production/")
    
    # extracting all the files to the production folder
    with zipfile.ZipFile("/home/pi/upgrade.zip", "r") as f:
        f.extractall("/home/pi/production/")

    print("TIME: %s" % str(datetime.now().time())[:8])
    print("Files has been extracted to /home/pi/production/")

    # reloading daemon
    # restarting service
    os.system("sudo systemctl daemon-reload")
    os.system("sudo systemctl start myScript.service")
    
    print("TIME: %s" % str(datetime.now().time())[:8])
    print("Files has been updated")