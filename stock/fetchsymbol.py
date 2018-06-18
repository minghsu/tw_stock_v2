#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Process, Queue
from lxml import etree
from constant.stock import RetriveType

import time
import random
import urllib.request

DEF_FETCH_TIMEOUT = 10
DEF_SLEEP_TIME = 0.1


# User Agent
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"
]


class FetchSymbol(Process):
    def __init__(self, argQueue, argType, argUrl):
        super(FetchSymbol, self).__init__()
        self.__queue = argQueue
        self.__type = argType
        self.__url = argUrl
        self.__queue.put([RetriveType.INFO, [self.__type, 0]])

    def run(self):
        time.sleep(DEF_SLEEP_TIME)

        fetchReq = urllib.request.Request(
            self.__url,
            data=None,
            headers={
                'User-Agent': random.choice(USER_AGENT_LIST)
            }
        )
        url_response = urllib.request.urlopen(
            fetchReq, timeout=DEF_FETCH_TIMEOUT)
        url_content = url_response.read()
        url_content = url_content.decode('big5-hkscs').encode('utf-8')

        html_content = etree.HTML(
            url_content, parser=etree.HTMLParser(encoding='utf-8'))
        tr_contents = html_content.xpath("//table[2]/tr")

        total_tr_count = len(tr_contents)
        for idx, tr in enumerate(tr_contents, start=1):
            td_contents = tr.xpath(".//td")
            if len(td_contents) == 7:
                td_name = td_contents[0].text
                td_date = td_contents[2].text

                splitIdx = td_name.find(u'　')
                if (splitIdx >= 0):
                    stock_code = td_name[:splitIdx]
                    stock_code = stock_code.replace(" ", "")
                    stock_name = td_name[splitIdx+1:]

                    self.__queue.put(
                        [RetriveType.DATA, [self.__type, [stock_code, stock_name, td_date]]])

                self.__queue.put(
                    [RetriveType.INFO, [self.__type, (idx/total_tr_count)*100]])

            if (idx % 100 == 0):
                time.sleep(DEF_SLEEP_TIME)

        self.__queue.put([RetriveType.INFO, [self.__type, 100]])
