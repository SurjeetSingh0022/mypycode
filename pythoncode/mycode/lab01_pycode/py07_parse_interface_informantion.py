from handler import NetmikoDeviceHandler
import ipaddress

username="admin"
password="admin"
#device_name=input("Enter Device IP to Connect : ")

def send_commands(device_name: str) -> str:
    try:
        handler = NetmikoDeviceHandler(device_name)
        connection = handler.connect()
        if connection is not None:
          output = connection.send_command('show ip int bri')
          return output
    except Exception as e:
        return str(e)

output=send_commands("192.168.2.21")

def parse_interfaces(output):
    # Split the output into lines
    lines = output.split('\n')

    # Initialize list and dictionary
    interfaces = []
    interface_ips = {}

    # Iterate over the lines
    for line in lines:
        # Split the line into words
        words = line.split()

        # Check if the line has the correct format
        if len(words) >= 4:
            try:
                ipaddress.ip_address(words[1])
                # Add the interface to the list
                interfaces.append(words[0])

                # Add the interface and IP to the dictionary
                interface_ips[words[0]] = words[1]
            except ValueError:
                pass

    return interfaces, interface_ips

interfaces, interface_ips = parse_interfaces(output)

print("Interfaces:", interfaces)
print("Interface IPs:", interface_ips)