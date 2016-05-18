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
import requests

class Turff():
    '''Turff is a toolchain description utility'''

    def load_json(self, j_file):
        '''Load JSON toolchain descriptor
        j_file: JSON file name
        returns: JSON object
        '''
        try:
            with open(j_file) as json_data:
                return json.load(json_data)
        except IOError:
            return None

    def send_registration(self, url, j_data):
        '''Send JSON toolchain registration to codi
        url: codi toolchain registration URL
        j_data: JSON object
        returns: JSON object
        '''
        return requests.post(url, json=j_data)

