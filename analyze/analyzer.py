#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from importlib import util


class Analyer:
    def __init__(self):
        self.__list_plugins = []
        tmpList = os.listdir("analyze/plugins/")
        for filename in tmpList:
            name, ext = os.path.splitext(filename)
            if (filename != "__init__.py" and ext == ".py"):
                plugins_class = __import__("analyze.plugins.%s" %
                                           (name), fromlist=[name])
                instanceClass = getattr(plugins_class, name)()

                self.__list_plugins.append(
                    [name, instanceClass.name(), instanceClass.colnum_info()])

    def get_plugins(self):
        retPlugins = ""
        for plugins in self.__list_plugins:
            if retPlugins != "":
                retPlugins = retPlugins + ", "
            retPlugins = retPlugins + plugins[1]

        return retPlugins
