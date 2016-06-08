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
import hashlib
import requests
import argparse

class Turff():
    '''Turff is a toolchain description utility'''

    def load_json(self, j_file, docker_url):
        '''Load JSON toolchain descriptor
        j_file: JSON file name
        returns: JSON object
        '''
        try:
            #TODO: add ip and port number to json object
            md5 = hashlib.md5()
            with open(j_file) as json_data:
                raw_data = json_data.read()
            md5.update(raw_data.encode('utf-8'))
            hex_md5 = md5.hexdigest()

            with open(j_file) as json_data:
                jdata= json.load(json_data)
            jdata['id'] = hex_md5
            jdata['docker'] = docker_url
            return jdata
        except (IOError, ValueError) as e:
            return None

    def send_registration(self, url, j_data):
        '''Send JSON toolchain registration to codi
        url: codi toolchain registration URL
        j_data: JSON object
        returns: JSON object
        '''
        return requests.post(url, json=j_data)

    def get_arg_parser(self):
        '''Create TURFF command line argument parser
        returns: turff arguments
        '''
        parser = argparse.ArgumentParser(
                description='TURFF command line arguments')
        parser.add_argument('--ip', default="0.0.0.0",
                help='codi ip address (default: 0.0.0.0)')
        parser.add_argument('--port', default=10000, type=int,
                help='codi port (default: 10000)')
        parser.add_argument('--jsonRoot', default="/opt/poky/.crops/",
                help='root directory for json descriptors (default:/opt/poky/.crops)')
        parser.add_argument('--dockerURL', default="unix:///var/run/docker.sock",
                help='Docker Engine URL (default:unix:///var/run/docker.sock)')
        return parser.parse_args()
