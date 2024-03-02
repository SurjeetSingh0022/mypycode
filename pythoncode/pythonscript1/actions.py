from netmiko import ConnectHandler
from netmiko import NetmikoTimeoutException
from creds import username, password

def get_cdp_neighbor_details(device_name):
    """
    get the CDP neighbor detail from the given device using SSH

    :param ip: IP address of the device
    :return:
    """
    try:
        # establish a connection to the device
        ssh_connection = ConnectHandler(
            device_type='cisco_ios',
            ip=device_name,
            username=username,
            password=password,
        )
    
        # enter enable mode
        ssh_connection.enable()

        # prepend the command prompt to the result (used to identify the local host)
        result = ssh_connection.find_prompt() + "\n"
    except Exception as err:
        return False, str(err)
    
    # execute the show cdp neighbor detail command
    # we increase the delay_factor for this command, because it take some time if many devices are seen by CDP
    result += ssh_connection.send_command("show cdp neighbor detail", delay_factor=2)

    # close SSH connection
    ssh_connection.disconnect()

    return result

# Example of Execution
#output= get_cdp_neighbor_details('192.168.2.12')
#print(output)