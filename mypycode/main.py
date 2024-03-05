from handler import NetmikoDeviceHandler
from handler import ConsoleTelnet
from core_actions import *
from pprint import pprint
import time


# Example usage
#device_base_config=generate_base_config('RTR01')
#pprint(device_base_config)
        
# Example usage
#inteface_running_config=InterfaceActions.get_interface_running_config('192.168.2.21',['Ethernet0/1'])
#pprint(inteface_running_config)        

# Example usage
#config=InterfaceActions.reset_interface_config('192.168.2.21',interfaces=['Ethernet0/4','Ethernet0/2'])
#config=config['reset_interface_config']
#pprint(config)

# Example usage
#config=InterfaceActions.disable_interface('192.168.2.21',interfaces=['Ethernet0/2','Ethernet0/3'])
#print(config)

# Example usage
#config=interfaceActions.enable_interface(interfaces=['eth0/1','eth0/2'])
#config=config['enable_interface_config']  

# Example usage
# execution to test above function    
#config = interfaceActions.get_device_interface_list(device_name='192.168.2.21')
#pprint(config['interface_status_list'])                            

def push_config(device_name:str, config: list):
    ''' This function will push the configuration to the device
        param: device_name or ip as string
        param: config_list as list
        result: True if successful, False otherwise'''
    try:
        handler = NetmikoDeviceHandler(device_name)
        connection = handler.connect()
        # Flatten the list of lists into a list of strings
        updated_config = [item for sublist in config for item in sublist]
        updated_config.append('do wri memory')
        pprint(updated_config)
        # Ask user for confirmation before pushing the config
        user_input = input("Are you sure you want to push the config? (yes/no): ")
        if user_input.lower() != "yes":
            print("Operation cancelled by user.")
            return False

        out = connection.send_config_set(updated_config)
        print(out)
        # Return True to indicate success
        return True
    except Exception as e:
        # Print an error message and return False
        print(f"Error pushing config: {str(e)}")
        return False

# Assume 'ssh_handler' is the device handler
#result = push_config('192.168.2.21', config)
#if result:
#    print("Config successfully pushed to the device.")
#else:
#    print("Failed to push config to the device.")
    

# Example usage
#device_base_config=generate_device_base_config('RTR01')
#pprint(device_base_config)

def device_onboarding_config(device_name, telnet_port):
    TELNET_TIMEOUT= 10
    tn_handler= ConsoleTelnet(device_name, telnet_port)  # Create an instance of ConsoleTelnet
    connection = tn_handler.connect()
    if connection is not None:
        tn_handler.initial_connection()  # Call initial_connection on the instance, not the class
        connection.tn.write(b'Configure terminal \n')
        print(f'Device is in Configuration mode.')
        config=generate_device_base_config(device_name)
        if config is not None:
            print(f'device config has been generated for {device_name}')
        with open(rf'D:\gitpycode\working_code\mypycode\device_onboarding_config\{device_name}.conf' , 'r') as cmd_file:
            for cmd in cmd_file.readlines():
                cmd.strip('\r\n')
                config=connection.tn.write(cmd.encode()+ b'\r')  # Call 'write' on the 'tn' attribute of the 'ConsoleTelnet' object
                time.sleep(2)
                # Check for syntax errors
                output = connection.tn.read_until(b'\n', timeout=TELNET_TIMEOUT).decode()
                if 'Invalid input detected' in output:
                    print(f'Syntax error in command: {cmd}')
                    return False
        print("Config successfully pushed to the device.")
        return True  # Return True if the configuration was successfully pushed
    else:
        print("Failed to connect to the device.")
        return False  # Return False if the connection was not successful

# Assume 'Console_Telnet' is the device handler
result = device_onboarding_config('rtr03', 32771)
if result:
    print("Config successfully pushed to the device.")
else:
    print("Failed to push config to the device.")             







