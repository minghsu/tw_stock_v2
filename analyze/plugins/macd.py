#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Process
from .. baseanalysis import BaseAnalyer


class macd(Process, BaseAnalyer):
    def __init__(self, arg_share_data, arg_share_result):
        super(macd, self).__init__()
        self.__data = arg_share_data
        self.__result = arg_share_result

    def name(self):
        return "MACD"

    def colnum_info(self):
        return (1, ("MACD"))

    def run(self):
        print("MACD")
        print(self.__data[0])
