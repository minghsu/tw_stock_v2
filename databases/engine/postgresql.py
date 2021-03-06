#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from .. basesql import BaseSQL

from constant.stock import StockDB

DEF_PSQL_SYS_DB_NAME = "postgres"

DICT_POSTGRESQL_CMD = {
    "CMD_CHECK_DATABASE": ("SELECT 1 FROM pg_database WHERE datname = '%s'"),
    "CMD_CREATE_DATABASE": ("CREATE DATABASE " + StockDB.STR_DATABASE_NAME.value),
    "CMD_CHECK_TABLE": ("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='%s'"),
    "CMD_CREATE_SYMBOL_TABLE": ("CREATE TABLE " + StockDB.STR_STOCK_SYMBOL_TABLE_NAME.value +
                                "(id SERIAL  PRIMARY KEY,"
                                "symbol      VARCHAR(10) UNIQUE,"
                                "name        VARCHAR(32),"
                                "create_date VARCHAR(10),"
                                "update_date VARCHAR(10))"),
    "CMD_CREATE_DATA_TABLE": ("CREATE TABLE " + StockDB.STR_STOCK_DATA_TABLE_PREFIX.value + "%s"
                              "(id SERIAL   PRIMARY KEY,"
                              "trade_date   VARCHAR(10) UNIQUE,"
                              "trade_volumn VARCHAR(16),"
                              "trade_money  VARCHAR(16),"
                              "trade_open   VARCHAR(8),"
                              "trade_max    VARCHAR(8),"
                              "trade_min    VARCHAR(8),"
                              "trade_end    VARCHAR(8),"
                              "trade_spread VARCHAR(8),"
                              "trade_count  VARCHAR(10))"),
}


class postgresql(BaseSQL):
    def __init__(self):
        super().__init__(DICT_POSTGRESQL_CMD)

    def __connect(self, arg_db, arg_host, arg_id, arg_pw):
        bRet = True
        try:
            self.connection = self.dbEngine.connect(
                dbname=arg_db, user=arg_id, password=arg_pw, host=arg_host)
        except:
            bRet = False

        return bRet

    def name(self):
        return "PostgreSQL"

    def dependency(self):
        return ['psycopg2']

    def initial(self, arg_db_class):
        self.dbEngine = __import__(arg_db_class)

    def connect(self, arg_host, arg_id, arg_pw):
        self.__Host = arg_host
        self.__Id = arg_id
        self.__Pw = arg_pw

        if (self.__connect(DEF_PSQL_SYS_DB_NAME, self.__Host, self.__Id, self.__Pw)):
            # enable the isolation_level auto commit
            self.connection.set_isolation_level(
                self.dbEngine.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            return super(postgresql, self).create_database()

        return False

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
            if (self.__connect(StockDB.STR_DATABASE_NAME.value,
                               self.__Host, self.__Id, self.__Pw)):
                return super(postgresql, self).create_symbol_table()
        except:
            bRet = False

        return bRet

    def cursor(self):
        if (self.connection != None):
            return self.connection.cursor()
        return None
