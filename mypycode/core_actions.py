from handler import NetmikoDeviceHandler
from interface_actions import InterfaceActions
import datetime
from pprint import pprint
import ipaddress
import csv

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
            end_device = item.get('neighbor', 'N/A')
            start_port = item.get('local_interface', 'N/A')
            end_port = item.get('neighbor_interface', ['N/A'])
            device_lldp_info[start_port] = {'start_device': hostname, 'start_port': start_port,'end_device': end_device, 'end_port': end_port}
        if device_lldp_info:
            return device_lldp_info
    else:
        return f'no lldp neighbor found on {device_name}'

def get_all_devices_lldp_info(rtr_list):
    all_devices_lldp_info = {}
    for device in rtr_list:
        device_lldp_info = get_device_lldp_info(device)
        if isinstance(device_lldp_info, dict):
            for start_port, lldp_info in device_lldp_info.items():
                # Create a unique identifier for the connection
                connection_id = tuple(sorted([lldp_info['start_device'] + lldp_info['start_port'], lldp_info['end_device'] + lldp_info['end_port']]))
                # Check if this connection already exists in the dictionary
                if connection_id not in all_devices_lldp_info:
                    all_devices_lldp_info[connection_id] = lldp_info
        else:
            print(device_lldp_info)
    return all_devices_lldp_info


#rtr_list=['192.168.2.21','192.168.2.22','192.168.2.23']
#all_devices_lldp_info = get_all_devices_lldp_info(rtr_list)
#pprint(all_devices_lldp_info)



def create_kustotable(device_name: str):
    subnet=input(f"Enter WAN Subnet for Your LAB: ")
    network = ipaddress.ip_network(subnet)
    addresses = network.hosts()
    # Specify the CSV file path
    csv_file_path = r"D:\gitpycode\working_code\mypycode\inventory\device_interface_ip_table.csv"
    device_lldp_info=get_device_lldp_info(device_name)
    interface_kusto_dict = {}
    for interface in device_lldp_info:
        interface_kusto_dict[interface] = device_lldp_info[interface].copy()  # Copy the existing info
        interface_kusto_dict[interface]['start_ipv4_addr'] = str(next(addresses))
        interface_kusto_dict[interface]['end_ipv4_addr'] = str(next(addresses))
        if interface_kusto_dict is not None:
            try:
                # Write data to CSV
                with open(csv_file_path, 'a', newline='') as csvfile:
                    fieldnames = list(interface_kusto_dict[next(iter(interface_kusto_dict))].keys())
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    for key, value in interface_kusto_dict.items():
                        writer.writerow(value)
            except Exception as e:
                return e        
    return interface_kusto_dict


#interface_kusto_dict=create_kustotable('192.168.2.23')
#print(interface_kusto_dict)

def create_kustotable_for_all_devices(rtr_list):
    # Specify the CSV file path
    csv_file_path = r"D:\gitpycode\working_code\mypycode\inventory\device_interface_ip_table.csv"
    subnet=input(f"Enter WAN Subnet for Your LAB: ")
    network = ipaddress.ip_network(subnet)
    addresses = network.hosts()
    all_devices_lldp_info = get_all_devices_lldp_info(rtr_list)
    for connection_id, device_lldp_info in all_devices_lldp_info.items():
        if isinstance(device_lldp_info, dict):  # Check if device_lldp_info is a dictionary
            interface_kusto_dict = device_lldp_info.copy()  # Copy the existing info
            interface_kusto_dict['start_ipv4_addr'] = str(next(addresses))
            interface_kusto_dict['end_ipv4_addr'] = str(next(addresses))
            try:
                # Write data to CSV
                with open(csv_file_path, 'a', newline='') as csvfile:
                    fieldnames = list(interface_kusto_dict.keys())
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow(interface_kusto_dict)
            except Exception as e:
                return f'error with csv as {e}'       
    return "Kusto table created for all devices."

#rtr_list=['192.168.2.21','192.168.2.22','192.168.2.23']
#print(create_kustotable_for_all_devices(rtr_list))

import csv
csv_file_path = r"D:\gitpycode\working_code\mypycode\inventory\device_interface_ip_table.csv"
with open(csv_file_path, 'r') as file:
    csv_file = csv.DictReader(file)
    for row in csv_file:
        pprint(dict(row))



def generate_interface_config(device_name: str):
    interface_kusto_dict= create_kustotable(device_name)
    interfaces_config=[]
    interfaces_list=[]
    for interface, info in interface_kusto_dict.items():
        interfaces_config.append([
        f"interface {interface}",
        f"description Connected to {info['remote_device']} on {info['remote_interface']}",
        f"ip address {info['start_ipv4_addr']} 255.255.255.252",
        f"no proxy-arp",
        f"no ip unreachable",
        f"load-interval 30",
        f"no shutdown",
        f"!"
        ]) 
        interfaces_list.append([interface])     
    return {"interfaces_config": interfaces_config, "interfaces_list": interfaces_list}

#config=generate_interface_config('192.168.2.23')
#pprint(config)

