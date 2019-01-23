#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from enum import Enum, unique


@unique
class StockDB(Enum):
    STR_DATABASE_NAME = "tw_stock"
    STR_STOCK_SYMBOL_TABLE_NAME = "stock_symbol"
    STR_STOCK_DATA_TABLE_PREFIX = "symbol_"


@unique
class RetriveType(Enum):
    DATA = 0
    INFO = 1
    ERROR = 2


@unique
class SymbolField(Enum):
    IDX_SYMBOL = 0
    IDX_NAME = 1
    IDX_CREATE_DATE = 2
    IDX_UPDATED_DATE = 3


@unique
class ClassSupportField(Enum):
    IDX_CLASS_NAME = 0
    IDX_RMDB_NAME = 1
    IDX_MODULE_NAME = 2


@unique
class FetchStockDataField(Enum):
    IDX_SYMBOL = 0
    IDX_START_DATE = 1
    IDX_STOP_DATE = 2


@unique
class StockDataField(Enum):
    IDX_DATE = 0
    IDX_VOLUMN = 1
    IDX_MONEY = 2
    IDX_OPEN = 3
    IDX_MAX = 4
    IDX_MIN = 5
    IDX_CLOSE = 6
    IDX_SPREAD = 7
    IDX_COUNT = 8


@unique
class Info(Enum):
    INFO_SYMBOL_DOWNLOADING = "STR_SYMBOL_DOWNLOADING"
    INFO_SYMBOL_DOWNLOAD_TIMEOUT = "STR_SYMBOL_REQUEST_TIMEOUT"
    INFO_STOCK_DATA_DOWNLOAD_TIMEOUT = "STR_STOCK_DATA_REQUEST_TIMEOUT"
    INFO_CALCULATING = "STR_CALCULATING"
    INFO_CALCULATED = "STR_CALCULATED"
