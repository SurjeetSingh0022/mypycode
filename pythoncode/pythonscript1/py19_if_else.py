from netmiko import ConnectHandler
from pprint import pprint as pp

''' Parsing device interface output using txtfsm ntpc template'''

with open('07_devices.txt') as device_list:
    for ip in device_list:
        ip=ip.strip()
        router_r1 = {
            'device_type': 'cisco_ios',
            'host':   ip,
            'username': 'admin',
            'password': 'admin',
        #    'port' : 8022,          # optional, defaults to 22
        #    'secret': 'secret',     # optional, defaults to ''
        }
        try:
            print('\n\n ## connecting on router #######' +router_r1['host'], '\n')
            net_connect = ConnectHandler(**router_r1)
        except Exception as err:
            print (err) 
            continue
        int_out = net_connect.send_command('show ip int bri',use_textfsm=True) 
        #Extract only up interfaces from device
        inter_name=int_out[1]['interface']
        status=int_out[1]['status']
        #print (int_out[1]['interface'] +" "+ int_out[1]['status'])
        if status == 'up':
            print ("finishing the script as primary interface " + inter_name+" is already up")
        else:
            config_commands = [ 'interface Ethernet0/2',
                    'no shut' ]
            int_out = net_connect.send_config_set(config_commands)
            net_connect.disconnect()
            print (int_out) 


