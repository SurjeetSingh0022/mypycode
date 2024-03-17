import logging
from typing import List
from handler import NetmikoDeviceHandler
from pprint import pprint

CMD_SHOW_RUN_INTERFACE ="show running-config interface {interface}"

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class InterfaceActions:
    def __init__(self, connection, device_name):
        self.connection = connection
        self.device_name = device_name


    def get_interface_running_config(device_name:str, interfaces: list):
        ''' This function will get interface running config
            param: device_name or ip as string
            param: interface/interfaces as list
            result: interfaces_config and interfaces_list in list format'''
        try:
            handler = NetmikoDeviceHandler(device_name)
            device_interfaces=InterfaceActions.get_device_interface_list(device_name)
            device_interfaces_list=device_interfaces['device_interfaces_list']
            connection = handler.connect()
            if connection is not None:
                interfaces_config = []
                interfaces_list = interfaces
                for interface in interfaces:
                    if interface not in device_interfaces_list:
                        print(f"Interface {interface} not found on the {device_name}")
                        print(f'List of interfaces available: {device_interfaces_list}')
                        continue
                    config = connection.send_command(CMD_SHOW_RUN_INTERFACE.format(interface=interface))
                    if config:
                        interfaces_config.append(config)
                if interfaces_config:
                    return {"interfaces_config": interfaces_config, "interfaces_list": interfaces_list} 
                else:
                    return f"Failed to get {interface} running config"
            else:
                return f'failed to connect device {device_name}.'    
        except Exception as e:
            return f"Failed to get {device_name}: {interface} running config.\n due to an error{e}"


    def reset_interface_config(device_name: str, interfaces: list):
        ''' This function will reset the interface to default
            param: device_name or ip as string
            param: interface/interfaces s as list
            result: interfaces_config and interfaces_list in list format'''
        try:
            device_interfaces=InterfaceActions.get_device_interface_list(device_name)
            device_interfaces_list=device_interfaces['device_interfaces_list']
            reset_interface_config=[]
            interfaces_list = interfaces
            for interface in interfaces:
                if interface not in device_interfaces_list:
                    print(f"Interface {interface} not found on the {device_name}")
                    print(f'List of interfaces available: {device_interfaces_list}')
                    continue                
                reset_interface_config.append([
                f'default interface {interface}',
                f'interface {interface}',
                f'load-interval 30',
                f'no shutdown'    
                ])
            if reset_interface_config:
                return {"reset_interface_config": reset_interface_config, "interfaces_list": interfaces_list} 
            else: 
                return f'failed to generate reset interface config for {device_name}'
        except Exception as e:
            return f'failed to generate reset interface config due to Error: {e}'


    def disable_interface(device_name: str, interfaces: list):
        ''' This function will shutdown the interface
            param: device_name or ip as string
            param: interface/interfaces s as list
            result: interfaces_config and interfaces_list in list format'''
        try:
            device_interfaces=InterfaceActions.get_device_interface_list(device_name)
            device_interfaces_list=device_interfaces['device_interfaces_list']
            disable_interface_config=[]
            interfaces_list = interfaces
            for interface in interfaces:
                if interface not in device_interfaces_list:
                    print(f"Interface {interface} not found on the {device_name}")
                    print(f'List of interfaces available: {device_interfaces_list}')
                    continue                
                disable_interface_config.append([
                    f'interface {interface}',
                    f'shutdown'
                    f'!'     
                    ])
            if disable_interface_config:
                return {"disable_interface_config": disable_interface_config, "interfaces_list": interfaces_list} 
            else:
                return f"Failed to generate {interface} disable config"
        except Exception as e:
            return f'failed to get disable config due to Error: {e}'
        

    def enable_interface(device_name: str, interfaces: list):
        ''' This function will shutdown the interface
            param: device_name or ip as string
            param: interface/interfaces s as list
            result: interfaces_config and interfaces_list in list format'''
        try:
            device_interfaces=InterfaceActions.get_device_interface_list(device_name)
            device_interfaces_list=device_interfaces['device_interfaces_list']
            enable_interface_config=[]
            interfaces_list = interfaces
            for interface in interfaces:
                if interface not in device_interfaces_list:
                    print(f"Interface {interface} not found on the {device_name}")
                    print(f'List of interfaces available: {device_interfaces_list}')
                    continue                
                enable_interface_config.append([
                    f'interface {interface}',
                    f'no shutdown' 
                    f'!'    
                    ])
            if enable_interface_config:
                return {"enable_interface_config": enable_interface_config, "interfaces_list": interfaces_list} 
            else:
                return f"Failed to generate {interface} enable config"
        except Exception as e:
            return f'failed to get enable config due to Error: {e}'
        

    def get_device_interface_list(device_name: str): 
        ''' This function will get list of available interfaces,
            their ip_address and status 
            i.e eth0/0,eth0/1
            param: device_name or ip as string
            result: interface list, interface_ip_list, interface_status_list'''
        try:
            handler = NetmikoDeviceHandler(device_name)
            connection = handler.connect()
            if connection is not None:
                device_interfaces_list = []
                device_interfaces_ip_list = {}
                device_interfaces_status_list = {}
                output = connection.send_command('show ip inter brief', use_textfsm=True)
                if output is not None:
                    for item in output:
                        device_interfaces_list.append(item['interface'])
                        device_interfaces_ip_list[item['interface']] = item['ip_address']
                        device_interfaces_status_list[item['interface']] = item['proto']
                    if device_interfaces_list:
                        return {"device_interfaces_list": device_interfaces_list, "device_interfaces_ip_list": device_interfaces_ip_list, "device_interfaces_status_list": device_interfaces_status_list}
                    else:
                        return f'failed to get interface list'
            else:
                return f'failed to connect device {device_name}.'         
        except Exception as e:
            return f'failed to get interface list due to Error: {e}'


## execution to test above function    
#config = InterfaceActions.get_device_interface_list(device_name='192.168.2.21')
#pprint(config['device_interfaces_list'])  


# Example usage
#inteface_running_config=InterfaceActions.get_interface_running_config('192.168.2.22',['Ethernet0/4'])
#pprint(inteface_running_config) 

# Example usage
#config=InterfaceActions.reset_interface_config('192.168.2.22',interfaces=['Ethernet0/4','Ethernet0/2'])
#config=config['reset_interface_config']
#pprint(config)

# Example usage
#config=InterfaceActions.disable_interface('192.168.2.22',interfaces=['Ethernet0/2','Ethernet0/3'])
#print(config)

# Example usage
#config=InterfaceActions.enable_interface('192.168.2.22',interfaces=['Ethernet0/1','Ethernet0/2'])
#config=config['enable_interface_config'] 
#pprint(config) 

# Example usage
# execution to test above function    
#config = InterfaceActions.get_device_interface_list(device_name='192.168.2.22')
#update=(config['interface_status_list'])
#pprint(update)  