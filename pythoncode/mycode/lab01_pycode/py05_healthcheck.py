from netmiko import ConnectHandler
from getpass import getpass
import datetime

username=input("Enter the username: ")
password=getpass("Enter the Password: ")
device_name=input("Enter the IP Address: ")

#tnow=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 

def device_healthcheck(ip):
    try:
        # Establish SSH connection
        print(f'connecting to {device_name} ')
        device = ConnectHandler(device_type='cisco_ios', ip=device_name, username=username, password=password)

        # Execute commands
        for command in commands:
            output = device.send_command(command)
            print(f'\n{command}:,\n{output}')
        # Close SSH connection
        device.disconnect()

    except Exception as e:
        print(f"Failed to connect to {device_name}: {e}")

# List of commands to execute
commands = ["terminal len 0","show processes cpu history", "show memory statistics", "show interfaces stats"]

#Excuting function to get logs
device_healthcheck(device_name)