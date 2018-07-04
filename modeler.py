#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from databases.dbfactory import DbFactory
from constant.stock import SymbolField, StockDB, StockDataField
from utils.utility import util_binary_search_idx, util_get_basename

import logging

DICT_SQL_CMD = {
    "SQL_CMD_FETCH_ALL_SYMBOL_INFO": ("SELECT symbol, name, create_date, update_date FROM "
                                      + StockDB.STR_STOCK_SYMBOL_TABLE_NAME.value + " ORDER BY symbol"),
    "SQL_CMD_INSERT_STOCK_SYMBOL": ("INSERT INTO " + StockDB.STR_STOCK_SYMBOL_TABLE_NAME.value +
                                    " (symbol, name, create_date, update_date)"
                                    " VALUES ('%s','%s','%s','%s')"),
    "SQL_CMD_UPDATE_STOCK_SYMBOL": ("UPDATE " + StockDB.STR_STOCK_SYMBOL_TABLE_NAME.value +
                                    " SET update_date = '%s' where symbol='%s'"),
    "SQL_CMD_FETCH_ALL_STOCK_DATA": ("SELECT trade_date, trade_volumn, trade_money, trade_open, trade_max, trade_min, trade_end, trade_spread, trade_count FROM "
                                     + StockDB.STR_STOCK_DATA_TABLE_PREFIX.value + "%s ORDER BY trade_date"),
    "SQL_CMD_INSERT_STOCK_DATA": ("INSERT INTO " + StockDB.STR_STOCK_DATA_TABLE_PREFIX.value + "%s"
                                  " (trade_date, trade_volumn, trade_money, trade_open, trade_max, trade_min, trade_end, trade_spread, trade_count)"
                                  " VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"),
    "SQL_CMD_UPDATE_STOCK_DATA": ("UPDATE " + StockDB.STR_STOCK_DATA_TABLE_PREFIX.value + "%s"
                                  " SET trade_volumn = '%s',  trade_money = '%s', trade_open = '%s',"
                                  " trade_max = '%s',  trade_min = '%s', trade_end = '%s',"
                                  " trade_spread = '%s',  trade_count = '%s' WHERE trade_date='%s'"),
}


class modeler:
    def __init__(self):
        self.__dbFactory = DbFactory()
        self.__SymbolInfoList = ()
        self.__logging = logging.getLogger(util_get_basename(__file__))

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

    def fetch_all_stock_data(self, arg_symbol):
        self.__SymbolDataCount, self.__SymbolDataList = self.__dbFactory.query(
            DICT_SQL_CMD['SQL_CMD_FETCH_ALL_STOCK_DATA'] % (arg_symbol))

    def get_symbol_trade_count(self):
        return self.__SymbolDataCount

    def get_stock_last_trade_date(self):
        if (self.__SymbolDataCount == 0):
            return None
        return self.__SymbolDataList[self.__SymbolDataCount-1][StockDataField.IDX_DATE.value]

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

        self.__logging.debug(str_sql_cmd)
        self.__dbFactory.execute(str_sql_cmd)
        self.__dbFactory.commit()

    def update_stock_data(self, arg_stock_data):
        str_sql_cmd = ""

        if (util_binary_search_idx(self.__SymbolDataList, 0, arg_stock_data[1][StockDataField.IDX_DATE.value]) == None):
            str_sql_cmd = DICT_SQL_CMD['SQL_CMD_INSERT_STOCK_DATA'] % (
                arg_stock_data[0],
                arg_stock_data[1][StockDataField.IDX_DATE.value],
                arg_stock_data[1][StockDataField.IDX_VOLUMN.value],
                arg_stock_data[1][StockDataField.IDX_MONEY.value],
                arg_stock_data[1][StockDataField.IDX_OPEN.value],
                arg_stock_data[1][StockDataField.IDX_MAX.value],
                arg_stock_data[1][StockDataField.IDX_MIN.value],
                arg_stock_data[1][StockDataField.IDX_CLOSE.value],
                arg_stock_data[1][StockDataField.IDX_SPREAD.value],
                arg_stock_data[1][StockDataField.IDX_COUNT.value])
        else:
            str_sql_cmd = DICT_SQL_CMD['SQL_CMD_UPDATE_STOCK_DATA'] % (
                arg_stock_data[0],
                arg_stock_data[1][StockDataField.IDX_VOLUMN.value],
                arg_stock_data[1][StockDataField.IDX_MONEY.value],
                arg_stock_data[1][StockDataField.IDX_OPEN.value],
                arg_stock_data[1][StockDataField.IDX_MAX.value],
                arg_stock_data[1][StockDataField.IDX_MIN.value],
                arg_stock_data[1][StockDataField.IDX_CLOSE.value],
                arg_stock_data[1][StockDataField.IDX_SPREAD.value],
                arg_stock_data[1][StockDataField.IDX_COUNT.value],
                arg_stock_data[1][StockDataField.IDX_DATE.value])

        self.__logging.debug(str_sql_cmd)
        self.__dbFactory.execute(str_sql_cmd)
        self.__dbFactory.commit()

    def is_symbol_exist(self, arg_symbol):
        return util_binary_search_idx(self.__SymbolInfoList, SymbolField.IDX_SYMBOL.value, arg_symbol)

    def get_symbol_info(self, arg_symbol):
        idx = self.is_symbol_exist(arg_symbol)
        if (idx != None):
            return self.__SymbolInfoList[idx]
        return None

    def create_stock_data_table(self, arg_symbol):
        return self.__dbFactory.create_stock_data_table(arg_symbol)
