from netmiko import ConnectHandler
from actions import get_cdp_neighbor_details
from pprint import pprint as pp

router_r1 = {
    'device_type': 'cisco_ios',
    'host':   '192.168.2.13',
    'username': 'admin',
    'password': 'admin',
#    'port' : 8022,          # optional, defaults to 22
#    'secret': 'secret',     # optional, defaults to ''
}

net_connect = ConnectHandler(**router_r1)
show_int1 = net_connect.send_command('show ip int brief')
print('## pre-check #######''\n' +show_int1)
config_commands = [ 'interface loopback200',
                    'ip address 200.1.1.1 255.255.255.255',
                    'no shut' ]
output = net_connect.send_config_set(config_commands)
show_int2 = net_connect.send_command('show ip int brief')
print('## Post-check #######''\n' +show_int2)

device_name='192.168.2.14'
cdp=get_cdp_neighbor_details(device_name)
pp(cdp)
