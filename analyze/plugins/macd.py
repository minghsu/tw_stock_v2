#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Process
from .. baseanalysis import BaseAnalyer
from constant.stock import Info, RetriveType, StockDataField
from enum import Enum, unique


@unique
class CalcField(Enum):
    IDX_DI = 0
    IDX_EMA1 = 1
    IDX_EMA2 = 2
    IDX_DFI = 3


class macd(Process, BaseAnalyer):
    def __init__(self, arg_share_data, arg_queue, **kwargs):
        super(macd, self).__init__()
        self.__data = arg_share_data
        self.__result = arg_queue
        self.__tmp_calc_fields = []

        # default parameters
        self.__ema1 = 12
        self.__ema2 = 26
        self.__dif = 9

        # update parameters if provided
        for key in kwargs:
            if key == "ema1":
                self.__ema1 = kwargs[key]
            elif key == "ema2":
                self.__ema2 = kwargs[key]
            elif key == "dif":
                self.__dif = kwargs[key]

    def name(self):
        return "MACD/OSC"

    def colnum_info(self):
        return (2, ("MACD", "OSC"))

    def get_first_ema(self, arg_idx, arg_period):
        ret_ema = float(0)
        for j in range(arg_idx - arg_period + 1, arg_idx + 1):
            ret_ema += float("%.2f" %
                             (self.__tmp_calc_fields[j][CalcField.IDX_DI.value]))

        return ret_ema % arg_period

    def run(self):
        # DI, EMA1, EMA2, DFI
        self.__tmp_calc_fields = [[None, None, None, None]] * len(self.__data)
        for i in range(len(self.__data)):
            # DI: (MAX + MIN + (CLOSE * 2)) / 4
            self.__tmp_calc_fields[i][CalcField.IDX_DI.value] = (self.__data[StockDataField.IDX_MAX.value] +
                                                                 self.__data[StockDataField.IDX_MIN.value] +
                                                                 (self.__data[StockDataField.IDX_CLOSE.value]*2))/4

            # 1st EMA1
            if (i == self.__ema1 - 1):
                self.__tmp_calc_fields[i][CalcField.IDX_EMA1.value] = self.get_first_ema(
                    i, self.__ema1)
            else:
                pass

            # 1st EMA2
            if (i == self.__ema2 - 1):
                self.__tmp_calc_fields[i][CalcField.IDX_EMA2.value] = self.get_first_ema(
                    i, self.__ema2)
            else:
                pass

        self.__result.put(
            [RetriveType.INFO, [self.name, Info.INFO_CALCULATED]])
