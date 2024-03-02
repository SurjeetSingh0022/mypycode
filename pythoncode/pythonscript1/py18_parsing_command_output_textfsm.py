from netmiko import ConnectHandler
from pprint import pprint as pp

''' Parsing device interface output using txtfsm ntpc template'''

device_info_dict = {}

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
        device_info= net_connect.send_command('show version',use_textfsm=True)
        net_connect.disconnect()
        l=len(int_out)

        # Extract list of interface device.
        inter_list=[]
        for i in int_out:
            inter_list.append(i['interface'])
        print("List of interfaces:", inter_list) 
       
        #Extract only up interfaces from device
        print("\nList of up interfaces on " + ip,)
        for i in range(0,l):
            if int_out[i]['status'] == 'up':
                print (int_out[i]['interface'] +" "+ int_out[i]['status'])

        #Extract only down interfaces from device    
        print("\nList of down interfaces on " + ip)
        for i in range(0,l):
            if int_out[i]['status'] != 'up':
                print (int_out[i]['interface'] +" "+ int_out[i]['status']) 


        
        # Extract relevant information from each device
        for info in device_info:
            hostname = info['hostname']
            version = info['version']
            serial_number = info['serial'][0]  # Assuming there's only one serial number
            running_image = info['running_image'][0]

            # Append information to the dictionary
            device_info_dict[hostname] = {
                'version': version,
                'serial_number': serial_number,
            }

print(device_info_dict)

# print hostname from our global device_info_dict       
print(f"Device Name: {hostname}")

# Extract the serial number for R1(for specific device)
r1_serial_number = device_info_dict.get('R1', {}).get('serial_number', 'N/A')
# Print the serial number
print(f"Serial Number for R1: {r1_serial_number}")


 
                   


'''[{'software_image': 'I86BI_LINUX-ADVENTERPRISEK9-M', 'version': '15.4(2)T4', 'release': '', 'rommon': 'Bootstrap', 
'hostname': 'R2', 'uptime': '4 days, 10 hours, 44 minutes', 'uptime_years': '', 'uptime_weeks': '', 'uptime_days': '4', 'uptime_hours': '10', 'uptime_minutes': '44',
 'reload_reason': 'Unknown reason', 'running_image': '/opt/unetlab/addons/iol/bin/L3-ADVENTERPRISEK9-M-15.4-2T.bin', 'hardware': [], 'serial': ['67108896'], 
 'config_register': '0x0', 'mac_address': [], 'restarted': ''}]'''

  
             
   
       
