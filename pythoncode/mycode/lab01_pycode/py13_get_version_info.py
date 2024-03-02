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

output=(get_interfaces_status('192.168.2.13'))

# initaite empty list to get hostname,version,serial number and uptime

device_info=[]

# Itrate over output to get the information
for item in output:
    hostname = item.get('hostname', 'N/A')
    version = item.get('version', 'N/A')
    serial = item.get('serial', ['N/A'])[0]
    uptime = item.get('uptime', ['N/A'])
    device_info.append(f'Hostname: {hostname}, Version: {version}, Serial Number: {serial}, Device uptime: {uptime}')
    ## print(f'Hostname: {hostname}, Version: {version}, Serial Number: {serial}, Device uptime: {uptime}')

print(device_info)

'''[{'config_register': '0x0',
  'hardware': [],
  'hostname': 'R1',
  'mac_address': [],
  'release': '',
  'reload_reason': 'Unknown reason',
  'restarted': '',
  'rommon': 'Bootstrap',
  'running_image': '/opt/unetlab/addons/iol/bin/L3-ADVENTERPRISEK9-M-15.4-2T.bin',
  'serial': ['67108880'],
  'software_image': 'I86BI_LINUX-ADVENTERPRISEK9-M',
  'uptime': '1 day, 6 hours, 55 minutes',
  'uptime_days': '1',
  'uptime_hours': '6',
  'uptime_minutes': '55',
  'uptime_weeks': '',
  'uptime_years': '',
  'version': '15.4(2)T4'}]'''