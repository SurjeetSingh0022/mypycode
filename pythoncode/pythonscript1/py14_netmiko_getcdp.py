from actions import get_cdp_neighbor_details
from pprint import pprint as pp

''' Get cdp information of list of devices using 
    using existing fuction created in action.py'''

device_list=['192.168.2.10','192.168.2.13','192.168.2.14']
for device in device_list:
    print('\n\n ######## Connecting to ' + device +'########### \n\n')
    cdp=get_cdp_neighbor_details(device)
    pp(cdp)