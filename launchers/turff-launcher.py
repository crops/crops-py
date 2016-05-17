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

    for jfile in os.listdir(config.JSON_ROOT):
        if jfile.endswith(".json"):
            jdata = turff.load_json(config.JSON_ROOT + jfile)
            if jdata is not None:
                response = turff.send_registration(config.REG_URL, jdata)
            else:
                response.status_code = 400

            if response.status_code == 200:
                print("Registration successful")
            else:
                print("Registration failed")
