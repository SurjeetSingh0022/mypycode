import getpass
import telnetlib
from netmiko import ConnectHandler
from creds import username, password

class CiscoDevice:
    def __init__(self, device_name):
        self.device_name = device_name
        self.username = username
        self.password = password

    def connect_ssh(self):
        device = {
            'device_type': 'cisco_ios',
            'host': self.device_name,
            'username': self.username,
            'password': self.password,
        }
        try:
            return ConnectHandler(**device)
        except Exception as e:
            print(f"Cannot connect via SSH to {self.device_name}: {e}")
            return None

    def connect_telnet(self):
        device_name='vracks.lab.local'
        telnet_port = input("Enter the Telnet port (default is 23): ")
        if not telnet_port:
            telnet_port = 23

        try:
            tn = telnetlib.Telnet(device_name, port=int(telnet_port), timeout=5)
            tn.write(b"\n")
            tn.read_until(b"Username: ")
            tn.write(self.username.encode('ascii') + b"\n")
            tn.read_until(b"Password: ")
            tn.write(self.password.encode('ascii') + b"\n")
            return tn
        except Exception as e:
            print(f"Cannot connect via Telnet to {device_name}: {e}")
            return None

# Usage:
handler = CiscoDevice('192.168.2.13')
ssh_connection = handler.connect_ssh()
if ssh_connection:
    output = ssh_connection.send_command('show ip int brief')
    print(output)
else:
    telnet_connection = handler.connect_telnet()
    if telnet_connection:
        telnet_connection.write(b"show ip int brief\n")
        print(telnet_connection.read_all().decode('ascii'))
    else:
        print("Both SSH and Telnet connections failed.")