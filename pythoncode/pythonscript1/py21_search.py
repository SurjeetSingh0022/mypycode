from netmiko import ConnectHandler
from pprint import pprint as pp

''' Parsing device interfaces output using txtfsm ntpc template
' in this code we will use for loop and list comprehension to print
' all up and all down interface seprately'''

searchip=input('\nEnter the ip address you want to Search: ')

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
        
        # Search method to find the ip address 
        ipsearch=[ipaddr['interface']+" "+ (ipaddr['ip_address']) for ipaddr in int_out if ipaddr['ip_address'] == searchip]
        for ipout in ipsearch:     
            print(searchip +" belong to ifname  " + ipsearch[0].split()[0] +" of "+ip) # Splitting the string by space and taking the first part

                
