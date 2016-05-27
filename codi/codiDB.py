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

import rethinkdb as r
import json

class CodiDB() :
    '''CodiDB is used as a persistent storage for tracking
    the currently active toolchains
    '''

    def __init__(self, db_name):
        self.db_name = db_name

    def __db_connect_(self):
        return r.connect('localhost', 28015).repl()

    def db_create(self):
        c = self.__db_connect_()
        res = None
        if self.db_name not in r.db_list().run(c):
            res = r.db_create(self.db_name).run(c)
        c.close()
        return res

    def db_table_create(self, table_name):
        c = self.__db_connect_()
        res = None
        if table_name not in r.db(self.db_name).table_list().run(c):
            res =r.db(self.db_name).table_create(table_name).run(c)
        c.close()
        return res

    def db_insert(self, table, entry):
        c = self.__db_connect_()
        res = r.db(self.db_name).table(table).insert(entry).run(c)
        c.close()
        return res

    def db_select(self, table, db_filter):
        c = self.__db_connect_()
        if db_filter is None:
            res = r.db(self.db_name).table(table).run(c)
        else:
            res = r.db(self.db_name).table(table).filter(json.loads(db_filter)).run(c)
        c.close()
        return res

    def db_update(self):
        pass

    def db_remove(self):
        pass

