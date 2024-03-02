from netmiko import ConnectHandler
from getpass import getpass

username=input("Enter the username: ")
password=getpass("Enter the Password: ")
ip=input("Enter the IP Address: ")

def configure_vlans(ip):
    try:
        # Establish SSH connection
        print(f'connecting to {ip} ')
        device = ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password)
        # List of commands to execute
        vlans = {
                10: 'admin',
                20: 'HR',
                30: 'IT'
                }
        
        #Executing config
        for vlan_id,vlan_name in vlans.items():
            device.send_config_set([f'vlan {vlan_id}', f'name {vlan_name}'])
            output=device.send_command('show vlan bri')
            if f'{vlan_id}' not in output:
                print(f'vlan {vlan_id} is not configured on device')

        # Close SSH connection
        device.disconnect()

    except Exception as e:
        print(f"Failed to connect to {ip}: {e}")



#Excuting function to get logs
configure_vlans(ip)