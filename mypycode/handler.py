from netmiko import ConnectHandler
from creds import username, password

class NetmikoDeviceHandler:
    def __init__(self, ip):
        self.device_type = 'cisco_ios'
        self.device_name = ip
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