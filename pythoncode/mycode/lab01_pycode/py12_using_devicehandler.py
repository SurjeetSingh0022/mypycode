from handler import NetmikoDeviceHandler
from pprint import pprint as pp

def get_interfaces_status(device_name: str) -> str:
    try:
        handler = NetmikoDeviceHandler(device_name)
        connection = handler.connect()
        if connection is not None:
          output = connection.send_command('show version', use_textfsm=True)
          return output
    except Exception as e:
        return str(e)

pp(get_interfaces_status('192.168.2.13'))