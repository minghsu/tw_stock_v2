#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from databases.dbfactory import DbFactory
from constant.stock import SymbolField, StockDB
from utils.utility import util_is_symbol_exist

DICT_SQL_CMD = {
    "SQL_CMD_FETCH_ALL_SYMBOL_INFO": ("SELECT symbol, name, create_date, update_date FROM "
                                      + StockDB.STR_STOCK_SYMBOL_TABLE_NAME.value + " ORDER BY symbol"),
    "SQL_CMD_INSERT_STOCK_SYMBOL": ("INSERT INTO " + StockDB.STR_STOCK_SYMBOL_TABLE_NAME.value +
                                    " (symbol, name, create_date, update_date)"
                                    " VALUES ('%s','%s','%s','%s')"),
    "SQL_CMD_UPDATE_STOCK_SYMBOL": ("UPDATE " + StockDB.STR_STOCK_SYMBOL_TABLE_NAME.value +
                                    " SET update_date = '%s' where symbol='%s'")
}


class modeler:
    def __init__(self):
        self.__dbFactory = DbFactory()
        self.__SymbolInfoList = ()

    def get_db_module_list(self):
        return self.__dbFactory.get_db_module_list()

    def connect(self, arg_db_class, arg_module, arg_host, arg_id, arg_pw):
        return self.__dbFactory.connect(arg_db_class, arg_module, arg_host, arg_id, arg_pw)

    def close(self):
        self.__dbFactory.close()

    def get_rmdb_name(self):
        return self.__dbFactory.get_rmdb_name()

    def open(self):
        return self.__dbFactory.open()

    def is_db_module_exist(self, argModule):
        return self.__dbFactory.is_db_module_exist(argModule)

    def fetch_symbol_list(self):
        self.__SymbolCount, self.__SymbolInfoList = self.__dbFactory.query(
            DICT_SQL_CMD['SQL_CMD_FETCH_ALL_SYMBOL_INFO'])

    def get_symbol_count(self):
        return self.__SymbolCount

    def update_stock_symbol(self, arg_symbol_item, arg_update_date):
        strSqlCmd = ""
        if (util_is_symbol_exist(self.__SymbolInfoList, arg_symbol_item[SymbolField.IDX_SYMBOL.value]) == None):
            strSqlCmd = DICT_SQL_CMD['SQL_CMD_INSERT_STOCK_SYMBOL'] % (
                arg_symbol_item[SymbolField.IDX_SYMBOL.value],
                arg_symbol_item[SymbolField.IDX_NAME.value],
                arg_symbol_item[SymbolField.IDX_CREATE_DATE.value],
                arg_update_date)
        else:
            strSqlCmd = DICT_SQL_CMD['SQL_CMD_UPDATE_STOCK_SYMBOL'] % (
                arg_update_date,
                arg_symbol_item[SymbolField.IDX_SYMBOL.value])

        self.__dbFactory.execute(strSqlCmd)
        self.__dbFactory.commit()

    def is_symbol_exist(self, arg_symbol):
        return util_is_symbol_exist(self.__SymbolInfoList, arg_symbol)

    def get_symbol_info(self, arg_symbol):
        idx = self.is_symbol_exist(arg_symbol)
        if (idx != None):
            return self.__SymbolInfoList[idx]

        return None
