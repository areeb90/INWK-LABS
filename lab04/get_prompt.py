from netmiko import Netmiko

device = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.101",
    "username": "student",
    "password": "Meilab123",
    "secret": "cisco",    # needed for enable() to work
    "port": "22",
}

net_connect = Netmiko(**device)

print(f"Default prompt: {net_connect.find_prompt()}")    # R01#

net_connect.send_command_timing("disable")
print(f"After disable: {net_connect.find_prompt()}")     # R01>

net_connect.enable()
print(f"After enable: {net_connect.find_prompt()}")      # R01#
