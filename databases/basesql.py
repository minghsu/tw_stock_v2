#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import abc

from constant.stock import StockDB


class BaseSQL(abc.ABC):
    def __init__(self, argDictSqlCmd):
        self.connection = None
        self.dbEngine = None
        self.dictSql = argDictSqlCmd

    @abc.abstractmethod
    def name(self):
        # must provide which RMDB name
        return NotImplemented

    @abc.abstractmethod
    def dependency(self):
        # must provide the python package name to check was installed or not
        return NotImplemented

    @abc.abstractclassmethod
    def initial(self, argDbClass):
        # Initial the instance
        return NotImplemented

    @abc.abstractclassmethod
    def connect(self, argHost, argId, argPw):
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
    def execute(self, argSqlCmd):
        lCursor = self.cursor()
        if (lCursor != None):
            lCursor.execute(argSqlCmd)
            return True

        return False

    # with row data
    def query(self, argSqlCmd):
        lCursor = self.cursor()
        if (lCursor != None):
            lCursor.execute(argSqlCmd)
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

    def create_symbol_table(self):
        if (not self.is_table_exist(StockDB.STR_STOCK_SYMBOL_TABLE_NAME.value)):
            if (self.execute(self.dictSql['CMD_CREATE_SYMBOL_TABLE'])):
                self.commit()
                return True
            else:
                return False

        return True

    def create_database(self):
        if (not self.is_database_exist()):
            if (self.execute(self.dictSql['CMD_CREATE_DATABASE'])):
                self.commit()
                return True
            else:
                return False

        return True
