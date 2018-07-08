#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Process
from .. baseanalysis import BaseAnalyer
from constant.stock import Info, RetriveType


class macd(Process, BaseAnalyer):
    def __init__(self, arg_share_data, arg_queue, **kwargs):
        super(macd, self).__init__()
        self.__data = arg_share_data
        self.__result = arg_queue

    def name(self):
        return "MACD"

    def colnum_info(self):
        return (1, ("MACD"))

    def run(self):
        self.__result.put(
            [RetriveType.INFO, [self.name, Info.INFO_CALCULATED]])
