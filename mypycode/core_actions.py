from handler import NetmikoDeviceHandler
from interface_actions import InterfaceActions
import datetime
from pprint import pprint
import ipaddress

tnow=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 


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
    
    
def generate_device_base_config(device_name: str):
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
            mask = '255.255.255.0'
        if device_type != "juniper_junos":
            device_base_config.extend([
                f'hostname {device_name}',
                f'no service config',
                f'username admin privilege 15 secret 5 $1$S/mu$FA6YLsSMa1nkJq.i79/gC1',
                f'ip domain name vracks.lab.local',
                f'! ssh config',
                f'crypto key generate rsa modulus 4096',
                f'ip ssh version 2',
                f'! aaa config',
                f'aaa new-model',
                f'aaa authentication login default local',
                f'line vty 0 4',
                f'privilege level 15',
                f'transport input ssh',
                f'!',
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
        if device_base_config is not None:
                filename=(rf"D:\gitpycode\working_code\mypycode\device_onboarding_config\{device_name}.conf")  # replace with your path keep backup config.
                with open(filename, 'w') as save_file:
                    # Join the list items into a string with each item in a new line
                    device_base_config_str = '\n'.join(device_base_config)
                    save_file.write(device_base_config_str)
                #print(f'Logs saved to {filename})
        return {"device_base_config": device_base_config}
    except Exception as e:
        print(f"An error occurred: {e}")
        

# Example usage
#device_base_config=generate_device_base_config('RTR01')
#pprint(device_base_config)
        

def device_config_backup():
    try:
        # access device_inventory to get devices IP informantion
        with open (rf'D:\pythoncode\mycode\lab02_pycode\devices_inventory',"r") as rtr_list:  # replace with your path for device inventory.
            for device in rtr_list:
                device=device.strip()
                print(f'\n Connecting to {device}')
                handler=NetmikoDeviceHandler(device)
                connection = handler.connect()
                if connection is not None:
                    # Execute commands
                    for command in commands:
                        output = connection.send_command(command)
                        print(output,'\n')
                        filename=(rf"D:\pythoncode\backups\lab02_config_backup_{device}_{tnow}")  # replace with your path keep backup config.
                        try:
                            with open(filename, 'w') as save_file:
                                save_file.write(output)
                            print(f'Logs saved to {filename}')
                        except Exception as e:
                            print(e)        
                    # Close SSH connection
                    connection.disconnect()
    except Exception as e:
        print(f"Failed to connect to {device}: {e}")

# List of commands to execute
commands = ["terminal len 0","show run"]

#Excuting function to get logs
#device_config_backup()

def get_device_lldp_info(device_name: str): 
    try:
        handler = NetmikoDeviceHandler(device_name)
        connection = handler.connect()
        hostname = connection.find_prompt()[:-1]
    except Exception as e:
        return f'Unexpected error occurred while connecting to the device: {device_name} {e}'

    try:
        device_lldp_info = {}
        output=connection.send_command('show lldp neighbors',use_textfsm= True)
    except Exception as e:
        return f'failed to connect device: {device_name}: {e}'

    if isinstance(output, list):
        for item in output:
            remote_device = item.get('neighbor', 'N/A')
            local_interface = item.get('local_interface', 'N/A')
            remote_interface = item.get('neighbor_interface', ['N/A'])
            device_lldp_info[local_interface] = {'device_name': hostname, 'remote_device': remote_device, 'remote_interface': remote_interface}
        if device_lldp_info:
            return device_lldp_info
    else:
        return f'no lldp neighbor found on {device_name}'

# execution to test above function    
#config = get_device_lldp_info(device_name='192.168.2.23') 
#pprint(config)

def create_kustotable(device_name: str):
    subnet=input(f"Enter WAN Subnet for Your LAB: ")
    network = ipaddress.ip_network(subnet)
    addresses = network.hosts()
    device_lldp_info=get_device_lldp_info(device_name)
    interface_kusto_dict = {}
    for interface in device_lldp_info:
        interface_kusto_dict[interface] = device_lldp_info[interface].copy()  # Copy the existing info
        interface_kusto_dict[interface]['start_ipv4_addr'] = str(next(addresses))
        interface_kusto_dict[interface]['end_ipv4_addr'] = str(next(addresses))
    return interface_kusto_dict


def generate_interface_config(device_name: str):
    interface_kusto_dict= create_kustotable(device_name)
    interfaces_config=[]
    interfaces_list=[]
    for interface, info in interface_kusto_dict.items():
        interfaces_config.append([
        f"interface {interface}",
        f"description Connected to {info['remote_device']} on {info['remote_interface']}",
        f"ip address {info['start_ipv4_addr']} 255.255.255.252",
        f"no shutdown",
        f"!"
        ]) 
        interfaces_list.append([interface])     
    return {"interfaces_config": interfaces_config, "interfaces_list": interfaces_list}

config=generate_interface_config('192.168.2.23')
pprint(config)

