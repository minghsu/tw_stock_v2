#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from .. basesql import BaseSQL
from constant.stock import StockDB

DICT_MYSQL_CMD = {
    "CMD_CHECK_DATABASE": ("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA"
                           " WHERE SCHEMA_NAME = '%s'"),
    "CMD_CREATE_DATABASE": ("CREATE DATABASE " + StockDB.STR_DATABASE_NAME.value
                            + " DEFAULT CHARSET utf8 COLLATE utf8_general_ci"),
    "CMD_CHECK_TABLE": ("SELECT * FROM INFORMATION_SCHEMA.TABLES"
                        " WHERE TABLE_SCHEMA = '" + StockDB.STR_DATABASE_NAME.value + "'"
                        " AND TABLE_NAME = '%s' LIMIT 1"),
    "CMD_CREATE_SYMBOL_TABLE": ("CREATE TABLE " + StockDB.STR_STOCK_SYMBOL_TABLE_NAME.value +
                                "(id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
                                "symbol VARCHAR(10) UNIQUE,"
                                "name VARCHAR(32),"
                                "create_date VARCHAR(10),"
                                "update_date VARCHAR(10)) DEFAULT CHARSET=utf8"),
}


class mysql(BaseSQL):
    def __init__(self):
        super().__init__(DICT_MYSQL_CMD)

    def name(self):
        return "MariaDB/MySQL"

    def dependency(self):
        return ['MySQLdb', 'pymysql']

    def initial(self, arg_db_class):
        self.dbEngine = __import__(arg_db_class)

    def connect(self, arg_host, arg_id, arg_pw):
        bRet = True
        try:
            self.connection = self.dbEngine.connect(
                host=arg_host, user=arg_id, passwd=arg_pw, charset='utf8')
            return super(mysql, self).create_database()
        except:
            bRet = False

        return bRet

    def close(self):
        if (self.connection != None):
            self.connection.close()
            self.connection = None

    def commit(self):
        if (self.connection != None):
            self.connection.commit()

    def open(self):
        bRet = True
        try:
            # select database
            self.connection.select_db(StockDB.STR_DATABASE_NAME.value)
            return super(mysql, self).create_symbol_table()
        except:
            bRet = False

        return bRet

    def cursor(self):
        if (self.connection != None):
            return self.connection.cursor()
        return None
