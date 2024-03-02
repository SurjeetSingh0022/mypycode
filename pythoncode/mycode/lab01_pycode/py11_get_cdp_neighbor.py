from netmiko import ConnectHandler
from pprint import pprint as pp


with open(r'D:\pythoncode\mycode\device_inventory','r') as device_inventory:
    for router in device_inventory:
        router=router.strip()
        devices = {
            'device_type': 'cisco_ios',
            'ip': router,
            # Add your username and password
            'username': 'admin',
            'password': 'admin',
        }

connection = ConnectHandler(**devices)

neighbor_list = connection.send_command('show cdp neighbor | be Device ID',use_textfsm=True)

config=[]

for neighbor_dict in neighbor_list:
    # Append configuration commands to the list
    neighbor_name = neighbor_dict['neighbor'].split('.')[0]
    local_interface = neighbor_dict['local_interface'].replace('Uni ', '')
    remote_interface = neighbor_dict['neighbor_interface'].replace('Uni ', '')  # Remove "Uni" prefix
    config.append([
        f'interface  {local_interface}',
        f'description {neighbor_name}_{remote_interface}',
        f'!',
    ])
lldp_list=[] 

# Extract and print neighbor name, local interface, and remote interface
for neighbor_dict in neighbor_list:
    neighbor_name = neighbor_dict['neighbor'].split('.')[0]
    lldp_list.append(neighbor_name)
    local_interface = neighbor_dict['local_interface']
    lldp_list.append(local_interface)
    remote_interface = neighbor_dict['neighbor_interface'].replace('Uni ', '')  # Remove "Uni" prefix
    lldp_list.append(remote_interface)
    print(f"Neighbor: {neighbor_name}, Local Interface: {local_interface}, Remote Interface: {remote_interface}")


pp(config)