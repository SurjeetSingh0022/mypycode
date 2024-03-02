from netmiko import ConnectHandler
from getpass import getpass
import datetime

username=input("Enter the username: ")
password=getpass("Enter the Password: ")
ip=input("Enter the IP Address: ")

tnow=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 

def getlogs(ip):
    try:
        # Establish SSH connection
        print(f'connecting to {ip} ')
        device = ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password)

        # Execute commands
        for command in commands:
            output = device.send_command(command)
            print(output,'\n')
            filename=(rf'D:\pythoncode\mycode\logs_and_backup_files\py03_logs_{ip}_{tnow}')
            with open(filename, 'w') as save_file:
                save_file.write(output)
            print(f'Logs saved to {filename}')    

        # Close SSH connection
        device.disconnect()

    except Exception as e:
        print(f"Failed to connect to {ip}: {e}")

# List of commands to execute
commands = ["show logging"]

#Excuting function to get logs
getlogs(ip)