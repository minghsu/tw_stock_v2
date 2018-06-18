#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import importlib
import locale

DEF_MAJOR_VERSION = 2
DEF_MINOR_VERSION = 0


class StringFactory:
    def __init__(self):
        self.__locale = locale.getdefaultlocale()[0]
        try:
            self.__module = importlib.import_module(
                "res.values.%s" % (self.__locale))
        except:
            self.__module = importlib.import_module("res.values.en_US")
        self.__dict = self.__module.DICT_STR_RESOURCE

    def get_version(self):
        return (self.__dict['STR_VERSION'] % (DEF_MAJOR_VERSION, DEF_MINOR_VERSION))

    def get_string(self, argKey):
        try:
            return self.__dict[argKey]
        except:
            return self.__dict['STR_NOT_DEFINED']
