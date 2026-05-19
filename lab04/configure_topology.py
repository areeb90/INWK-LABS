import yaml
import logging
from jinja2 import Environment, FileSystemLoader
from netmiko import Netmiko

# Question 4 - Setup Logger
logging.basicConfig(
    filename='network_automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load YAML
hosts = yaml.load(open('topology_hosts.yml'), Loader=yaml.SafeLoader)

# Setup Jinja2
env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, autoescape=False)
template = env.get_template('topology_config.j2')

# Loop over each router
for host in hosts["hosts"]:
    try:
        # Render config for this specific host
        config = template.render(host=host)

        logger.info(f"Connecting to {host['name']} ({host['hostname']})")
        print(f"\nConnecting to {host['name']} ({host['hostname']})...")

        net_connect = Netmiko(
            host=host["name"],
            username=host["username"],
            password=host["password"],
            port=host["port"],
            device_type=host["type"]
        )

        print(f"Logged into {host['name']} successfully")
        logger.info(f"Logged into {host['name']} successfully")

        output = net_connect.send_config_set(config.split("\n"))

        print(f"Config pushed to {host['name']} successfully")
        logger.info(f"Config pushed to {host['name']} successfully")

        net_connect.disconnect()

    except Exception as e:
        print(f"ERROR on {host['name']}: {str(e)}")
        logger.error(f"Failed on {host['name']}: {str(e)}")

print("\nDone!")
logger.info("Script completed")
