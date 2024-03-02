import ipaddress

# Ask the user for the subnet
subnet_input = input("Please enter the site subnet: ")

# Use the input to create the network
site_subnet = ipaddress.ip_network(subnet_input)

# Initialize VLANs dictionary
vlans = {
    9: 'WAN-Transit',
    10: 'Admin',
    20: 'HR',
    30: 'IT',
    40: 'Marketing',
    50: 'SAP'
}

vlan_config = []

# Iterate over subnets and VLANs
for subnet, (vlan_id, vlan_name) in zip(site_subnet.subnets(new_prefix=26), vlans.items()):
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