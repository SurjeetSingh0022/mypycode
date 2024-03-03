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
        



from telnetlib import Telnet
import time

class ConsoleTelnet:
    def __init__(self, device_name, telnet_port):
        self.host='vracks.lab.local'
        self.device_name = device_name
        self.port = telnet_port
        self.timeout = 30
        self.tn = None

    def connect(self):
        try:
            self.tn = Telnet(self.host, self.port, self.timeout)
            return self
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def initial_connection(self, command):
        if self.tn is None:
            print("Not connected to the device. Please connect first.")
            return None
        self.tn.write(b"\n")
        self.tn.read_until(b"Would you like to enter the initial configuration dialog? [yes/no]:")
        self.tn.write(b"no\n")
        time.sleep(5)
        self.tn.read_until(b"Press RETURN to get started!")
        self.tn.write(b"\r")
        if self.tn.read_until(b">") or self.tn.read_until(b"#"):
            print(f'connected to device')
            self.tn.write(command.encode('ascii'))
            self.tn.write(b"\n")
            time.sleep(2)
            output = self.tn.read_very_eager().decode('ascii')
            return output
 
        self.tn.write(b"exit\n") 

# Usage:
handler = ConsoleTelnet('rtr01','32776')
connection = handler.connect()
if connection is not None:
    output = connection.initial_connection('show ip int brief')
    print(output)


