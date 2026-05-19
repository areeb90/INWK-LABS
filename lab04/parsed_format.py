from netmiko import Netmiko

device = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.101",
    "username": "student",
    "password": "Meilab123",
    "port": "22"
}

net_connect = Netmiko(**device)

output = net_connect.send_command("show ip interface brief", use_textfsm=True)

print(f"{'Interface':<25} {'IP Address':<20} {'Status':<25} {'Protocol'}")
print("-" * 80)
for interface in output:
    print(f"{interface['interface']:<25} {interface['ip_address']:<20} {interface['status']:<25} {interface['proto']}")

net_connect.disconnect()
