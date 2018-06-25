#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Description:
# Check DB configurations
# Load DB configurations
# Write DB configurations

import os.path
import os

from lxml import etree

CONFIG_XML_FILE = "configuration.xml"


class DbConfigure:
    def __init__(self):
        self.__exist = True if (os.path.isfile(
            CONFIG_XML_FILE) != 0) else False
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
            configuration = etree.Element("configuration")
            rmdbs = etree.SubElement(configuration, 'rmdbs')

            db_class = etree.SubElement(rmdbs, "class")
            db_class.text = self.__dbclass
            db_module = etree.SubElement(rmdbs, "module")
            db_module.text = self.__module
            db_host = etree.SubElement(rmdbs, "host")
            db_host.text = self.__host
            db_id = etree.SubElement(rmdbs, "id")
            db_id.text = self.__id
            db_pw = etree.SubElement(rmdbs, "pw")
            db_pw.text = self.__pw

            tree = etree.ElementTree(configuration)
            tree.write(CONFIG_XML_FILE, pretty_print=True,
                       xml_declaration=True, encoding='utf-8')
        except:
            bRet = False
        return bRet

    def load(self):
        bRet = True

        try:
            xml = etree.parse(CONFIG_XML_FILE)
            configuration = xml.getroot()

            xml_node = configuration.xpath("rmdbs//class")
            self.__dbclass = xml_node[0].text
            xml_node = configuration.xpath("rmdbs//module")
            self.__module = xml_node[0].text
            xml_node = configuration.xpath("rmdbs//host")
            self.__host = xml_node[0].text
            xml_node = configuration.xpath("rmdbs//id")
            self.__id = xml_node[0].text
            xml_node = configuration.xpath("rmdbs//pw")
            self.__pw = xml_node[0].text
        except:
            bRet = False
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
