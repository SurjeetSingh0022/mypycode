from handler import NetmikoDeviceHandler
from interface_actions import InterfaceActions
import datetime
from pprint import pprint
import ipaddress
import csv
import ctypes
import os
import subprocess
import sys
from jinja2 import Template

tnow=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 


def update_hostfile(device_facts: str):
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    # Extract the hostname   
    device_name = device_facts['device_name']
    management_ip = device_facts['management_ip']
    new_host_entry = (f'{management_ip}    {device_name}')
    ## Request admin privileges
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)
    ## Append to the hosts file
    with open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'a') as hosts_file:
        print(f'updating system hostfile with for {device_name}') 
        hosts_file.write(f"\n{new_host_entry}")


def update_device_inventory(device_name: str): 
    try:
        handler = NetmikoDeviceHandler(device_name)
        connection = handler.connect()
        csv_file_path = r"D:\gitpycode\working_code\mypycode\inventory\lab02deviceinventory.csv"
        device_facts = {}
        output=connection.send_command('show version',use_textfsm= True)
        get_interfaces=InterfaceActions.get_device_interface_list(device_name)
        device_interfaces_ip_list=get_interfaces['device_interfaces_ip_list']
        Management_IP = list(device_interfaces_ip_list.keys())[0]
        Management_IP = device_interfaces_ip_list[Management_IP]    
        if output is not None:
            for item in output:
                hostname = item.get('hostname', 'N/A')
                version = item.get('version', 'N/A').split("(")[0]
                serial = item.get('serial', ['N/A'])[0]
                uptime = item.get('uptime', ['N/A'])
                hwsku = item.get('running_image', ['N/A']).split('/')[4]
                if "L3" in item.get('running_image', ['N/A']).split('/')[6]:
                    device_type= 'router'
                elif "L2" in item.get('running_image', ['N/A']).split('/')[6]:
                    device_type= 'switch'   
                device_facts = {'device_name': hostname, 'management_ip': Management_IP, 'hwsku': hwsku, 'device_type': device_type, 'version': version, 'serial number': serial, 'uptime': uptime}            
            if device_facts is not None:
                try:
                    print(f'updating device_inventory for {device_name}')
                    with open(csv_file_path, 'a', newline='') as csvfile:
                        fieldnames = list(device_facts.keys())
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writerow(device_facts)
                        update_hostfile(device_facts)  
                except Exception as e:
                    return f'error with csv as {e}'
        if device_facts is not None:
            return device_facts                  
        else:
            return f"Failed to get show version output from {device_name}"                    
    except Exception as e:
        return f'failed to get device facts due to Error: {e}' 

#for i in range(21,26):
#    device_name=(f'192.168.2.{i}')
#    update_device_inventory(device_name)

