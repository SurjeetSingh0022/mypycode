import napalm
from tabulate import tabulate
from creds import username,password

def main():
    driver_ios = napalm.get_network_driver("ios")
    driver_iosxr = napalm.get_network_driver("iosxr")

    device_list = [
        ["192.168.2.13", "ios", "switch"],
        ["192.168.2.14", "ios", "router"],
    ]

    network_devices = []
    for device in device_list:
        hostname, device_type, _ = device
        device_details = {
            "hostname": hostname,
            "username": username,
            "password": password,
        }
        if device_type == "ios":
            network_devices.append(driver_ios(**device_details))
        elif device_type == "iosxr":
            network_devices.append(driver_iosxr(**device_details))

    devices_table = [["hostname", "vendor", "model", "uptime", "serial_number"]]
    

    for device in network_devices:
        print(f"Connecting to {device.hostname}...")
        try:
            device.open()
            print("Getting device facts")
            device_facts = device.get_facts()
            lldp=device.get_interfaces()
            print(lldp)
            devices_table.append(
                [
                    device_facts["hostname"],
                    device_facts["vendor"],
                    device_facts["model"],
                    device_facts["uptime"],
                    device_facts["serial_number"],
                ]
            )   
        except Exception as err:
            print(f"Error connecting to {device.hostname}: {err}")
        finally:
            device.close()

    print("Done.")
    print(tabulate(devices_table, headers="firstrow"))

if __name__ == "__main__":
    main()
