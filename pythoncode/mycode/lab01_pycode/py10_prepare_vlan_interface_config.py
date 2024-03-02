import ipaddress

# Ask the user for the subnet
subnet_input = input("Please enter the site subnet: ")

# Use the input to create the network
site_subnet = ipaddress.ip_network(subnet_input)

# Initialize VLANs dictionary with new_prefix values
vlans = {
    9: {'name': 'WAN-Transit', 'new_prefix': 29},
    10: {'name': 'Admin', 'new_prefix': 26},
    20: {'name': 'HR', 'new_prefix': 27},
    30: {'name': 'IT', 'new_prefix': 28},
    40: {'name': 'Marketing', 'new_prefix': 26},
    # Add more VLANs as needed
}

vlan_config = []

# Iterate over VLANs
for vlan_id, vlan_info in vlans.items():
    # Get the new_prefix for this VLAN
    new_prefix = vlan_info['new_prefix']
    vlan_name = vlan_info['name']

    # Create an iterator for the subnets with the new_prefix
    subnet_iter = iter(site_subnet.subnets(new_prefix=new_prefix))

    # Check if there are still subnets left in the iterator
    try:
        subnet = next(subnet_iter)
    except StopIteration:
        print(f"No more subnets available for VLAN {vlan_id}")
        break

    hostip = str(subnet.network_address + 1)
    subnetmask = str(subnet.netmask)
    # Append configuration commands to the list
    vlan_config.append([f'vlan {vlan_id}', f'name {vlan_name}'])
    vlan_config.append([
        f'interface vlan {vlan_id}',
        f'description {vlan_name}',
        f'ip address {hostip} {subnetmask}',
        f'no shutdown',
        f'!',
    ])

# Print the configuration commands
for config in vlan_config:
    print('\n'.join(config))
