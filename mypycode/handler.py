from netmiko import ConnectHandler
from creds import *
from telnetlib import Telnet
import time


class NetmikoDeviceHandler:
    def __init__(self, device_name):
        self.device_type = 'cisco_ios'
        self.device_name = device_name
        self.username = username
        self.password = password

    def connect(self):
        device = {
            'device_type': 'cisco_ios',
            'ip':   self.device_name,
            'username': self.username,
            'password': self.password,
            "timeout": 120,  # Set a longer initial timeout (adjust as needed)
            "global_delay_factor": 3,  # Increase the delay factor (adjust as needed)
        }
        try:
            return ConnectHandler(**device)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Usage:
#handler = NetmikoDeviceHandler('192.168.2.21')
#connection = handler.connect()
#if connection is not None:
#    output = connection.send_command('show ip int brief')
#    print(output)
        


class ConsoleTelnet:
    def __init__(self, device_name, telnet_port):
        self.host='vracks.lab.local'
        self.device_name = device_name
        self.port = telnet_port
        self.timeout = 10
        self.tn = None
        self.username = username
        self.password = password

    def connect(self):
        try:
            self.tn = Telnet(self.host, self.port, self.timeout)
            return self
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    def initial_connection(self):
        if self.tn is None:
            raise Exception("Not connected to the device. Please connect first.")
        self.tn.write(b"\n")
        self.tn.read_until(b"Would you like to enter the initial configuration dialog? [yes/no]:")
        self.tn.write(b"no\n")
        time.sleep(3)
        self.tn.read_until(b"Press RETURN to get started!")
        self.tn.write(b"\r")
        if self.tn.read_until(b">"):
            self.tn.write(b'enable\n') 
            if self.tn.read_until(b"#"):
                print(f'Connected Sucessfully to {self.device_name} on {self.port}')
            else:
                raise Exception(f'Failed to enter enable mode on {self.device_name} on {self.port}')
        else:
            raise Exception(f'Failed to connect to {self.device_name} on {self.port}')  

    def send_command(self,command):
        if self.tn is None:
            raise Exception("Not connected to the device. Please connect first.")
        self.tn.write(b"\r")
        self.tn.read_until(b"Username: ")
        self.tn.write(self.username.encode('ascii') + b"\n")
        if self.password:
            self.tn.read_until(b"Password: ")
            self.tn.write(self.password.encode('ascii') + b"\n")
            if self.tn.read_until(b">"):
                self.tn.write(b'enable\n') 
                if self.tn.read_until(b"#"):
                    print(f'Connected Sucessfully to {self.device_name} on {self.port}')
                else:
                    raise Exception(f'Failed to enter enable mode on {self.device_name} on {self.port}')
        elif self.tn.read_until(b"#"):
            print(f'Connected Sucessfully to {self.device_name} on {self.port}')                  
        self.tn.write(command.encode('ascii'))
        self.tn.write(b"\n")
        time.sleep(2)
        output = self.tn.read_very_eager().decode('ascii')
        return(output)


# Usage:
#handler = ConsoleTelnet('vracks.lab.local','32769')
#connection = handler.connect()
#if connection is not None:
#    output = connection.send_command('show ip int brief')
#
#print(output)