from pprint import pprint as pp

inter = ['Ethernet0/'+str(n) for n in range(1,4)] 

config = []

for interface in inter:
    config.extend (
        [
            f"interface {interface}",
            "no shutdown"

        ]
    )
            
pp(config)

#DEVICE_LIST = ['10.10.10.10','10.10.10.11','R1']
#print (DEVICE_LIST[0]) 

#some of the operations
# type(devices)
#dir(devices)
#devices.append('SW4')
#DEVICE_LIST = ['10.10.10.10','10.10.10.11']

#DEVICE_LIST = ['10.10.10.'+ str(n) for n in range(10,15)]
#pp(DEVICE_LIST)

#for RTR in DEVICE_LIST:
#    ip = "10.10.10." + str(n)
#    pp(ip)

import paramiko
import time
from getpass import getpass
from creds import username,password

a = int (input('Enter first loopback in range : '))
b = int (input('Enter last loopback in range : ')) + 1

device_list=["192.168.2." + str(i) for i in range(13,15)]

for RTR in device_list:
    ip = RTR
    print ('\n##### Connecting to the device ' + ip +' #####')
    
    SESSION = paramiko.SSHClient()
    SESSION.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SESSION.connect(ip,port=22,
                    username=username,
                    password=password,
                    look_for_keys=False,
                    allow_agent=False)
    
    DEVICE_ACCESS = SESSION.invoke_shell()
    DEVICE_ACCESS.send(b'config t\n')
    for N in range (a,b):
        DEVICE_ACCESS.send('int lo ' +str(N) + '\n')
        DEVICE_ACCESS.send('ip address 1.1.1.' +str(N) + ' 255.255.255.255\n') 
    
    time.sleep(3)
    DEVICE_ACCESS.send(b'do term length 0\n')
    DEVICE_ACCESS.send(b'do show ip int brief\n')
    time.sleep(1)
    output = DEVICE_ACCESS.recv(65000)
    print (output.decode('ascii'))
    
    SESSION.close
