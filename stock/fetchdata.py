#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Process, Queue
from constant.stock import RetriveType, Info
from constant.useragent import USER_AGENT_LIST

DEF_CRAWL_CODE_URL = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s&stockNo=%s"


class FetchData(Process):
    def __init__(self, arg_queue, arg_symbol, arg_start_date, arg_stop_date):
        self.__queue = arg_queue
        self.__symbol = arg_symbol
        self.__start_date = arg_start_date
        self.__stop_date = arg_stop_date
