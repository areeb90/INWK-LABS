from jinja2 import Environment, FileSystemLoader
import yaml

ENV = Environment(loader=FileSystemLoader('.'))
template = ENV.get_template("template-lab.j2")

with open("data-lab.yml") as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)
    print(template.render(routers=data['routers']))
