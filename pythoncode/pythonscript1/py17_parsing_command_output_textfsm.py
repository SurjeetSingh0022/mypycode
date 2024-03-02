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
            net_connect = ConnectHandler(**router_r1)
        except Exception as err:
            print (err) 
            continue
        print('\n\n ## connecting on router #######' +router_r1['host'], '\n')
        int_out = net_connect.send_command('show ip int bri',use_textfsm=True)
        print(" interface list and their details for "+ ip)
        pp(int_out)
        net_connect.disconnect()
        

        # Extract the interface names
        interface_names = [entry['interface'] for entry in int_out]
        # Print the interface names
        print("interface list on Device:"+ip)
        for name in interface_names:
           print(name)
       
