import logging
import requests
from requests.auth import HTTPBasicAuth
import json
import yaml

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

USER = 'student'
PASS = 'Meilab123'

def set_interface(host, interface_name, ip, netmask):
    base_url = f'http://{host}/restconf/api/running/'
    url = base_url + f'interfaces/interface/{interface_name}'

    auth = HTTPBasicAuth(USER, PASS)
    headers = {
        'Accept': 'application/vnd.yang.data+json',
        'Content-Type': 'application/vnd.yang.data+json'
    }
    data = {
        "ietf-interfaces:interface": {
            "name": interface_name,
            "description": "Set via RESTCONF automation",
            "type": "iana-if-type:ethernetCsmacd",
            "enabled": "true",
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": ip,
                        "netmask": netmask
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    logging.info(f"Configuring {interface_name} on {host} with IP {ip}")
    response = requests.put(url, auth=auth, headers=headers, data=json.dumps(data))

    if response.status_code == 204:
        logging.info(f"[{host}] {interface_name} set to {ip} — SUCCESS")
    else:
        logging.error(f"[{host}] {interface_name} FAILED — {response.status_code}: {response.text}")

# Load YAML config
with open('routers.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Loop through each router and each interface
for router in config['routers']:
    host = router['management_ip']
    logging.info(f"=== Configuring {router['hostname']} ({host}) ===")
    for iface in router['interfaces']:
        set_interface(host, iface['name'], iface['ip'], iface['netmask'])
