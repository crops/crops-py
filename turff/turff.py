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
from flask import jsonify
from flask import request
from utils.globs import config

app = Flask(__name__)

@app.route('/turff/', methods = ['GET'])
def api_list():
    '''Show TURFF API
    args: None
    returns: List of all registered routes in JSON format
    '''
    return config.get_all_routes(app)

@app.route('/turff/version', methods=['GET'])
def get_version():
    '''Show TURFF version
    args: None
    returns: TURFF version in JSON format
    '''
    return jsonify(version=config.VERSION)

if __name__ == '__main__':
    app.run(host=config.TURFF_IP, port=config.TURFF_PORT, debug=True)
