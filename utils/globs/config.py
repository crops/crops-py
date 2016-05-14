from flask import json
from docker import Client

VERSION=0.1
CODI_IP="0.0.0.0"
CODI_PORT=10000
TURFF_IP="0.0.0.0"
TURFF_PORT=9999

def get_all_routes(app):
    d = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            doc = app.view_functions[rule.endpoint].__doc__
            if doc is not None:
                d[rule.rule] = doc.replace('\n', '<br/>&nbsp&nbsp') + "<br/>"
    return json.dumps(d)

def docker_connect(base_url='unix://var/run/docker.sock'):
    cli = Client(base_url)
    return cli

