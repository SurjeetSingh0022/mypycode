import paramiko
import time
from getpass import getpass

host = input("Enter the Device_Name/IP_Address You want to Connect : ")
username = input( "Enter Username : ")
password = input( "Enter Password : ")
cmd = input("Enter the Command you want to Execute : ")


ssh = paramiko.SSHClient()

# Load SSH host keys.
ssh.load_system_host_keys()
# Add SSH host key automatically if needed.
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Connect to router using username/password authentication.
ssh.connect(host, 
            username=username, 
            password=password,
            look_for_keys=False )

# Run command.
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd.encode('ascii') + b"\n")  # Encode the command as bytes

output = ssh_stdout.readlines()
# Close connection.
ssh.close()

# Analyze show ip route output
for line in output:
    if "Ethernet0/0" in line:
        print("Found Ethernet:")
        print(line)

        