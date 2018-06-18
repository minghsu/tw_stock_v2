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

    def is_db_module_exist(self, argModule):
        bRet = True
        if (util.find_spec(argModule) == None):
            bRet = False
        return bRet

    def get_db_module_list(self):
        return self.__dbList

    def connect(self, argDbClass, argModule, argHost, argId, argPw):
        bRet = False
        if (util.find_spec(argModule) != None):
            dbClassBase = __import__("databases.engine.%s" %
                                     (argDbClass), fromlist=[argDbClass])
            self.__dbClass = getattr(dbClassBase, argDbClass)()
            self.__dbClass.initial(argModule)
            bRet = self.__dbClass.connect(argHost, argId, argPw)

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

    def execute(self, argSqlCmd):
        if (self.__dbClass != None):
            return self.__dbClass.execute(argSqlCmd)

    def query(self, argSqlCmd):
        if (self.__dbClass != None):
            return self.__dbClass.query(argSqlCmd)

    def commit(self):
        if (self.__dbClass != None):
            return self.__dbClass.commit()
