#!/usr/bin/env python
"""Creates a Ansible Inventory in Ansible Tower """

import os
from jinja2 import Template
import yaml


def read_file(read_site):
    """Read a site file """
    with open("./sites/" + read_site + "/prometheus_variables.yaml", 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print exc


def convert_yaml(convert_site, yaml_data):
    """Convert yaml to json """
    all_hosts = []
    all_hosts.append(yaml_data['director'])
    all_hosts.extend(yaml_data['controllers'] + yaml_data['computes'] +
                     yaml_data['tenants'] + yaml_data['rhvs'])
    json_template = Template('''
    {
        "site_{{ site }}": {
            "hosts": {{ all_hosts }},
            "vars": {
                "coordinates": "{{ coordinates }}",
                "environment": "production",
                "directors": "{{ director }}",
                "controllers": "{{ controllers }}",
                "computes": "{{ computes }}",
                "tenants": "{{ tenants }}",
                "rhvs": "{{ rhvs }}",
            }
        },
        "_meta": {
        }
    }''')
    return json_template.render(
        site=convert_site,
        coordinates=yaml_data['coordinates'],
        all_hosts=all_hosts,
        director=yaml_data['director'],
        controllers=yaml_data['controllers'],
        computes=yaml_data['computes'],
        tenants=yaml_data['tenants'],
        rhvs=yaml_data['rhvs']
    )


if __name__ == '__main__':
    SITES = os.listdir("./sites")
    for site in SITES:
        site_yaml = read_file(site)
        site_json = convert_yaml(site, site_yaml)
        print site_json
