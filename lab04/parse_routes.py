from netmiko import Netmiko

device = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.101",
    "username": "student",
    "password": "Meilab123",
    "port": "22"
}

net_connect = Netmiko(**device)

output = net_connect.send_command("show ip route", use_textfsm=True)

print(f"{'Protocol':<12} {'Network':<20} {'Distance':<12} {'Metric'}")
print("-" * 60)
for route in output:
    print(f"{route['protocol']:<12} {route['network']:<20} {route['distance']:<12} {route['metric']}")

net_connect.disconnect()
