#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Process, Queue
from lxml import etree
from constant.stock import RetriveType, Info
from constant.useragent import USER_AGENT_LIST

import time
import random
import urllib.request

DEF_FETCH_SYMBOL_TIMEOUT = 10
DEF_FETCH_SYMBOL_SLEEP_TIME = 0.1


class FetchSymbol(Process):
    def __init__(self, arg_queue, arg_type, arg_url):
        super(FetchSymbol, self).__init__()
        self.__queue = arg_queue
        self.__type = arg_type
        self.__url = arg_url

    def run(self):
        fetchReq = urllib.request.Request(
            self.__url,
            data=None,
            headers={
                'User-Agent': random.choice(USER_AGENT_LIST)
            }
        )
        try:
            url_response = urllib.request.urlopen(
                fetchReq, timeout=DEF_FETCH_SYMBOL_TIMEOUT)
        except:
            self.__queue.put(
                [RetriveType.INFO, [self.__type, Info.INFO_SYMBOL_DOWNLOAD_TIMEOUT]])
        else:
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
                    time.sleep(DEF_FETCH_SYMBOL_SLEEP_TIME)

            self.__queue.put([RetriveType.INFO, [self.__type, 100]])
