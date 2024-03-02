from pprint import pprint as pp
from handler import NetmikoDeviceHandler
from pprint import pprint as pp


def get_interfaces_status(device_name: str) -> str:
    try:
        handler = NetmikoDeviceHandler(device_name)
        connection = handler.connect()
        if connection is not None:
          output = connection.send_command('show cdp neighbor | be Device ID',use_textfsm=True)
          return output
    except Exception as e:
        return str(e)

neighbor_list=get_interfaces_status('192.168.2.13')

config=[]

for neighbor_dict in neighbor_list:
    # Append configuration commands to the list
    neighbor_name = neighbor_dict['neighbor'].split('.')[0]
    local_interface = neighbor_dict['local_interface'].replace('Uni ', '')
    remote_interface = neighbor_dict['neighbor_interface'].replace('Uni ', '')  # Remove "Uni" prefix
    config.append([
        f'interface  {local_interface}',
        f' description {neighbor_name}_{remote_interface}',
        f' ip address 192.168.10.1 255.255.255.0',
        f' no shutdown',
        f' no ip-redirect',
        f' no proxy-arp',
        f' no ip unreachable',
        f'!',
    ])

pp(config)

lldp_list=[] 

# Extract and print neighbor name, local interface, and remote interface
for neighbor_dict in neighbor_list:
    neighbor_name = neighbor_dict['neighbor'].split('.')[0]
    lldp_list.append(neighbor_name)
    local_interface = neighbor_dict['local_interface']
    lldp_list.append(local_interface)
    remote_interface = neighbor_dict['neighbor_interface'].replace('Uni ', '')  # Remove "Uni" prefix
    lldp_list.append(remote_interface)
    #print(f"Neighbor: {neighbor_name}, Local Interface: {local_interface}, Remote Interface: {remote_interface}")



