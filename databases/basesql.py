#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import abc

from constant.stock import StockDB


class BaseSQL(abc.ABC):
    def __init__(self, arg_dict_sql_cmd):
        self.connection = None
        self.dbEngine = None
        self.dictSql = arg_dict_sql_cmd

    @abc.abstractmethod
    def name(self):
        # must provide which RMDB name
        return NotImplemented

    @abc.abstractmethod
    def dependency(self):
        # must provide the python package name to check was installed or not
        return NotImplemented

    @abc.abstractclassmethod
    def initial(self, arg_db_class):
        # Initial the instance
        return NotImplemented

    @abc.abstractclassmethod
    def connect(self, arg_host, arg_id, arg_pw):
        # connect to database
        return NotImplemented

    @abc.abstractclassmethod
    def close(self):
        # close the connection
        return NotImplemented

    @abc.abstractclassmethod
    def open(self):
        return NotImplemented

    @abc.abstractclassmethod
    def commit(self):
        # commit the change
        return NotImplemented

    @abc.abstractclassmethod
    def cursor(self):
        # return the cursor, subclass must implement
        raise NotImplementedError

    # without row data
    def execute(self, arg_sql_cmd):
        lCursor = self.cursor()
        if (lCursor != None):
            lCursor.execute(arg_sql_cmd)
            return True

        return False

    # with row data
    def query(self, arg_sql_cmd):
        lCursor = self.cursor()
        if (lCursor != None):
            lCursor.execute(arg_sql_cmd)
            if (lCursor.rowcount > 0):
                return (lCursor.rowcount, lCursor.fetchall())

        return (0, ())

    def is_database_exist(self):
        lCursor = self.cursor()
        if (lCursor != None):
            lCursor.execute(self.dictSql['CMD_CHECK_DATABASE'] % (
                StockDB.STR_DATABASE_NAME.value))
            if (lCursor.rowcount > 0):
                return True

        return False

    def is_table_exist(self, arg_table_name):
        lCursor = self.cursor()
        if (lCursor != None):
            lCursor.execute(self.dictSql['CMD_CHECK_TABLE'] % (arg_table_name))
            if (lCursor.rowcount > 0):
                return True

        return False

    def create_stock_data_table(self, arg_symbol):
        if (self.is_table_exist(StockDB.STR_STOCK_DATA_TABLE_PREFIX.value + arg_symbol)):
            return True

        if (self.execute(self.dictSql['CMD_CREATE_DATA_TABLE'] % (arg_symbol))):
            self.commit()
            return True

        return False

    def create_symbol_table(self):
        if (self.is_table_exist(StockDB.STR_STOCK_SYMBOL_TABLE_NAME.value)):
            return True

        if (self.execute(self.dictSql['CMD_CREATE_SYMBOL_TABLE'])):
            self.commit()
            return True

        return False

    def create_database(self):
        if (not self.is_database_exist()):
            if (self.execute(self.dictSql['CMD_CREATE_DATABASE'])):
                self.commit()
                return True
            else:
                return False

        return True
