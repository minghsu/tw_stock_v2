#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from importlib import util
from multiprocessing import Manager, Queue
from constant.analysis import AnalyzeFieldIdx
from constant.stock import RetriveType, Info

import os


class Analyer:
    def __init__(self):
        self.__plugins = []
        self.__mp = []
        self.__manager = Manager()
        self.__share_data = self.__manager.list()
        self.__queue_result = Queue()
        self.__status = []

        tmpList = os.listdir("analyze/plugins/")
        for filename in tmpList:
            name, ext = os.path.splitext(filename)
            if (filename != "__init__.py" and ext == ".py"):
                plugins_class = __import__("analyze.plugins.%s" %
                                           (name), fromlist=[name])
                instanceClass = getattr(plugins_class, name)(
                    self.__manager.list(), None)
                self.__plugins.append(
                    [name, instanceClass.analysis_name(), instanceClass.colnum_info(), True])

    def get_plugins(self):
        retPlugins = ""
        for plugins in self.__plugins:
            if retPlugins != "":
                retPlugins = retPlugins + ", "

            retPlugins = retPlugins + \
                plugins[AnalyzeFieldIdx.IDX_ANALYE_NAME.value]

        return retPlugins

    def set_data(self, arg_data):
        self.__data = arg_data
        self.__share_data = self.__manager.list(arg_data)

    def run(self):
        self.__mp.clear()
        self.__status.clear()
        i = 0
        for plugins in self.__plugins:
            if plugins[AnalyzeFieldIdx.IDX_IS_EXECUTE.value]:
                name = plugins[AnalyzeFieldIdx.IDX_MODULE_NAME.value]
                plugins_class = __import__(
                    "analyze.plugins.%s" % (name), fromlist=[name])
                self.__mp.append(getattr(plugins_class, name)(
                    self.__data, self.__queue_result))
                self.__status.append(
                    [plugins[AnalyzeFieldIdx.IDX_ANALYE_NAME.value], Info.INFO_CALCULATING])
                i += 1

        for mp in self.__mp:
            mp.start()

    def is_alive(self):
        while any(i.is_alive() for i in self.__mp):
            return True

        return False

    def is_queue_empty(self):
        return self.__queue_result.empty()

    def retrive_data(self):
        while not self.__queue_result.empty():
            dataItem = self.__queue_result.get()
            if (dataItem[0] == RetriveType.DATA):
                self.__queue_result.put(dataItem[1])
            elif (dataItem[0] == RetriveType.INFO):
                for i in range(len(self.__status)):
                    if (self.__status[i][0] == dataItem[1][0]):
                        self.__status[i][1] = dataItem[1][1]

    def get_plugins_count(self):
        return len(self.__mp)

    def get_status(self):
        return self.__status
