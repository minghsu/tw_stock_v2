#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Process
from .. baseanalysis import BaseAnalyer
from constant.stock import Info, RetriveType, StockDataField
from pandas.core.frame import DataFrame

import pandas as pd


class rsi(Process, BaseAnalyer):
    def __init__(self, arg_share_data, arg_queue, **kwargs):
        super(rsi, self).__init__()
        self.__data = arg_share_data
        self.queue = arg_queue

        # default parameters
        self.__rsi_period = 6

        # update parameters if provided
        for key in kwargs:
            if key == "rsi_period":
                self.__rsi_period = kwargs[key]

    def analysis_name(self):
        return "RSI"

    def colnum_info(self):
        return ("RSI",)

    def get_rsi(self, arg_idx):
        up_val = 0
        down_val = 0

        for j in range(arg_idx - self.__rsi_period + 1, arg_idx + 1):
            if self.__data[j][StockDataField.IDX_SPREAD.value] == "X0.00":
                pass
            else:
                spread_val = float(
                    self.__data[j][StockDataField.IDX_SPREAD.value])

                if spread_val > 0:
                    up_val += spread_val
                else:
                    down_val -= spread_val

        up_val = float("%.2f" % (up_val/self.__rsi_period))
        down_val = float("%.2f" % (down_val/self.__rsi_period))

        if up_val == 0 or down_val == 0:
            return 0

        return float("%.2f" % (100 * up_val/(up_val+down_val)))

    def run(self):
        super(rsi, self).delay()

        self.__df_result = DataFrame([0] * len(self.__data))

        for i in range(len(self.__data)):
            if (i < self.__rsi_period):
                pass
            else:
                self.__df_result.iloc[[i], [0]] = self.get_rsi(i)

        self.__df_result.columns = self.colnum_info()

        self.queue.put(
            [RetriveType.DATA, self.__df_result])
        self.queue.put(
            [RetriveType.INFO, [self.analysis_name(), Info.INFO_CALCULATED]])
