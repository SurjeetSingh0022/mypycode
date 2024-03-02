from netmiko import ConnectHandler

''' netmiko to send commands on list for device using host ip from text file'''

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
            print('\n\n ## connecting on router #######' +router_r1['host'], '\n')
            show_int1 = net_connect.send_command('show ip int brief')
            print('## pre-check #######''\n' +show_int1)
            config_commands = [ 'interface loopback200',
                                'ip address 200.1.1.1 255.255.255.255',
                                'no shut' ]
            output = net_connect.send_config_set(config_commands)
            show_int2 = net_connect.send_command('show ip int brief')
            print('## Post-check #######''\n' +show_int2)
        except Exception as err:
            print (err)    