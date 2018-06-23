#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from importlib import util


class DbFactory():
    def __init__(self):
        self.__dbList = []
        self.__dbClass = None
        tmpList = os.listdir("databases/engine/")
        for filename in tmpList:
            name, ext = os.path.splitext(filename)
            if (filename != "__init__.py" and ext == ".py"):
                dbClass = __import__("databases.engine.%s" %
                                     (name), fromlist=[name])
                instanceClass = getattr(dbClass, name)()

                lstDependency = instanceClass.dependency()
                for dependency in lstDependency:
                    if (util.find_spec(dependency) != None):
                        # Package Name, Database Name, dependency name
                        # Ex: MySQL, MariabDB/MySQL, MySQLdb
                        self.__dbList.append(
                            [name, instanceClass.name(), dependency])
                        break

    def is_db_module_exist(self, arg_module):
        bRet = True
        if (util.find_spec(arg_module) == None):
            bRet = False
        return bRet

    def get_db_module_list(self):
        return self.__dbList

    def connect(self, arg_db_class, arg_module, arg_host, arg_id, arg_pw):
        bRet = False
        if (util.find_spec(arg_module) != None):
            dbClassBase = __import__("databases.engine.%s" %
                                     (arg_db_class), fromlist=[arg_db_class])
            self.__dbClass = getattr(dbClassBase, arg_db_class)()
            self.__dbClass.initial(arg_module)
            bRet = self.__dbClass.connect(arg_host, arg_id, arg_pw)

        return bRet

    def close(self):
        if (self.__dbClass != None):
            self.__dbClass.close()

    def get_rmdb_name(self):
        if (self.__dbClass != None):
            return self.__dbClass.name()

    def open(self):
        if (self.__dbClass != None):
            return self.__dbClass.open()

    def execute(self, arg_sql_cmd):
        if (self.__dbClass != None):
            return self.__dbClass.execute(arg_sql_cmd)

    def query(self, arg_sql_cmd):
        if (self.__dbClass != None):
            return self.__dbClass.query(arg_sql_cmd)

    def commit(self):
        if (self.__dbClass != None):
            return self.__dbClass.commit()

    def create_symbol_data_table(self, arg_symbol):
        if (self.__dbClass != None):
            return self.__dbClass.create_symbol_data_table(arg_symbol)
