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

from flask import Flask
from codi import codi
from codi import codiDB
from utils.globs import config

def register_codi_routes (app):
    app.add_url_rule('/codi/', 'api_list', codi.list_api)
    app.add_url_rule('/codi/version', 'get_version', codi.get_version)
    app.add_url_rule('/codi/list-toolchains', 'get_toolchains', codi.get_toolchains)
    app.add_url_rule('/codi/register-toolchain', 'add_toolchain', codi.add_toolchain, methods=['POST'])
    app.add_url_rule('/codi/find-image', 'find_image', codi.find_image)
    app.add_url_rule('/codi/pull-image', 'pull_image', codi.pull_image)
    app.add_url_rule('/codi/remove-image', 'remove-image', codi.remove_image)
    app.add_url_rule('/codi/remove-toolchain', 'remove_toolchain', codi.remove_toolchain)

if __name__ == '__main__':
    app = Flask(__name__)
    db = codiDB.CodiDB(config.CODI_DB)
    codi = codi.Codi(app, db)
    register_codi_routes(app)
    app.run(host=config.CODI_IP, port=config.CODI_PORT, debug=True)
