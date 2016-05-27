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

class Codi() :
    '''Codi is used to track toolchains and manage Docker images

    Args: app (Flask): Instance of a Flask application
    '''

    def __init__(self, flask_app, codi_db):
        '''Initialize Codi with a flask app instance variable'''
        self.app = flask_app
        self.db = codi_db

    def list_api(self):
        '''Show CODI API
        args: None
        returns: List of all registered routes in JSON format
        '''
        return config.get_all_routes(self.app)

    def get_version(self):
        '''Show CODI version
        args: None
        returns: TURFF version in JSON format
        '''
        return jsonify(version=config.VERSION)

    def get_toolchains(self):
        '''List toolchains in CODI database
        filter: toolchain filter
        returns: List of all known toolchains in JSON format
        '''
        if request.method == 'GET':
            filter = request.args.get("filter")
            response = self.db.db_select(config.TOOLCHAINS_TBL, filter)
        return Response(json.dumps(list(response)),  mimetype='application/json')

    def add_toolchain(self):
        '''Add toolchain to the CODI database
        id: toolchain unique id
        name: toolchain name
        json: toolchain json descriptor
        returns: registration status
        '''
        if request.method == 'POST':
            json_data = request.get_json()
            self.db.db_create()
            self.db.db_table_create(config.TOOLCHAINS_TBL)
            self.db.db_insert(config.TOOLCHAINS_TBL, json_data)
        else:
            print("Unable to get JSON data")

    def find_image(self):
        '''Search for a toolchain image in Docker repository
        image: image name
        returns: search results in JSON format
        '''
        if request.method == 'GET':
            cli = config.docker_connect()
            response = cli.search(request.args.get("image"))
            return Response(json.dumps(response),  mimetype='application/json')

    def pull_image(self):
        '''Download a toolchain image from Docker repository
        image: repo/image:tag
        returns: result of docker pull operation
        '''
        if request.method == 'GET':
            cli = config.docker_connect()
            image = request.args.get("image")
            if image is not None:
                response = cli.pull(image)
                return Response(json.dumps(response),  mimetype='application/json')
            else:
                return "Error: Image not found"

    def remove_image(self):
        '''Remove toolchain image from local store
        image: repo/image:tag
        returns: result of docker remove image operation
        '''
        if request.method == 'GET':
            cli = config.docker_connect()
            image = request.args.get("image")
            if image is not None:
                response = cli.remove_image(image)
                return Response(json.dumps(response),  mimetype='application/json')
            else:
                return "Error: Image not found"

    def remove_toolchain(self):
        '''Remove toolchain from CODI database
        toolchain: toolchain id
        returns: result of docker remove image operation
        '''
        if request.method == 'GET':
            pass
        return 'TODO'
