from pprint import pprint as pp
import paramiko
import time
from getpass import getpass
from creds import username,password


# Using readlines()
inv = open('07_devices.txt', 'r')
device_list = inv.readlines()

# Using readlines()
config= open('07_config.txt', 'r')
config = config.readlines()

pp(config)


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
    
    for line in config:
        time.sleep(1)
        DEVICE_ACCESS.send(line)
    DEVICE_ACCESS.send(b'do term length 0\n')
    DEVICE_ACCESS.send(b'do show ip int brief\n')
    time.sleep(1)
    output = DEVICE_ACCESS.recv(65000)
    print (output.decode('ascii'))
    
    SESSION.close