def generate_device_base_config(device_name: str):
    '''This function generates a base or minimal configuration for network devices.
    Parameters:
    device_name (str): The name of the device for which the configuration is to be generated.
    Returns:
    dict: A dictionary containing the base configuration for the device.'''

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
                f'no cdp run',
                f'lldp run',
                f'! aaa config',
                f'aaa new-model',
                f'aaa authentication login default local',
                f'line vty 0 4',
                f'privilege level 15',
                f'transport input ssh',
                f'!',
            ])
            if device_type == "cisco_iol":
                if "rtr" in device_name.lower():
                    device_base_config.extend([
                        f'interface eth0/0',
                        f'description to-cloud',
                        f'ip address {ip_address} {mask}',
                        f'no shutdown',
                        f'interface range eth0/0-3',
                        f'no shutdown',
                        f'do wri',
                        f'!',
                    ])
                if "sw" in device_name.lower():
                    device_base_config.extend([
                        f'interface eth0/0',
                        f'description to-cloud',
                        f'no switchport',
                        f'ip address {ip_address} {mask}',
                        f'no shutdown',
                        f'interface range eth0/0-3',
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
#device_base_config=generate_device_base_config('core-sw01')
#pprint(device_base_config)
        

def device_config_backup():
    '''This function backs up the configuration of network devices.'''
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
    '''
    Retrieves the Link Layer Discovery Protocol (LLDP) information of a specified network device.
    Parameters: device_name (str): The name of the network device.
    Returns:
    dict: A dictionary containing the LLDP information if successful.
    str: An error message if an error occurs during the process.
    '''
    try: 
        handler = NetmikoDeviceHandler(device_name)
        connection = handler.connect()
        hostname = connection.find_prompt()[:-1]
        if connection is not None:
            device_lldp_info = {}
            output=connection.send_command('show lldp neighbors',use_textfsm= True)
            if isinstance(output, list):
                for item in output:
                    end_device = item.get('neighbor', 'N/A').split('.')[0]
                    start_port = item.get('local_interface', 'N/A')
                    end_port = item.get('neighbor_interface', ['N/A'])
                    device_lldp_info[start_port] = {'start_device': hostname, 'start_port': start_port,'end_device': end_device, 'end_port': end_port}
                if device_lldp_info:
                    return device_lldp_info
            else:
                return f'no lldp neighbor found on {hostname}:{device_name}' 
    except Exception as e:
        return f'failed to connect device: {device_name}: {e}'


def get_all_devices_lldp_info(devices_list):
    '''
    Retrieves the Link Layer Discovery Protocol (LLDP) information of a all network devices.
    Parameters: devices_list (list): The name of the network device.
    Returns:
    dict: A dictionary containing the LLDP information if successful.
    str: An error message if an error occurs during the process.
    '''
    all_devices_lldp_info = {}
    for device in devices_list:
        device_lldp_info = get_device_lldp_info(device)
        if isinstance(device_lldp_info, dict):
            for start_port, lldp_info in device_lldp_info.items():
                # Create a unique identifier for the connection
                connection_id = tuple(sorted([lldp_info['start_device'] + lldp_info['start_port'], lldp_info['end_device'] + lldp_info['end_port']]))
                # Check if this connection already exists in the dictionary
                if connection_id not in all_devices_lldp_info:
                    all_devices_lldp_info[connection_id] = lldp_info
        else:
            return (f'lldp information not found.')            
    return all_devices_lldp_info


#devices_list=['192.168.2.21']
#all_devices_lldp_info = get_all_devices_lldp_info(devices_list)
#pprint(all_devices_lldp_info)



def create_kustotable(device_name: str):
    """
    This function creates a dictionary of interface information for a given device and writes it to a CSV file.
    Parameters:
    device_name (str): The name of the device for which the interface information is to be fetched and stored.
    Returns:
    dict: A dictionary containing the interface information for the given device.
    """
    subnet=input(f"Enter WAN Subnet for Your LAB: ")
    network = ipaddress.ip_network(subnet)
    addresses = network.hosts()
    # Specify the CSV file path
    csv_file_path = r"D:\gitpycode\working_code\mypycode\inventory\deviceinterfaceiptable.csv"
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


#nterface_kusto_dict=create_kustotable('192.168.2.23')
#print(interface_kusto_dict)

def create_kustotable_for_all_devices(device_list):
    """
    This function creates a dictionary of interface information for all devices and writes it to a CSV file.
    Parameters:
    device_list(lsit): The name of the device for which the interface information is to be fetched and stored.
    Returns:
    dict: A dictionary containing the interface information for the given device.
    """
    # Specify the CSV file path
    csv_file_path = r"D:\gitpycode\working_code\mypycode\inventory\deviceinterfaceiptable.csv"
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

#rtr_list=['192.168.2.21','192.168.2.22','192.168.2.23','192.168.2.24','192.168.2.25']
#print(create_kustotable_for_all_devices(rtr_list))

def verify_device_in_device_inventory(device_name: str):
    device_inventory=rf'mypycode/inventory/lab02deviceinventory.csv'
    inventory_device_list=[]
    with open(device_inventory, mode ='r') as file:
        csvFile = csv.DictReader(file)
        for line in csvFile:
            inventory_device_list.append(line['device_name'])   
        if device_name not in inventory_device_list:
            print(f"{device_name} is not found in inventory")

def reverse_wiring(row, device_name):
    if device_name in row['end_device']:
        start_device=row['end_device'].strip()
        start_port=row['end_port'].strip()
        start_ipv4_addr=row['end_ipv4_addr'].strip()
        end_device=row['start_device'].strip()
        end_port=row['start_port'].strip()
        end_ipv4_addr=row['start_ipv4_addr'].strip()
    elif device_name in row['start_device']:
        start_device=row['start_device'].strip()
        start_port=row['start_port'].strip()
        start_ipv4_addr=row['start_ipv4_addr'].strip()
        end_device=row['end_device'].strip()
        end_port=row['end_port'].strip()
        end_ipv4_addr=row['end_ipv4_addr'].strip()
    else:
        print(f'wiring is not availabe for this device')    
    return start_device, start_port, start_ipv4_addr, end_device, end_port, end_ipv4_addr

def interface_and_ip_table_reader(device_name: str):
    """
    This function will read the deviceinterfaceiptable.csv.
    Parameters:
    device_name (str): The name of the device for which to interface and ip informantion.
    Returns:
    dict: A dictionary containing the start_device, start_port, end_device, end_port, start_ipv4addr, end_ipv4addr.
    """
    # Open the CSV file and read its contents
    csv_file_path = rf"D:/gitpycode/working_code/mypycode/inventory/deviceinterfaceiptable.csv"
    interface_ip_table=[]
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        # Iterate over each row in the CSV file
        for row in reader:
            # Remove leading and trailing spaces from keys
            row = {k.strip(): v for k, v in row.items()}
            # Check if the device name is present in the start_device or end_device columns
            if device_name in row['start_device'] or device_name in row['end_device']:
                # Call the reverse_wiring function to get the interface details
                start_device, start_port, start_ipv4_addr, end_device, end_port, end_ipv4_addr = reverse_wiring(row, device_name)
                interface_ip_table.append({'start_device': start_device,'start_port': start_port, 'end_device': end_device, 'end_port': end_port, 'start_ipv4_addr': start_ipv4_addr, 'end_ipv4_addr': end_ipv4_addr})
        if not interface_ip_table:
            return (f'{device_name} not found in deviceinterfaceiptable.csv') 
    # Return a list containing the interfaces' configurations and list
    return {"interface_ip_table": interface_ip_table}

# Call the function and print the result
#config = interface_and_ip_table_reader('rtr02')
#pprint(config)

def generate_interface_config(device_name: str):
    """
    This function generates the configuration for a given device's interfaces.
    It reads the interface details from a CSV file and returns a dictionary containing the configurations and interface list.
    Parameters:
    device_name (str): The name of the device for which to generate the configuration.
    Returns:
    dict: A dictionary containing the interfaces' configurations and list.
    """
    interfaces_config = []
    interfaces_list = []
    # Open the CSV file and read its contents
    csv_file_path = r"D:\gitpycode\working_code\mypycode\inventory\deviceinterfaceiptable.csv"
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        # Iterate over each row in the CSV file
        for row in reader:
            # Remove leading and trailing spaces from keys
            row = {k.strip(): v for k, v in row.items()}
            # Check if the device name is present in the start_device or end_device columns
            if device_name in row['start_device'] or device_name in row['end_device']:
                # Call the reverse_wiring function to get the interface details
                start_device, start_port, start_ipv4_addr, end_device, end_port, end_ipv4_addr = reverse_wiring(row, device_name)
                interfaces_config.append([
                    f"interface {start_port}",
                    f"description Connected to {end_device} on {end_port}",
                    f"ip address {start_ipv4_addr} 255.255.255.252",
                    f"no proxy-arp",
                    f"no ip unreachable",
                    f"load-interval 30",
                    f"no shutdown",
                    f"!"
                ])

                # Append the interface name to the interfaces_list
                interfaces_list.append(start_port)
    if not interfaces_list:
        return (f'{device_name} not found in database.') 
    # Return a dictionary containing the interfaces' configurations and list
    return {"interfaces_config": interfaces_config, "interfaces_list": interfaces_list}

# Call the function and print the result
#config = generate_interface_config('rtr02')
#pprint(config)


def generate_interface_config_with_jinja(device_name: str):
    """
    This function generates the configuration for a given device's interfaces.
    It uses the interface_and_ip_table_reader function to get the interface details and returns a dictionary containing the configurations and interface list.
    Parameters:
    device_name (str): The name of the device for which to generate the configuration.
    Returns:
    dict: A dictionary containing the interfaces' configurations and list.
    """
    interfaces_config = []
    interfaces_list = []
    template_file='mypycode/Jinja/interface_template.j2'  
    # Call the interface_and_ip_table_reader function to get the interface details
    interface_ip_table = interface_and_ip_table_reader(device_name)
    if 'interface_ip_table' not in interface_ip_table:
        return (f'{device_name} not found in deviceinterfaceiptable.csv') 
    # Iterate over each row in the interface_ip_table
    for row in interface_ip_table['interface_ip_table']:
        row = {'start_port': row['start_port'], 'end_device': row['end_device'], 'end_port': row['end_port'], 'start_ipv4_addr': row['start_ipv4_addr']}
        with open(template_file) as f:
            cisco_template = Template(f.read(), keep_trailing_newline=True)
            interface_config = cisco_template.render(row)
        interfaces_config.append(interface_config)
        # Append the interface name to the interfaces_list
        interfaces_list.append(row['start_port'])
    # Return a dictionary containing the interfaces' configurations and list
    return {"interfaces_config": interfaces_config, "interfaces_list": interfaces_list}


# Call the function and print the result
#config = generate_interface_config_with_jinja('rtr03')
#pprint(config)





