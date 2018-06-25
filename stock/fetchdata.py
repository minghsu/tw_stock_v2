#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Process, Queue
from constant.stock import RetriveType, Info, StockDataField
from constant.useragent import USER_AGENT_LIST
from utils.utility import util_convert_roc_to_ad_year

import time
import random
import urllib.request
import json


DEF_STOCK_DATA_FROM_199301 = "199301"
DEF_FETCH_DATA_TIMEOUT = 10
DEF_FETCH_DATA_SLEEP_TIME = 20
DEF_CRAWL_STOCK_DATA_URL = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s01&stockNo=%s"


class FetchData(Process):
    def __init__(self, arg_queue, arg_symbol, arg_start_date, arg_stop_date):
        super(FetchData, self).__init__()
        self.__queue = arg_queue
        self.__symbol = arg_symbol
        self.__start_date = arg_start_date
        self.__stop_date = arg_stop_date

    def __get_next_date(self, arg_date):
        n_year = int(arg_date[:4])
        n_month = int(arg_date[4:]) + 1

        if (n_month > 12):
            n_month = 1
            n_year += 1

        return "%04d%02d" % (n_year, n_month)

    def run(self):
        current_date = self.__start_date

        if (current_date < DEF_STOCK_DATA_FROM_199301):
            current_date = DEF_STOCK_DATA_FROM_199301

        while (self.__stop_date >= current_date):
            fetch_url = DEF_CRAWL_STOCK_DATA_URL % (
                current_date, self.__symbol)

            fetchReq = urllib.request.Request(
                fetch_url,
                data=None,
                headers={
                    'User-Agent': random.choice(USER_AGENT_LIST)
                }
            )

            try:
                json_response = urllib.request.urlopen(
                    fetchReq, timeout=DEF_FETCH_DATA_TIMEOUT).read()
            except:
                self.__queue.put(
                    [RetriveType.INFO, [self.__symbol, Info.INFO_TIMEOUT]])
            else:
                json_contents = json.loads(json_response)
                for trade_info in json_contents['data']:
                    self.__queue.put(
                        [RetriveType.DATA, [self.__symbol,
                                            [util_convert_roc_to_ad_year(trade_info[StockDataField.IDX_DATE.value]),
                                             trade_info[StockDataField.IDX_VOLUMN.value],
                                             trade_info[StockDataField.IDX_MONEY.value],
                                             trade_info[StockDataField.IDX_OPEN.value],
                                             trade_info[StockDataField.IDX_MAX.value],
                                             trade_info[StockDataField.IDX_MIN.value],
                                             trade_info[StockDataField.IDX_CLOSE.value],
                                             trade_info[StockDataField.IDX_SPREAD.value],
                                             trade_info[StockDataField.IDX_COUNT.value]]]])

                current_date = self.__get_next_date(current_date)
                self.__queue.put(
                    [RetriveType.INFO, [self.__symbol, current_date]])
            finally:
                time.sleep(DEF_FETCH_DATA_SLEEP_TIME)
