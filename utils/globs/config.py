#
# Copyright (C) 2016 Intel Corporation
#
# Author: Todor Minchev <todor.minchev@linux.intel.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU General Public License,
# version 2, or (at your option) any later version, as published by
# the Free Software Foundation.
#
# This program is distributed in the hope it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.

from flask import json
from docker import Client

VERSION=0.1
CODI_IP="0.0.0.0"
CODI_PORT=10000
TURFF_IP="0.0.0.0"
TURFF_PORT=9999
JSON_ROOT= "/opt/poky/.crops/"
REG_URL= "http://0.0.0.0:10000/codi/register-toolchain"

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

