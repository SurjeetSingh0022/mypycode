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
        
        net_connect = ConnectHandler(**router_r1)
        print('\n\n ## connecting on router #######' +router_r1['host'], '\n')
        show_int1 = net_connect.send_command('show ip int brief')
        print('## pre-check #######''\n' +show_int1)
        prompt = net_connect.find_prompt()
        net_connect.config_mode()
        output = net_connect.send_config_from_file(config_file='07_config.txt')
        show_int2 = net_connect.send_command('show ip int brief')
        print('## Post-check #######''\n' +show_int2)