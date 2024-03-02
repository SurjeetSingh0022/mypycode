from netmiko import ConnectHandler
from getpass import getpass
import datetime
import difflib

username=input("Enter the username: ")
password=getpass("Enter the Password: ")
device_name=input("Enter the IP Address: ")

tnow=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 

def device_healthcheck(device_name, check_type):
    filename = rf'D:\pythoncode\mycode\logs_and_backup_files\{device_name}_{check_type}_{tnow}.txt'
    print(f'saving logs to {filename}')
    try:
        # Establish SSH connection
        print(f'connecting to {device_name} ')
        device = ConnectHandler(device_type='cisco_ios', ip=device_name, username=username, password=password)

        # Execute commands
        for command in commands:
            output = device.send_command(command)
#            print(output,'\n')
            try:
                with open(filename, 'a') as save_file:
                    save_file.write(output) 
            except Exception as e:
                print(e)        

        # Close SSH connection
#        device.disconnect()

    except Exception as e:
        print(f"Failed to connect to {device_name}: {e}")
    return filename

# List of commands to execute
commands = ["terminal len 0","show interface desc"]

# Perform pre-checks
pre_check_file = device_healthcheck(device_name, 'pre')

# Perform your network changes here...
config=["interface lo400",
        "shutdown"]
try:
    # Establish SSH connection
    print(f'connecting to {device_name} to configuring device')
    device = ConnectHandler(device_type='cisco_ios', ip=device_name, username=username, password=password)
    # Execute commands
    output = device.send_config_set(config)
    print(output,'\n')
    device.disconnect()
except Exception as e:
    print(f"Failed to connect to {device_name}: {e}")

# Perform post-checks
post_check_file = device_healthcheck(device_name, 'post')


# Compare pre and post checks
with open(pre_check_file, 'r') as pre, open(post_check_file, 'r') as post:
    diff = difflib.unified_diff(
        pre.readlines(),
        post.readlines(),
        fromfile=pre_check_file,
        tofile=post_check_file,
    )

for line in diff:
    print(line)
