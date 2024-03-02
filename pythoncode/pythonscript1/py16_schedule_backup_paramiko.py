import schedule
from main import send_commands
import datetime
import time

''' schedule device backup using paramiko and schedule library'''

# function to schedule backup
def backup():
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    with open('07_devices.txt') as device_list:
        for ip in device_list:
            ip=ip.strip()
            try:
                output = send_commands( ip,'show running-config')
                print ('Starting backup for device : ' + ip + ' at ' + str(timestamp))
            except Exception as err:
                print (err) 
                continue
            filename = (f"backups\\py16_RTR_backup_"+ ip + "_" + str(timestamp))
            with open(filename, 'w') as save_file:
                save_file.write(output)
            
            # Disconnect from the device
            #send_commands.close()
            
            print("####### Configuration backup completed #######"+'\n\n')


schedule.every().minute.at(":00").do(backup)
while True:
    schedule.run_pending()
    time.sleep(1)            