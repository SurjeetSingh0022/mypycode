import paramiko
import time
from creds import username, password 

''' this fuction is define to connect to device and send command
    inputs are device_name and command '''

import paramiko

def send_commands(device_name, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(device_name, 22, username, password)
    commands = client.invoke_shell()
    commands.send(f"{command}\n")
    time.sleep(2)
#    _, stdout, _ = client.exec_command(command)
#    output = stdout.read().decode()
    output = commands.recv(1000000).decode("utf-8")
    client.close()
    return output

# Example usage:
#device_name = "192.168.2.14"
#command_to_execute = "show version"
#result = send_commands(device_name, command_to_execute)
#print(result)
