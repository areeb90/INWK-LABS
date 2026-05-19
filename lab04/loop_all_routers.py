from netmiko import Netmiko

routers = ["192.168.1.101", "192.168.1.102", "192.168.1.103", "192.168.1.104"]

for ip in routers:
    device = {
        "device_type": "cisco_ios",
        "ip": ip,
        "username": "student",
        "password": "Meilab123",
        "secret": "cisco",
        "port": "22",
    }
    net_connect = Netmiko(**device)
    print(f"{ip} → {net_connect.find_prompt()}")
    net_connect.disconnect()
