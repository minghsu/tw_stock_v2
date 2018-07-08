#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Process
from .. baseanalysis import BaseAnalyer
from constant.stock import Info, RetriveType, StockDataField


class kdj(Process, BaseAnalyer):
    def __init__(self, arg_share_data, arg_queue, **kwargs):
        super(kdj, self).__init__()
        self.__data = arg_share_data
        self.__result = arg_queue

        # default parameters
        self.__fast_k_period = 9
        self.__slow_k_period = 3
        self.__slow_d_period = 3

        # update parameters if provided
        for key in kwargs:
            if key == "fast_k_period":
                self.__fast_k_period = kwargs[key]
            elif key == "slow_k_period":
                self.__slow_k_period = kwargs[key]
            elif key == "slow_d_period":
                self.__slow_d_period = kwargs[key]

    def name(self):
        return "KDJ"

    def colnum_info(self):
        return (3, ("K", "D", "J"))

    def get_max_min_value(self, arg_current_idx):
        ret_max = float(self.__data[arg_current_idx]
                        [StockDataField.IDX_MAX.value])
        ret_min = float(self.__data[arg_current_idx]
                        [StockDataField.IDX_MIN.value])

        for j in range(arg_current_idx - self.__fast_k_period, arg_current_idx):
            if ret_max < float(self.__data[j][StockDataField.IDX_MAX.value]):
                ret_max = float(self.__data[j][StockDataField.IDX_MAX.value])
            if ret_min > float(self.__data[j][StockDataField.IDX_MIN.value]):
                ret_min = float(self.__data[j][StockDataField.IDX_MIN.value])

        return (ret_max, ret_min)

    def run(self):
        k_val = 0
        d_val = 0
        for i in range(len(self.__data)):
            last_k_val = k_val
            last_d_val = d_val
            if (i < self.__fast_k_period - 1):
                self.__result.put([RetriveType.DATA, ["N/A", "N/A", "N/A"]])
            elif (i == self.__fast_k_period - 1):
                self.__result.put([RetriveType.DATA, [50, 50, 50]])
                k_val = 50
                d_val = 50
            else:
                max, min = self.get_max_min_value(i)
                rsv = float(
                    100*(float(self.__data[i][StockDataField.IDX_CLOSE.value])-min)/(max-min))

                k_val = float('%.2f' % ((1/self.__slow_k_period) *
                                        rsv + (2/self.__slow_d_period) * last_k_val))
                d_val = float('%.2f' % ((1/self.__slow_d_period) *
                                        k_val + (2/self.__slow_d_period) * last_d_val))
                j_val = float('%.2f' % ((d_val*3) - (k_val*2)))

                print("[DEBUG] %s, last k %.2f, last d %.2f, max %.2f, min %.2f, k %.2f, d %.2f, j %.2f, rsv %.2f" %
                      (self.__data[i][StockDataField.IDX_DATE.value], last_k_val, last_d_val, max, min, k_val, d_val, j_val, rsv))
                self.__result.put([RetriveType.DATA, [k_val, d_val, j_val]])

        self.__result.put(
            [RetriveType.INFO, [self.name, Info.INFO_CALCULATED]])
