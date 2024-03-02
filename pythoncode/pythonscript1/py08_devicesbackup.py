from pprint import pprint as pp
import paramiko
import time
import datetime
from getpass import getpass
from creds import username,password
import os

tnow=datetime.datetime.now().replace(microsecond=0)
tnow=str(tnow)

# Using readlines()
inv = open('07_devices.txt', 'r')
device_list = inv.readlines()


for RTR in device_list:
    ip = RTR.strip()
    print ('\n##### Connecting to the device ' + ip +' #####')
    
    SESSION = paramiko.SSHClient()
    SESSION.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SESSION.connect(ip,port=22,
                    username=username,
                    password=password,
                    look_for_keys=False,
                    allow_agent=False)
    
    DEVICE_ACCESS = SESSION.invoke_shell() 
    
    DEVICE_ACCESS.send(b'term length 0\n')
    DEVICE_ACCESS.send(b'show run\n')
    time.sleep(3)
    output = DEVICE_ACCESS.recv(65000)
    print (output.decode('ascii'))
    save_file = open("backup_from_py08_router_"+ip, "w")
    save_file.write(output.decode('ascii'))
    save_file.close
    SESSION.close
