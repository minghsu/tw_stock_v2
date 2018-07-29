#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from importlib import util
from multiprocessing import Manager, Queue
from constant.analysis import AnalyzeFieldIdx
from constant.stock import RetriveType, Info
from pandas.core.frame import DataFrame
from datetime import datetime

import pandas as pd
import os

DEF_STOCK_COULMN_NAME = ["Date", "Volumn", "Money", "Open",
                         "Max", "Min", "Close", "Spread", "Count"]

DEF_EXPORT_FOLDER_NAME = "exportfile"


class Analyer:
    def __init__(self):
        self.__plugins = []
        self.__mp = []
        self.__manager = Manager()
        self.__share_data = self.__manager.list()
        self.__queue = Queue()
        self.__status = []
        self.__result = []

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

    def get_supported_plugins(self):
        retSupported = ""
        for plugins in self.__plugins:
            if retSupported != "":
                retSupported = retSupported + ", "

            retSupported = retSupported + \
                plugins[AnalyzeFieldIdx.IDX_ANALYE_NAME.value]

        return retSupported

    def get_plugins(self):
        return self.__plugins

    def set_data(self, arg_data):
        self.__data = arg_data
        self.__share_data = self.__manager.list(arg_data)

    def get_data(self):
        return self.__data
    data = property(get_data, set_data)

    def run(self):
        self.__mp.clear()
        self.__status.clear()
        self.__result.clear()
        i = 0
        for plugins in self.__plugins:
            if plugins[AnalyzeFieldIdx.IDX_IS_EXECUTE.value]:
                name = plugins[AnalyzeFieldIdx.IDX_MODULE_NAME.value]
                plugins_class = __import__(
                    "analyze.plugins.%s" % (name), fromlist=[name])
                self.__mp.append(getattr(plugins_class, name)(
                    self.__data, self.__queue))
                self.__status.append(
                    [plugins[AnalyzeFieldIdx.IDX_ANALYE_NAME.value], Info.INFO_CALCULATING])
                i += 1

        for mp in self.__mp:
            mp.start()

    def is_result_exist(self):
        return len(self.__result)

    def is_alive(self):
        while any(i.is_alive() for i in self.__mp):
            return True

        return False

    def is_queue_empty(self):
        return self.__queue.empty()

    def retrive_data(self):
        while not self.__queue.empty():
            dataItem = self.__queue.get()
            if (dataItem[0] == RetriveType.DATA):
                self.__result.append(dataItem[1])
            elif (dataItem[0] == RetriveType.INFO):
                for i in range(len(self.__status)):
                    if (self.__status[i][0] == dataItem[1][0]):
                        self.__status[i][1] = dataItem[1][1]

    def get_plugins_count(self):
        return len(self.__mp)

    def get_status(self):
        return self.__status

    def get_column_info(self, arg_name):
        for plugin in self.__plugins:
            if plugin[AnalyzeFieldIdx.IDX_ANALYE_NAME.value] == arg_name:
                return plugin[AnalyzeFieldIdx.IDX_COLUMN_INFO.value]

        return None

    def get_result(self):
        return self.__result

    def export_analyze_result(self, arg_symbol):

        if not os.path.exists(DEF_EXPORT_FOLDER_NAME):
            os.makedirs(DEF_EXPORT_FOLDER_NAME)

        main_data = DataFrame(list(self.__data))
        main_data.columns = DEF_STOCK_COULMN_NAME

        result_data = []
        result_data.append(main_data)
        result_data += self.__result

        df = pd.concat(result_data, axis=1)

        filename = datetime.today().strftime(arg_symbol + "_%Y%m%d-%H%M%S.csv")

        try:
            df.to_csv(DEF_EXPORT_FOLDER_NAME +
                      os.sep + filename, sep=',', encoding='utf-8')
        except:
            return None

        return filename
