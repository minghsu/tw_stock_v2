#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Queue
from . fetchsymbol import FetchSymbol
from constant.stock import RetriveType, Info

# URL for List & OTC company
DICT_CRAWL_CODE_URL = {
    "STR_LISTED_COMPANY": "http://isin.twse.com.tw/isin/C_public.jsp?strMode=2",
    "STR_OTC_COMPANY": "http://isin.twse.com.tw/isin/C_public.jsp?strMode=4",
}


class StockSymbol:
    def __init__(self):
        self.__mp = []
        self.__status = []
        self.__result = Queue()
        self.__queue = Queue()
        for key, value in DICT_CRAWL_CODE_URL.items():
            self.__mp.append(
                FetchSymbol(self.__queue, key, value))
            self.__status.append(
                [key, Info.INFO_SYMBOL_DOWNLOADING])

    def get_fetch_count(self):
        return len(DICT_CRAWL_CODE_URL)

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
