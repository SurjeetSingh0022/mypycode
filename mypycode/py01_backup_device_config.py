from handler import NetmikoDeviceHandler
import datetime

tnow=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 

def device_config_backup():
    try:
        # access device_inventory to get devices IP informantion
        with open (rf'D:\pythoncode\mycode\lab02_pycode\devices_inventory',"r") as rtr_list:
            for device in rtr_list:
                device=device.strip()
                print(f'\n Connecting to {device}')
                handler=NetmikoDeviceHandler(device)
                connection = handler.connect()
                if connection is not None:
                    # Execute commands
                    for command in commands:
                        output = connection.send_command(command)
                        print(output,'\n')
                        filename=(rf"D:\pythoncode\backups\lab02_config_backup_{device}_{tnow}")
                        try:
                            with open(filename, 'w') as save_file:
                                save_file.write(output)
                            print(f'Logs saved to {filename}')
                        except Exception as e:
                            print(e)        
                    # Close SSH connection
                    connection.disconnect()
    except Exception as e:
        print(f"Failed to connect to {device}: {e}")

# List of commands to execute
commands = ["terminal len 0","show run"]

#Excuting function to get logs
device_config_backup()