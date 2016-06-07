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

from turff import turff
from flask import Response
from utils.globs import config
import os

if __name__ == '__main__':
    response = Response()
    turff = turff.Turff()
    turff_args = turff.get_arg_parser()

    for jfile in os.listdir(turff_args.jsonRoot + "/"):
        if jfile.endswith(".json"):
            jdata = turff.load_json(turff_args.jsonRoot + "/" + jfile)
            if jdata is not None:
                url = "http://" + turff_args.ip + ":" + \
                str(turff_args.port) + "/codi/register-toolchain"
                response = turff.send_registration(url, jdata)
            else:
                response.status_code = 400

            if response.status_code == 200:
                print("Registration successful : " + jfile)
            else:
                print("Registration failed : " + jfile)
