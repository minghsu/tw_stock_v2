#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from enum import Enum, unique


@unique
class StockDB(Enum):
    STR_DATABASE_NAME = "tw_stock"
    STR_STOCK_SYMBOL_TABLE_NAME = "stock_symbol"
    STR_STOCK_SYMBOL_DATA_TABLE_PREFIX = "symbol_"


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
