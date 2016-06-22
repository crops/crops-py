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

from utils.globs import config
import rethinkdb as r
import signal
import json
import time
import sys
import os

class CodiDB() :
    '''CodiDB is used as a persistent storage for tracking
    the currently active toolchains
    '''

    def __init__(self, db_name):
        self.db_name = db_name
        create = self.db_create()
        if create is not None:
            if create is False:
                if self.db_table_create(config.TOOLCHAINS_TBL) is None:
                    print("Unable to initialize database table.Exiting")
                    if ("gunicorn" in os.environ.get("SERVER_SOFTWARE", "")):
                        os.kill(os.getppid(), signal.SIGTERM)
                    else:
                        sys.exit(0)
        else:
            print("Couldn't connect to the database")
            if ("gunicorn" in os.environ.get("SERVER_SOFTWARE", "")):
                os.kill(os.getppid(), signal.SIGTERM)
            else:
                sys.exit(0)

    def __db_connect_(self):
        try:
            conn = r.connect('localhost', 28015).repl()
        except r.ReqlDriverError:
            return False
        return conn

    def __db_connect_retry(self, retries):
        while(bool(retries)):
            conn =  self.__db_connect_();
            if (not conn):
                retries -= 1
                time.sleep(2)
            else:
                return conn

    def db_create(self):
        c = self.__db_connect_retry(config.DB_RETRIES)
        res = None
        if c :
            if self.db_name not in r.db_list().run(c):
                res = r.db_create(self.db_name).run(c)
            else:
                res = False
            c.close()
        return res

    def db_table_create(self, table_name):
        c = self.__db_connect_retry(config.DB_RETRIES)
        res = None
        if c:
            if table_name not in r.db(self.db_name).table_list().run(c):
                res =r.db(self.db_name).table_create(table_name).run(c)
            else:
                res = False
            c.close()
        return res

    def db_insert(self, table, entry):
        c = self.__db_connect_retry(config.DB_RETRIES)
        res = None
        if c:
            res = r.db(self.db_name).table(table).insert(entry).run(c)
            c.close()
        return res

    def db_select(self, table, db_filter):
        c = self.__db_connect_retry(config.DB_RETRIES)
        res = None
        if c:
            if db_filter is None:
                res = r.db(self.db_name).table(table).run(c)
            else:
                res = r.db(self.db_name).table(table).filter(json.loads(db_filter)).run(c)
            c.close()
        return res

    def db_remove(self, table, id):
        c = self.__db_connect_retry(config.DB_RETRIES)
        res = None
        if c:
            if id is not None:
                res = r.db(self.db_name).table(table).get(id).delete().run(c)
            c.close()
        return res
