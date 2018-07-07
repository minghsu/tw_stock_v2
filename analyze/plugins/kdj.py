#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Process
from .. baseanalysis import BaseAnalyer


class kdj(Process, BaseAnalyer):
    def __init__(self, arg_share_data, arg_share_result):
        super(kdj, self).__init__()
        self.__data = arg_share_data
        self.__result = arg_share_result

    def name(self):
        return "KDJ"

    def colnum_info(self):
        return (3, ("K", "D", "J"))

    def run(self):
        print("KDJ")
        print(self.__data[0])
