#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Queue
from . fetchsymbol import FetchSymbol
from . basestock import BaseStock
from constant.stock import RetriveType, Info

# URL for List & OTC company
DICT_CRAWL_CODE_URL = {
    "STR_LISTED_COMPANY": "http://isin.twse.com.tw/isin/C_public.jsp?strMode=2",
    "STR_OTC_COMPANY": "http://isin.twse.com.tw/isin/C_public.jsp?strMode=4",
}


class StockSymbol(BaseStock):
    def __init__(self):
        super(StockSymbol, self).__init__()
        for key, value in DICT_CRAWL_CODE_URL.items():
            self.mp.append(
                FetchSymbol(self.queue, key, value))
            self.status.append(
                [key, Info.INFO_SYMBOL_DOWNLOADING])