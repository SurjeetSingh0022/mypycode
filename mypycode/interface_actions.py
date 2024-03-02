import logging
from typing import List
from handler import NetmikoDeviceHandler
from pprint import pprint

CMD_SHOW_RUN_INTERFACE ="show running-config interface {interface}"

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class interfaceActions:
    def __init__(self, connection, device_name):
        self.connection = connection
        self.device_name = device_name


    def get_interface_config(device_name:str, interfaces: list):
        ''' This function will get interface running config
            param: device_name or ip as string
            param: interface/interfaces s as list
            result: interfaces_config and interfaces_list in list format'''
        try:
            handler = NetmikoDeviceHandler(device_name)
            connection = handler.connect()
            interfaces_config = []
            interfaces_list = interfaces
            for interface in interfaces:
                config = connection.send_command(CMD_SHOW_RUN_INTERFACE.format(interface=interface))
                if config:
                    interfaces_config.append(config)
            if interfaces_config:
                return {"interfaces_config": interfaces_config, "interfaces_list": interfaces_list} 
            else:
                return f"Failed to get interface {interface} config"
        except Exception as e:
            return f'failed to get interface config due to Error: {e}'


    def reset_interface_config(interfaces: list):
        ''' This function will reset the interface to default
            param: device_name or ip as string
            param: interface/interfaces s as list
            result: interfaces_config and interfaces_list in list format'''
        try:
            reset_interface_config=[]
            interfaces_list = interfaces
            for interface in interfaces:
                reset_interface_config.append([
                f'default interface {interface}',
                f'interface {interface}',
                f'load-interval 30',
                f'no shutdown'    
                ])
            if reset_interface_config:
                return {"reset_interface_config": reset_interface_config, "interfaces_list": interfaces_list} 
        except Exception as e:
            return f'failed to generate reset interface config due to Error: {e}'


    def disable_interface(interfaces: list):
        ''' This function will shutdown the interface
            param: device_name or ip as string
            param: interface/interfaces s as list
            result: interfaces_config and interfaces_list in list format'''
        try:
            disable_interface_config=[]
            interfaces_list = interfaces
            for interface in interfaces:
                disable_interface_config.append([
                    f'interface {interface}',
                    f'shutdown'    
                    ])
            if disable_interface_config:
                return {"disable_interface_config": disable_interface_config, "interfaces_list": interfaces_list} 
            else:
                return f"Failed to generate {interface} disable config"
        except Exception as e:
            return f'failed to get disable config due to Error: {e}'
        

    def enable_interface(interfaces: list):
        ''' This function will shutdown the interface
            param: device_name or ip as string
            param: interface/interfaces s as list
            result: interfaces_config and interfaces_list in list format'''
        try:
            enable_interface_config=[]
            interfaces_list = interfaces
            for interface in interfaces:
                enable_interface_config.append([
                    f'interface {interface}',
                    f'shutdown'    
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
            interface_list = []
            interface_ip_list = {}
            interface_status_list = {}
            output = connection.send_command('show ip inter brief', use_textfsm=True)
            if output is not None:
                for item in output:
                    interface_list.append(item['interface'])
                    interface_ip_list[item['interface']] = item['ip_address']
                    interface_status_list[item['interface']] = item['proto']
                if interface_list:
                    return {"interface_list": interface_list, "interface_ip_list": interface_ip_list, "interface_status_list": interface_status_list}       
        except Exception as e:
            return f'failed to get interface list due to Error: {e}' 

## execution to test above function    
#config = interfaceActions.get_device_interface_list(device_name='192.168.2.21')
#pprint(config['interface_status_list'])    
    
class InterfaceActions:
    def __init__(self, connection, device_name):
        self.connection = connection
        self.device_name = device_name

    def get_interface_running_config(self, interface: str) -> str:
        ''' send command to get interface running-config/current config
            param: device_name 
            param: interface number "eth0/0"'''
        try:
            output = self.connection.send_command(CMD_SHOW_RUN_INTERFACE.format(interface=interface))
        except Exception as e:
            logger.exception(f"{self.device_name}: Exception while retriving interface {interface} config.")
        if output is None:
            logger.exception("output for who interface is none. interface: {0}".format(interface))
            raise Exception("output for who interface is none. interface: {0}".format(interface))
        return output
    


    def get_interface_default_config_set(self, interface: str) -> List[str]:
        ''' 
        Generate a list of commands to reset the interface to its default configuration.
        param: interface: The name of the interface, e.g., "eth0/0"
        return: A list of commands as strings
        '''
        return [
            f'default interface {interface}',
            f'interface {interface}',
            'load-interval 30',
            'no shutdown'
        ]
    
    #def reset_interface_config(self, interface: str) -> bool:
    #    ''' 
    #    Reset the interface configuration to its default state.
    #    param: interface: The name of the interface, e.g., "eth0/0"
    #    return: True if the operation was successful, False otherwise
    #    '''
    #    try:
    #        config_set = self.get_interface_default_config_set(interface)
    #        self.connection.send_config_set(config_set)
    #        return True
    #    except Exception as e:
    #        if '% Interface does not exist' in str(e):
    #            logger.info(f'{interface} does not exist')
    #            return False
    #        logger.exception(f"{self.device_name}: Exception while resetting interface {interface} config.")
    #        raise
#
    def ios_disable_interface(self, interface: str) -> List[str]:
        ''' 
        shutdown the interface.
        param: interface: The name of the interface, e.g., "eth0/0"
        return: A list of commands as strings
        '''
        return [
            f'interface {interface}',
            'shutdown'
        ]



    def unshut_interface(self, interface: str) -> bool:
        ''' 
        un-shutdown/no shutdown the interface.
        param: interface: The name of the interface, e.g., "eth0/0"
        return: True if the operation was successful, False otherwise
        '''
        try:
            config_set = [
            f'interface {interface}',
            'no shutdown'
        ]
            self.connection.send_config_set(config_set)
            return config_set
        except Exception as e:
            if '% Interface does not exist' in str(e):
                logger.info(f'{interface} does not exist')
                return False
            logger.exception(f"{self.device_name}: Exception while shutting interface {interface},")
            raise



