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

from flask import jsonify
from flask import json
from flask import request
from flask import Response
from utils.globs import config
from utils.docker import dcrops
from codi import codiDB
import argparse

class Codi() :
    '''Codi is used to track toolchains and manage Docker images

    Args: app (Flask): Instance of a Flask application
    '''

    def __init__(self, flask_app):
        '''Initialize Codi with a flask app instance variable'''
        self.app = flask_app
        self.db = codiDB.CodiDB(config.CODI_DB)

    def list_api(self):
        '''Show CODI API [GET]
        args: None
        returns: List of all registered routes in JSON format
        '''
        return config.get_all_routes(self.app)

    def get_version(self):
        '''Show CODI version [GET]
        args: None
        returns: TURFF version in JSON format
        '''
        return jsonify(version=config.VERSION)

    def get_toolchains(self):
        '''List toolchains in CODI database [GET]
        filter: toolchain filter
        returns: List of all known toolchains in JSON format
        '''
        if request.method == 'GET':
            filter = request.args.get("filter")
            response = self.db.db_select(config.TOOLCHAINS_TBL, filter)
        return Response(json.dumps(list(response)),  mimetype='application/json')

    def add_toolchain(self):
        '''Add toolchain to the CODI database [POST]
        json: toolchain json descriptor
        returns: registration status
        '''
        if request.method == 'POST':
            json_data = request.get_json()
            json_data["client_ip"] = request.remote_addr
            response = self.db.db_insert(config.TOOLCHAINS_TBL, json_data)
            if response is not None:
                response = Response(json.dumps(list(response)),  mimetype='application/json')
                response.status_code = 200
            else:
                response = Response(json.dumps(list(response)),  mimetype='application/json')
                response.status_code = 400
        else:
            response = Response(json.dumps(list(response)),  mimetype='application/json')
            response.status_code = 400
        return response

    def find_image(self):
        '''Search for a toolchain image in Docker repository [GET]
        image: image name
        returns: search results in JSON format
        '''
        if request.method == 'GET':
            cli = dcrops.docker_connect(config.DOCKER_SOCKET)
            image = request.args.get("image")
            if image is not None:
                response = cli.search(image)
                cli.close()
                return Response(json.dumps(response),  mimetype='application/json')
            else:
                cli.close()
                return "Error: Image not provided"

    def pull_image(self):
        '''Download a toolchain image from Docker repository [GET]
        image: repo/image:tag
        returns: result of docker pull operation
        '''
        if request.method == 'GET':
            temp = ""
            cli = dcrops.docker_connect(config.DOCKER_SOCKET)
            image = request.args.get("image")
            if image is not None:
                cli.pull(image, stream=False)
                cli.close()
                return Response(json.dumps("Success"),  mimetype='application/json')
            else:
                cli.close()
                return "Error: Image not provided"

    def remove_image(self):
        '''Remove toolchain image from local store [GET]
        image: repo/image:tag
        returns: result of docker remove image operation
        '''
        if request.method == 'GET':
            cli = dcrops.docker_connect(config.DOCKER_SOCKET)
            image = request.args.get("image")
            if image is not None:
                response = cli.remove_image(image)
                cli.close()
                return Response(json.dumps(response),  mimetype='application/json')
            else:
                cli.close()
                return "Error: Image not provided"

    def remove_toolchain(self):
        '''Remove toolchain from CODI database [GET]
        id: toolchain id
        returns: result of remove toolchain operation
        '''
        if request.method == 'GET':
            id = request.args.get("id")
            self.db.db_remove(config.TOOLCHAINS_TBL, id)
            return "Success"
        else:
            return "Error"

    def get_arg_parser(self):
        '''Create CODI command line argument parser
        returns: codi arguments
        '''
        parser = argparse.ArgumentParser(
            description='CODI command line arguments')
        parser.add_argument('--ip', default="0.0.0.0",
            help='codi ip address (default: 0.0.0.0)')
        parser.add_argument('--port', default=10000, type=int,
            help='codi port (default: 10000)')
        return parser.parse_args()
