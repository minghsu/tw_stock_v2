#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Description:
# Check DB configurations
# Load DB configurations
# Write DB configurations

import os.path
import os

CONFIG_FILE_NAME = "CONFIG.FILE"


class DbConfigure:
    def __init__(self):
        self.__exist = True if (os.path.isfile(
            CONFIG_FILE_NAME) != 0) else False
        if (self.__exist == False or self.load() == False):
            self.__reset()

    def __reset(self):
        self.__host = "localhost"
        self.__module = ""
        self.__dbclass = ""
        self.__id = ""
        self.__pw = ""

    def save(self):
        bRet = True
        try:
            fp = open(CONFIG_FILE_NAME, "w")
            fp.writelines(self.__dbclass + "\n")
            fp.writelines(self.__module + "\n")
            fp.writelines(self.__host + "\n")
            fp.writelines(self.__id + "\n")
            fp.writelines(self.__pw + "\n")
        except:
            bRet = False
        else:
            fp.close()
        return bRet

    def load(self):
        bRet = True
        try:
            fp = open(CONFIG_FILE_NAME, "r")
            self.__dbclass = fp.readline().strip()
            self.__module = fp.readline().strip()
            self.__host = fp.readline().strip()
            self.__id = fp.readline().strip()
            self.__pw = fp.readline().strip()
        except:
            bRet = False
        else:
            fp.close()
        return bRet

    def isExist(self):
        return self.__exist

    def setModule(self, argModule):
        self.__module = argModule

    def getModule(self):
        return self.__module
    module = property(getModule, setModule)

    def setDbClass(self, argDbClass):
        self.__dbclass = argDbClass

    def getDbClass(self):
        return self.__dbclass
    dbClass = property(getDbClass, setDbClass)

    def setHost(self, argHost):
        self.__host = argHost

    def getHost(self):
        return self.__host
    host = property(getHost, setHost)

    def setId(self, argId):
        self.__id = argId

    def getId(self):
        return self.__id
    id = property(getId, setId)

    def setPw(self, argPw):
        self.__pw = argPw

    def getPw(self):
        return self.__pw
    pw = property(getPw, setPw)

    def __str__(self):
        return ("DB Module: " + self.__module
                + "\nDB DB Class: " + self.__dbclass
                + "\nDB Host: " + self.__host
                + "\nDB ID: " + self.__id
                + "\nDB PW: " + self.__pw)
