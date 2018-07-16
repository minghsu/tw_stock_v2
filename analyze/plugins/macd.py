#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Process
from .. baseanalysis import BaseAnalyer
from constant.stock import Info, RetriveType, StockDataField
from enum import Enum, unique
from pandas.core.frame import DataFrame
import pandas as pd


@unique
class CalcField(Enum):
    IDX_DI = 0
    IDX_EMA1 = 1
    IDX_EMA2 = 2
    IDX_DIF = 3


@unique
class ResultField(Enum):
    IDX_MACD = 0
    IDX_OSC = 1


class macd(Process, BaseAnalyer):
    def __init__(self, arg_share_data, arg_queue, **kwargs):
        super(macd, self).__init__()
        self.__data = arg_share_data
        self.queue = arg_queue
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

    def analysis_name(self):
        return "MACD/OSC"

    def colnum_info(self):
        return ("MACD", "OSC")

    def get_first_ema(self, arg_idx, arg_period):
        ret_ema = float(0)
        for j in range(arg_idx - arg_period + 1, arg_idx + 1):
            ret_ema += float("%.2f" %
                             (self.__df_calculate[CalcField.IDX_DI.value].values[j]))
        return float("%.2f" % (ret_ema / arg_period))

    def get_ema(self, arg_idx, arg_previous_ema, arg_period):
        ret_ema = float("%.2f" % (((arg_previous_ema * (arg_period-1)) +
                                   (self.__df_calculate[CalcField.IDX_DI.value].values[arg_idx]*2)) / (arg_period+1)))
        return ret_ema

    def get_first_macd(self, arg_idx):
        ret_macd = float(0)
        for j in range(arg_idx - self.__dif + 1, arg_idx + 1):
            ret_macd += float("%.2f" %
                              (self.__df_calculate[CalcField.IDX_DIF.value].values[j]))

        return float("%.2f" % (ret_macd / self.__dif))

    def get_macd(self, arg_idx):
        ret_macd = float("%.2f" % (((self.__df_result[ResultField.IDX_MACD.value].values[arg_idx - 1] * (self.__dif - 1)) +
                                    (self.__df_calculate[CalcField.IDX_DIF.value].values[arg_idx]*2)) / (self.__dif + 1)))

        return ret_macd

    def run(self):
        super(macd, self).delay()

        # MACD, OSC
        self.__df_result = DataFrame([[0, 0]] * len(self.__data))

        # DI, EMA1, EMA2, DIF
        self.__df_calculate = DataFrame([[0, 0, 0, 0]] * len(self.__data))

        for i, stock_data in enumerate(self.__data):

            # DI: (MAX + MIN + (CLOSE * 2)) / 4
            self.__df_calculate.iloc[[i], [CalcField.IDX_DI.value]] = float("%.2f" % ((float(stock_data[StockDataField.IDX_MAX.value]) +
                                                                                       float(stock_data[StockDataField.IDX_MIN.value]) +
                                                                                       (float(stock_data[StockDataField.IDX_CLOSE.value])*2))/4))
            # EMA1
            if (i == self.__ema1 - 1):
                self.__df_calculate.iloc[[i], [CalcField.IDX_EMA1.value]] = self.get_first_ema(
                    i, self.__ema1)

            elif (i >= self.__ema1):
                # EMA12 = [EMA12(t-1) × (12 - 1) + DI(t) × 2] ÷ (12+1)
                self.__df_calculate.iloc[[i], [CalcField.IDX_EMA1.value]] = self.get_ema(
                    i, self.__df_calculate[CalcField.IDX_EMA1.value].values[i-1], self.__ema1)

            # EMA2
            if (i == self.__ema2 - 1):
                self.__df_calculate.iloc[[i], [CalcField.IDX_EMA2.value]] = self.get_first_ema(
                    i, self.__ema2)
            elif (i >= self.__ema2):
                    # EMA26 = [EMA26(t-1) × (26 - 1) + DI(t) × 2] ÷ (26+1)
                self.__df_calculate.iloc[[i], [CalcField.IDX_EMA2.value]] = self.get_ema(
                    i, self.__df_calculate[CalcField.IDX_EMA2.value].values[i-1], self.__ema2)

            # DIF
            if (i >= self.__ema2-1):
                self.__df_calculate.iloc[[i], [CalcField.IDX_DIF.value]] = self.__df_calculate[
                    CalcField.IDX_EMA1.value].values[i] - self.__df_calculate[CalcField.IDX_EMA2.value][i]

            if (i == (self.__ema2 + self.__dif - 1)):
                # 1st MACD
                self.__df_result.iloc[[i], [
                    ResultField.IDX_MACD.value]] = self.get_first_macd(i)
            elif (i >= self.__ema2 + self.__dif):
                # Other MACD
                self.__df_result.iloc[[i], [
                    ResultField.IDX_MACD.value]] = self.get_macd(i)

            # OSC
            if (i >= (self.__ema2 + self.__dif - 1)):
                self.__df_result.iloc[[i], [ResultField.IDX_OSC.value]] = float("%.2f" % (self.__df_calculate[CalcField.IDX_DIF.value].values[i] -
                                                                                          self.__df_result[ResultField.IDX_MACD.value].values[i]))
        self.__df_result.columns = self.colnum_info()

        self.queue.put(
            [RetriveType.DATA, self.__df_result])
        self.queue.put(
            [RetriveType.INFO, [self.analysis_name(), Info.INFO_CALCULATED]])
