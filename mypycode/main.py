from handler import NetmikoDeviceHandler
from interface_actions import InterfaceActions
from pprint import pprint


def get_device_facts(device_name: str): 
    ''' This function will get device facts 
        i.e hostname,version,serial number, uptime
        param: device_name or ip as string
        result: get hostname,version,serial number, uptime in list format'''
    try:
        handler = NetmikoDeviceHandler(device_name)
        connection = handler.connect()
        device_facts = []
        output=connection.send_command('show version',use_textfsm= True)
        if output is not None:
            # Itrate over output to get the information
            for item in output:
                hostname = item.get('hostname', 'N/A')
                version = item.get('version', 'N/A')
                serial = item.get('serial', ['N/A'])[0]
                uptime = item.get('uptime', ['N/A'])
                device_facts.append(f'Hostname: {hostname}, Version: {version}, Serial Number: {serial}, uptime: {uptime}')
            if device_facts:
                return {"device_facts": device_facts} 
        else:
            return f"Failed to get show version output from {device_name}"    
    except Exception as e:
        return f'failed to get device facts due to Error: {e}' 

# execution to test above function    
#config = get_device_facts(device_name='192.168.2.21') 
#pprint(config)
    
    
def generate_base_config(device_name: str):
    '''This function generates base/minimal config for IOL RTR'''
    try:
        device_base_config = []
        # Ask user to enter device_type
        device_type = input("Enter your device_type (choose from cisco_iol, cisco_ios, arista_veos, juniper_junos): ")
        # Validate the user input
        valid_device_types = ["cisco_iol", "cisco_ios", "arista_veos", "juniper_junos"]
        if device_type not in valid_device_types:
            print("Invalid device_type. Please choose from the provided options.")
        else:
            print(f"device_type is: {device_type}")
        # Ask user to enter device management ip address
        ip_address = input('Enter device management ip eth0_0:')
        if not ip_address:
            ip_address = 'dhcp'
            mask = ''
        else:
            mask = 'mask 255.255.255.0'
        if device_type != "juniper_junos":
            device_base_config.extend([
                f'hostname {device_name}',
                f'username admin privilege 15 secret 5 $1$S/mu$FA6YLsSMa1nkJq.i79/gC1',
                f'ip domain name vracks.lab.local',
                f'crypto key generate rsa modulus 4096',
                f'ip ssh version 2',
                f'aaa new-model',
                f'aaa authentication login default local',
                f'line vty 0 4',
                f'privilege level 15',
                f'transport input both',
            ])
            if device_type == "cisco_iol":
                device_base_config.extend([
                    f'interface eth0/0',
                    f'description to-cloud',
                    f'ip address {ip_address} {mask}',
                    f'no shutdown',
                    f'do wri',
                    f'!',
                ])
            elif device_type == "cisco_ios":
                device_base_config.extend([
                    f'interface fa0/0',
                    f'description to-cloud',
                    f'ip address {ip_address} {mask}',
                    f'no shutdown',
                    f'do wri',
                    f'!',
                ])
            elif device_type == "arista_veos":
                device_base_config.extend([
                    f'interface mgmt1',
                    f'description to-cloud',
                    f'ip address {ip_address} {mask}',
                    f'no shutdown',
                    f'do wri',
                    f'!',
                ])
        return {"device_base_config": device_base_config}

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
#device_base_config=generate_base_config('RTR01')
#pprint(device_base_config)
        
# Example usage
inteface_running_config=InterfaceActions.get_interface_running_config('192.168.2.21',['Ethernet0/4'])
pprint(inteface_running_config)        

#config=interfaceActions.reset_interface_config(interfaces=['eth0/1','eth0/2'])
#config=config['reset_interface_config']

#config=interfaceActions.disable_interface(interfaces=['eth0/4','eth0/5'])
#config=config['disable_interface_config']  

#config=interfaceActions.enable_interface(interfaces=['eth0/1','eth0/2'])
#config=config['enable_interface_config']  

# execution to test above function    
#config = interfaceActions.get_device_interface_list(device_name='192.168.2.21')
#pprint(config['interface_status_list'])                            

def push_config(device_name:str, config: list):
    ''' This function will push the configuration to the device
        param: device_name or ip as string
        param: config_list as list
        result: True if successful, False otherwise'''
    try:
        handler = NetmikoDeviceHandler(device_name)
        connection = handler.connect()
        # Flatten the list of lists into a list of strings
        updated_config = [item for sublist in config for item in sublist]
        updated_config.append('do wri memory')
        pprint(updated_config)
        # Ask user for confirmation before pushing the config
        user_input = input("Are you sure you want to push the config? (yes/no): ")
        if user_input.lower() != "yes":
            print("Operation cancelled by user.")
            return False

        out = connection.send_config_set(updated_config)
        print(out)
        # Return True to indicate success
        return True
    except Exception as e:
        # Print an error message and return False
        print(f"Error pushing config: {str(e)}")
        return False

# Assume 'ssh_handler' is the device handler
#result = push_config('192.168.2.21', config)
#if result:
#    print("Config successfully pushed to the device.")
#else:
#    print("Failed to push config to the device.")






