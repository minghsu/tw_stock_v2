#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from importlib import util
from multiprocessing import managers
from constant.analysis import AnalyzeFieldIdx

import os


class Analyer:
    def __init__(self):
        self.__plugins = []
        self.__mp = []
        tmpList = os.listdir("analyze/plugins/")
        for filename in tmpList:
            name, ext = os.path.splitext(filename)
            if (filename != "__init__.py" and ext == ".py"):
                plugins_class = __import__("analyze.plugins.%s" %
                                           (name), fromlist=[name])
                instanceClass = getattr(plugins_class, name)()
                self.__plugins.append(
                    [name, instanceClass.name(), instanceClass.colnum_info(), True])

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
