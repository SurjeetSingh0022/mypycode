from netmiko import ConnectHandler
from pprint import pprint as pp

''' Parsing device interfaces output using txtfsm ntpc template
' in this code we will use for loop and list comprehension to print
' all up and all down interface seprately'''

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
        #pp(int_out)
        
        # 1st method of printing up interfaces and their status
        for ifname in int_out:
            if ifname['status'] == 'up':
                up_int=ifname['interface'] +" "+ ifname['status']
                pp(up_int)

        # 2st method of printing up interfaces and their status
        up_int_list=[]        
        for ifname in int_out:
            if ifname['status'] == 'up':
                up_int_list.append(ifname['interface'] +" "+ ifname['status'])
        pp(up_int_list)
      
        # 3rd method of printing up interfaces using comprehension method
        print('list of up interfaces')
        pp([ifname['interface']+" "+ (ifname['status']) for ifname in int_out if ifname['status'] == 'up'])
        print('\nlist of down interfaces')
        pp([ifname['interface']+" "+ (ifname['status']) for ifname in int_out if ifname['status'] != 'up'])