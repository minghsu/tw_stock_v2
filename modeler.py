#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from databases.dbfactory import DbFactory
from constant.stock import SymbolField, StockDB
from utils.utility import util_binary_search_idx

DICT_SQL_CMD = {
    "SQL_CMD_FETCH_ALL_SYMBOL_INFO": ("SELECT symbol, name, create_date, update_date FROM "
                                      + StockDB.STR_STOCK_SYMBOL_TABLE_NAME.value + " ORDER BY symbol"),
    "SQL_CMD_INSERT_STOCK_SYMBOL": ("INSERT INTO " + StockDB.STR_STOCK_SYMBOL_TABLE_NAME.value +
                                    " (symbol, name, create_date, update_date)"
                                    " VALUES ('%s','%s','%s','%s')"),
    "SQL_CMD_UPDATE_STOCK_SYMBOL": ("UPDATE " + StockDB.STR_STOCK_SYMBOL_TABLE_NAME.value +
                                    " SET update_date = '%s' where symbol='%s'"),
    "SQL_CMD_FETCH_SYMBOL_TRADE_DATE_LIST": ("SELECT trade_date FROM "
                                             + StockDB.STR_STOCK_SYMBOL_DATA_TABLE_PREFIX.value + "%s ORDER BY trade_date"),
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

    def fetch_symbol_trade_date_list(self, arg_symbol):
        self.__SymbolTradeCount, self.__SymbolTradeDateList = self.__dbFactory.query(
            DICT_SQL_CMD['SQL_CMD_FETCH_SYMBOL_TRADE_DATE_LIST'] % (arg_symbol))

    def get_symbol_trade_count(self):
        return self.__SymbolTradeCount

    def get_symbol_last_trade_date(self):
        if (self.__SymbolTradeCount == 0):
            return None
        return self.__SymbolTradeDateList[self.__SymbolTradeCount-1]

    def update_stock_symbol(self, arg_symbol_item, arg_update_date):
        str_sql_cmd = ""
        if (self.is_symbol_exist(arg_symbol_item[SymbolField.IDX_SYMBOL.value]) == None):
            str_sql_cmd = DICT_SQL_CMD['SQL_CMD_INSERT_STOCK_SYMBOL'] % (
                arg_symbol_item[SymbolField.IDX_SYMBOL.value],
                arg_symbol_item[SymbolField.IDX_NAME.value],
                arg_symbol_item[SymbolField.IDX_CREATE_DATE.value],
                arg_update_date)
        else:
            str_sql_cmd = DICT_SQL_CMD['SQL_CMD_UPDATE_STOCK_SYMBOL'] % (
                arg_update_date,
                arg_symbol_item[SymbolField.IDX_SYMBOL.value])

        self.__dbFactory.execute(str_sql_cmd)
        self.__dbFactory.commit()

    def is_symbol_exist(self, arg_symbol):
        return util_binary_search_idx(self.__SymbolInfoList, SymbolField.IDX_SYMBOL.value, arg_symbol)

    def get_symbol_info(self, arg_symbol):
        idx = self.is_symbol_exist(arg_symbol)
        if (idx != None):
            return self.__SymbolInfoList[idx]

        return None

    def create_symbol_data_table(self, arg_symbol):
        return self.__dbFactory.create_symbol_data_table(arg_symbol)
