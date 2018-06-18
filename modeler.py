#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from databases.dbfactory import DbFactory
from constant.stock import SymbolField, StockDB
from utils.utility import IsSymbolExist

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

    def connect(self, argDbClass, argModule, argHost, argId, argPw):
        return self.__dbFactory.connect(argDbClass, argModule, argHost, argId, argPw)

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

    def update_stock_symbol(self, argSymbolItem, argUpdateDate):
        strSqlCmd = ""
        if (IsSymbolExist(self.__SymbolInfoList, argSymbolItem[SymbolField.IDX_SYMBOL.value]) == None):
            strSqlCmd = DICT_SQL_CMD['SQL_CMD_INSERT_STOCK_SYMBOL'] % (
                argSymbolItem[SymbolField.IDX_SYMBOL.value],
                argSymbolItem[SymbolField.IDX_NAME.value],
                argSymbolItem[SymbolField.IDX_CREATE_DATE.value],
                argUpdateDate)
        else:
            strSqlCmd = DICT_SQL_CMD['SQL_CMD_UPDATE_STOCK_SYMBOL'] % (
                argUpdateDate,
                argSymbolItem[SymbolField.IDX_SYMBOL.value])

        self.__dbFactory.execute(strSqlCmd)
        self.__dbFactory.commit()
