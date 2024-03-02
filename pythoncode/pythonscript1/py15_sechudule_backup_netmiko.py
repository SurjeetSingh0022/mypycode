import schedule
from netmiko import ConnectHandler
import datetime
import time

''' schedule device backup using netmiko and schedule library'''

# function to schedule backup
def backup():
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
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
                print ('Starting backup for device : ' + ip + ' at ' + str(timestamp))
            except Exception as err:
                print (err) 
                continue
            # Retrieve the running configuration
            output = net_connect.send_command('show running-config')
            filename = (f"backups\\py15_RTR_backup_"+ ip + "_" + str(timestamp))
            with open(filename, 'w') as save_file:
                save_file.write(output)
            
            # Disconnect from the device
            net_connect.disconnect()
            
            print("####### Configuration backup completed #######"+'\n\n')


schedule.every().minute.at(":00").do(backup)
while True:
    schedule.run_pending()
    time.sleep(1)            