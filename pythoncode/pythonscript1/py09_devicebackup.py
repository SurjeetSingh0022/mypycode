from main import send_commands
import time

device_list=["192.168.2.14", "192.168.2.13"]
commands=["ter len 0", "show run"]


for device_name in device_list:
    print ("########### Connecting to "  +device_name+ " ###########")
    for cmd in commands:
        result= send_commands(device_name,cmd)
        time.sleep(3)
        #output = result.recv(65000)
        save_file = open("backup_from_py09_router_"+device_name, "w")
        save_file.write(result)
        save_file.close
        print (result)