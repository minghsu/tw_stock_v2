#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Queue
from constant.stock import RetriveType, Info, FetchStockDataField
from . fetchdata import FetchData
from . basestock import BaseStock

DEF_STOCK_DATA_FROM_199301 = "199301"

class StockData(BaseStock):
    def __init__(self, arg_symbol_list):
        super(StockData, self).__init__()
        for symbol in arg_symbol_list:

            real_start_date = symbol[FetchStockDataField.IDX_START_DATE.value]
            if (real_start_date < DEF_STOCK_DATA_FROM_199301):
                real_start_date = DEF_STOCK_DATA_FROM_199301

            self.mp.append(FetchData(self.queue,
                                       symbol[FetchStockDataField.IDX_SYMBOL.value],
                                       real_start_date,
                                       symbol[FetchStockDataField.IDX_STOP_DATE.value]))
            self.status.append([symbol[FetchStockDataField.IDX_SYMBOL.value],
                                  real_start_date,
                                  symbol[FetchStockDataField.IDX_STOP_DATE.value]])