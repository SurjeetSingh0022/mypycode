from netmiko import ConnectHandler

username='admin'
password='admin' 

def configure_device(ip):
    try:
        # Establish SSH connection
        print(f'connecting to ,{ip} ')
        device = ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password)

        # Execute commands
        for command in commands:
            output = device.send_command(command)
            print(output,'\n')

        # Close SSH connection
        device.disconnect()

    except Exception as e:
        print(f"Failed to connect to {ip}: {e}")

# List of commands to execute
commands = ["show ip int bri","show version"]


with open('D:\pythoncode\mycode\devices_inventory','r') as devices_inventory:
    for ip in devices_inventory:
        ip=ip.strip()
        configure_device(ip)    