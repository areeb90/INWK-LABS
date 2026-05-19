import yaml
import logging
from netmiko import Netmiko

logging.basicConfig(
    filename='network_automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

hosts = yaml.load(open('topology_hosts.yml'), Loader=yaml.SafeLoader)

for host in hosts["hosts"]:
    try:
        print(f"\n{'='*70}")
        print(f"  Routing Table for {host['hostname']} ({host['name']})")
        print(f"{'='*70}")

        net_connect = Netmiko(
            host=host["name"],
            username=host["username"],
            password=host["password"],
            port=host["port"],
            device_type=host["type"],
            conn_timeout=20,
            global_cmd_verify=False,
        )

        output = net_connect.send_command("show ip route", use_textfsm=True)
        net_connect.disconnect()

        if isinstance(output, list) and len(output) > 0:
            print(f"{'Proto':<8} {'Network':<18} {'Prefix':<8} {'Distance':<10} {'Metric':<8} {'Next-Hop':<16} {'Interface'}")
            print("-" * 90)
            for route in output:
                proto    = route['protocol']
                network  = route['network']
                prefix   = route['prefix_length']
                distance = route['distance'] if route['distance'] else '-'
                metric   = route['metric']   if route['metric']   else '-'
                nexthop  = route['nexthop_ip'] if route['nexthop_ip'] else 'directly'
                iface    = route['nexthop_if']
                print(f"{proto:<8} {network:<18} /{prefix:<7} {distance:<10} {metric:<8} {nexthop:<16} {iface}")

        logger.info(f"Successfully collected routing table from {host['hostname']}")

    except Exception as e:
        print(f"ERROR on {host['name']}: {str(e)}")
        logger.error(f"Failed on {host['name']}: {str(e)}")

print(f"\n{'='*70}")
print("Done! Routing tables collected from all routers.")
print(f"{'='*70}")
