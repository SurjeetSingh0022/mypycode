from main import send_commands
import time
from getpass import getpass
from creds import scp_pass


device_list=["192.168.2.14", "192.168.2.13"]
commands=['copy nvram:startup-config scp://root@192.168.2.1///root/mypywork/configbackup/ROUTER' + '\n\n\n\n']    


for device_name in device_list:
    print ("########### Connecting to "  +device_name+ " ###########")
    for cmd in commands:
        result= send_commands(device_name,cmd)
        time.sleep(5)
        print (result)

    