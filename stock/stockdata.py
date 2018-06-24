#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Queue
from constant.stock import RetriveType, Info, FetchStockDataField
from . fetchdata import FetchData


class StockData:
    def __init__(self, arg_symbol_list):
        self.__mp = []
        self.__status = []
        self.__result = []
        self.__queue = Queue()
        for symbol in arg_symbol_list:
            self.__mp.append(FetchData(self.__queue,
                                       symbol[FetchStockDataField.IDX_SYMBOL.value],
                                       symbol[FetchStockDataField.IDX_START_DATE.value],
                                       symbol[FetchStockDataField.IDX_STOP_DATE.value]))
            self.__status.append([symbol[FetchStockDataField.IDX_SYMBOL.value],
                                  symbol[FetchStockDataField.IDX_START_DATE.value],
                                  symbol[FetchStockDataField.IDX_STOP_DATE.value]])
