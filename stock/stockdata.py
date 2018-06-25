#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Queue
from constant.stock import RetriveType, Info, FetchStockDataField
from . fetchdata import FetchData


class StockData:
    def __init__(self, arg_symbol_list):
        self.__mp = []
        self.__status = []
        self.__result = Queue()
        self.__queue = Queue()
        for symbol in arg_symbol_list:
            self.__mp.append(FetchData(self.__queue,
                                       symbol[FetchStockDataField.IDX_SYMBOL.value],
                                       symbol[FetchStockDataField.IDX_START_DATE.value],
                                       symbol[FetchStockDataField.IDX_STOP_DATE.value]))
            self.__status.append([symbol[FetchStockDataField.IDX_SYMBOL.value],
                                  symbol[FetchStockDataField.IDX_START_DATE.value],
                                  symbol[FetchStockDataField.IDX_STOP_DATE.value]])

    def get_fetch_count(self):
        return len(self.__mp)

    def run(self):
        for mp in self.__mp:
            mp.start()

    def retrive_data(self):
        while not self.__queue.empty():
            dataItem = self.__queue.get()
            if (dataItem[0] == RetriveType.DATA):
                self.__result.put(dataItem[1])
            elif (dataItem[0] == RetriveType.INFO):
                for i in range(len(self.__status)):
                    if (self.__status[i][0] == dataItem[1][0]):
                        self.__status[i][1] = dataItem[1][1]

    def is_queue_empty(self):
        return self.__queue.empty()

    def get_status(self):
        return self.__status

    def get_result(self):
        if (not self.__result.empty()):
            return self.__result.get()
        return None

    def is_alive(self):
        while any(i.is_alive() for i in self.__mp):
            return True

        return False
