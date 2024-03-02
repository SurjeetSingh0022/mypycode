import creds
from main import send_commands

# Get user input
host = input("Enter the Device_Name/IP_Address You want to Connect: ")
cmd = input("Enter the Command you want to Execute: ")

# Call the functions
command_output = send_commands(host, cmd + "\n")
print("++++++++++++++++++ Command output: +++++++++++++++++++" + "\n")
print(command_output)