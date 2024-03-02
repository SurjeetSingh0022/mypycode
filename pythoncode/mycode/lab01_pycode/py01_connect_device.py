from netmiko import ConnectHandler

CSR = {
    'device_type': 'cisco_ios',
    'ip': '192.168.2.14',
    # Add your username and password
    'username': 'admin',
    'password': 'admin',
}

connection = ConnectHandler(**CSR)

output = connection.send_command('show ip interface brief')
print(output)