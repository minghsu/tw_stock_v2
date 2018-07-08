#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from constant.state import State
from constant.stock import SymbolField, ClassSupportField, Info
from res.stringfactory import StringFactory
from consoles import consoles
from utils.switch import Switch
from modeler import modeler
from databases.dbconfigure import DbConfigure
from stock.stocksymbol import StockSymbol
from stock.stockdata import StockData
from datetime import datetime
from utils.utility import util_get_basename
from analyze.analyzer import Analyer

import time
import commander
import viewer as viewer
import logging

DEF_MULIT_PROCESS_SELLP_TIMER = 1
DEF_LENGTH_STOCK_DATA_MESSAGE = 60


class controller:
    def __init__(self):
        self.__strFactory = StringFactory()
        self.__model = modeler()
        self.__consoles = consoles(self.__strFactory)
        self.__state = State.Startup
        self.__strCmd = None
        self.__parameter = None
        self.__symbol_info = None
        self.__symbol = None
        self.__logging = logging.getLogger(util_get_basename(__file__))
        self.__analyzer = None

    def __update_symbol_use_info(self):
        last_trade_date = self.__model.get_stock_last_trade_date()
        if (last_trade_date == None):
            last_trade_date = self.__strFactory.get_string(
                'STR_NOT_AVAILABLE')

        retStatus = self.__strFactory.get_string('STR_SYMBOL_INFO') % (self.__symbol_info[SymbolField.IDX_SYMBOL.value],
                                                                       self.__symbol_info[SymbolField.IDX_NAME.value],
                                                                       self.__symbol_info[SymbolField.IDX_CREATE_DATE.value],
                                                                       self.__symbol_info[SymbolField.IDX_UPDATED_DATE.value],
                                                                       self.__model.get_symbol_trade_count(),
                                                                       last_trade_date)
        return retStatus

    def __update_analysis_info(self, arg_status):
        return
        retStatus = ""
        for status in arg_status:
            tmp = "%10s: %s" % (
                status[0], self.__strFactory.get_string(status[1].value))

            if (retStatus != ""):
                retStatus = retStatus.ljust(
                    DEF_LENGTH_STOCK_DATA_MESSAGE, " ") + "\n"
            retStatus = retStatus + tmp

        return retStatus

    def __updating_symbol_message(self, arg_status):
        retStatus = ""
        for status in arg_status:
            if (status[1] == Info.INFO_SYMBOL_DOWNLOAD_TIMEOUT or
                    status[1] == Info.INFO_SYMBOL_DOWNLOADING):
                tmp = "%s: %s" % (
                    self.__strFactory.get_string(status[0]), self.__strFactory.get_string(status[1].value))
            else:
                tmp = self.__strFactory.get_string(status[0]) + ": " + (self.__strFactory.get_string(
                    'STR_SYMBOL_UPDATING') % (status[1]))

            if (retStatus != ""):
                retStatus = retStatus.ljust(
                    DEF_LENGTH_STOCK_DATA_MESSAGE, " ") + "\n"
            retStatus = retStatus + tmp

        return retStatus

    def __updating_stock_data_message(self, arg_status):
        retStatus = ""
        for status in arg_status:
            if (status[1] == Info.INFO_STOCK_DATA_DOWNLOAD_TIMEOUT):
                tmp = self.__strFactory.get_string(Info.INFO_STOCK_DATA_DOWNLOAD_TIMEOUT.value) % (
                    status[0], status[1][:4], status[1][4:])

            else:
                tmp = self.__strFactory.get_string('STR_STOCK_DATA_UPDATING') % (
                    status[0], status[1][:4], status[1][4:])

            if (retStatus != ""):
                retStatus = retStatus.ljust(
                    DEF_LENGTH_STOCK_DATA_MESSAGE, " ") + "\n"
            retStatus = retStatus + tmp

        return retStatus

    def do_job(self):
        self.__logging.debug(self.__state)
        for case in Switch(self.__state):
            if case(State.Exit):
                self.__model.close()
                return False
            if case(State.Startup):
                viewer.empty_string()
                viewer.bold_string(self.__strFactory.get_string(
                    'STR_WELCOME') % (self.__strFactory.get_version()))
                viewer.empty_string()
                self.__state = State.DbCheck
                break
            if case(State.Reconfigure):
                viewer.empty_string()
                if (self.__consoles.get_confirm(self.__strFactory.get_string('STR_DB_RE_CONFIG'), False)):
                    self.__state = State.Configure
                    viewer.empty_string()
                else:
                    self.__state = State.Exit
                break
            if case(State.DbCheck):
                self.__config = DbConfigure()
                self.__state = State.Connect if (
                    self.__config.isExist() != False) else State.Configure
                break
            if case(State.Connect):
                # Check the db module was installed or not
                if (self.__model.is_db_module_exist(self.__config.module) == False):
                    viewer.warning_string(
                        self.__strFactory.get_string('STR_DB_MODULE_MISSED') % (self.__config.module))
                    self.__state = State.Exit
                else:
                    if (self.__model.connect(self.__config.dbClass,
                                             self.__config.module,
                                             self.__config.host,
                                             self.__config.id,
                                             self.__config.pw) == False):
                        viewer.warning_string(
                            self.__strFactory.get_string('STR_DB_CONNECT_ERROR'))
                        self.__state = State.Reconfigure
                    else:
                        viewer.string(self.__strFactory.get_string(
                            'STR_DB_CONNECTED') % (self.__model.get_rmdb_name()))
                        self.__state = State.Open
                break
            if case(State.Open):
                if (self.__model.open() == False):
                    viewer.warning_string(
                        self.__strFactory.get_string('STR_DB_OPEN_FAIL'))
                    self.__state = State.Exit
                else:
                    self.__state = State.Update
                break
            if case(State.Update):
                viewer.empty_string()
                self.__stocksymbol = StockSymbol()
                self.__fetch_symbol_count = self.__stocksymbol.get_fetch_count()
                self.__model.fetch_symbol_list()
                self.__state = State.Updating
                self.__symbol_info_updated_date = datetime.today().strftime("%Y/%m/%d")
                viewer.string(self.__updating_symbol_message(
                    self.__stocksymbol.get_status()))
                self.__stocksymbol.run()
                time.sleep(DEF_MULIT_PROCESS_SELLP_TIMER)
                break
            if case(State.Updating):
                self.__stocksymbol.retrive_data()
                viewer.move_cursor_up(self.__fetch_symbol_count)
                viewer.string(self.__updating_symbol_message(
                    self.__stocksymbol.get_status()))

                symbol_info = self.__stocksymbol.get_result()
                while (symbol_info != None):
                    self.__model.update_stock_symbol(
                        symbol_info[1], self.__symbol_info_updated_date)
                    symbol_info = self.__stocksymbol.get_result()

                if (self.__stocksymbol.is_alive() == False
                        and self.__stocksymbol.is_queue_empty()):
                    self.__model.fetch_symbol_list()
                    viewer.string(self.__strFactory.get_string(
                        'STR_SYMBOL_UPDATED') % (self.__model.get_symbol_count()))
                    viewer.empty_string()
                    self.__state = State.Input
                else:
                    time.sleep(DEF_MULIT_PROCESS_SELLP_TIMER)
                break
            if case(State.Configure):
                viewer.warning_string(self.__strFactory.get_string(
                    'STR_CONFIG_DATABASE'))
                lst_db_supported_modules = self.__model.get_db_module_list()

                if (len(lst_db_supported_modules)):
                    viewer.bold_string(
                        self.__strFactory.get_string('STR_DB_SUPPORT_LIST'))
                    for i in range(len(lst_db_supported_modules)):
                        viewer.string("%d. %s" %
                                      (i+1, lst_db_supported_modules[i][ClassSupportField.IDX_RMDB_NAME.value]))

                    nChoose = self.__consoles.getValue(
                        self.__strFactory.get_string('STR_DB_SELECT'), 1, len(lst_db_supported_modules))
                    # Ex: MySQL (0), MariabDB/MySQL, MySQLdb (2)
                    # 0 > dynamic import the class on DbFactory.py
                    # 2 > dynamice import the db module (Ex: pymysql, MySQLdb or psycopg2 )
                    self.__config.dbClass = lst_db_supported_modules[nChoose -
                                                                     1][ClassSupportField.IDX_CLASS_NAME.value]
                    self.__config.module = lst_db_supported_modules[nChoose -
                                                                    1][ClassSupportField.IDX_MODULE_NAME.value]
                    self.__config.host = self.__consoles.get_string(
                        self.__strFactory.get_string('STR_DB_HOST'), self.__config.host)
                    self.__config.id = self.__consoles.get_string(
                        self.__strFactory.get_string('STR_DB_ID'), self.__config.id)
                    self.__config.pw = self.__consoles.get_string(
                        self.__strFactory.get_string('STR_DB_PW'), self.__config.pw)

                    viewer.empty_string()

                    if (self.__config.save() == False):
                        viewer.warning_string(
                            self.__strFactory.get_string('STR_DB_CONF_SAVE_ERROR'))
                        self.__state == State.Exit
                    else:
                        self.__state = State.Connect
                else:
                    viewer.warning_string(
                        self.__strFactory.get_string('STR_DB_NOT_DETECTED'))
                    self.__state = State.Exit
                break
            if case(State.Input):
                self.__strCmd = self.__consoles.getCommand()
                self.__strCmd = self.__strCmd.lower()
                self.__state, self.__parameter = commander.cmdParser(
                    self.__strCmd)
                break
            if case(State.CmdHelp):
                viewer.empty_string()
                viewer.string(
                    self.__strFactory.get_string('STR_HELP_MESSAGE'))
                self.__state = State.Input
                viewer.empty_string()
                break
            if case(State.CmdError):
                viewer.warning_string(
                    self.__strFactory.get_string('STR_UNKNOWN_COMMAND'))
                self.__state = State.Input
                break
            if case(State.CmdFetch):
                if (self.__symbol_info):
                    stock_list = []

                    stock_symbol = self.__symbol_info[SymbolField.IDX_SYMBOL.value]
                    stock_stop_date = datetime.today().strftime("%Y%m")

                    stock_start_date = self.__model.get_stock_last_trade_date()
                    if (stock_start_date == None):
                        stock_start_date = self.__symbol_info[SymbolField.IDX_CREATE_DATE.value]
                    else:
                        stock_start_date = stock_start_date
                    stock_start_date = datetime.strptime(
                        stock_start_date, '%Y/%m/%d').strftime("%Y%m")

                    stock_list.append(
                        [stock_symbol, stock_start_date, stock_stop_date])
                    self.__stockdata = StockData(stock_list)
                    self.__fetch_stock_count = self.__stockdata.get_fetch_count()

                    viewer.empty_string()
                    for i in range(self.__fetch_stock_count):
                        viewer.bold_string(self.__strFactory.get_string(
                            'STR_PREPARE_FETCH_STOCK_DATA') % (stock_list[i][0],
                                                               stock_list[i][1][:4],
                                                               stock_list[i][1][4:],
                                                               stock_list[i][2][:4],
                                                               stock_list[i][2][4:]))

                    viewer.string(self.__updating_stock_data_message(
                        self.__stockdata.get_status()))
                    self.__stockdata.run()
                    self.__state = State.Fetching
                else:
                    self.__state = State.CmdError
                break
            if case(State.Fetching):
                self.__stockdata.retrive_data()
                viewer.move_cursor_up(self.__fetch_stock_count)
                viewer.string(self.__updating_stock_data_message(
                    self.__stockdata.get_status()))

                stock_data = self.__stockdata.get_result()
                while (stock_data != None):
                    self.__model.update_stock_data(stock_data)
                    stock_data = self.__stockdata.get_result()

                if (self.__stockdata.is_alive() == False
                        and self.__stockdata.is_queue_empty()):
                    self.__model.fetch_all_stock_data(self.__symbol)
                    viewer.bold_string(self.__update_symbol_use_info())
                    viewer.empty_string()
                    self.__state = State.Input
                else:
                    time.sleep(DEF_MULIT_PROCESS_SELLP_TIMER)
                break
            if case(State.CmdUse):
                self.__symbol = self.__parameter
                self.__symbol_info = self.__model.get_symbol_info(
                    self.__symbol)
                if (self.__symbol_info != None):
                    self.__consoles.set_used_symbol(self.__symbol)
                    self.__model.create_stock_data_table(self.__symbol)
                    self.__model.fetch_all_stock_data(self.__symbol)
                    viewer.bold_string(self.__update_symbol_use_info())
                else:
                    viewer.string(
                        self.__strFactory.get_string('STR_SYMBOL_NOT_FOUND') % (self.__symbol))
                    self.__parameter = ""

                self.__state = State.Input
                break
            if case(State.Analyze):
                self.__analyzer = Analyer()
                if self.__parameter == "?":
                    viewer.empty_string()
                    viewer.string(self.__strFactory.get_string(
                        'STR_STOCK_ANALYSIS_SUPPORTED') % (self.__analyzer.get_plugins()))
                    viewer.empty_string()
                    self.__state = State.Input
                else:
                    self.__analyzer.set_data(self.__model.get_stock_data())
                    self.__analyzer.run()
                    self.__state = State.Analying
                    viewer.string(self.__update_analysis_info(
                        self.__analyzer.get_status()))
                    time.sleep(DEF_MULIT_PROCESS_SELLP_TIMER)
                break
            if case(State.Analying):
                self.__analyzer.retrive_data()
                viewer.move_cursor_up(self.__analyzer.get_plugins_count())
                viewer.string(self.__update_analysis_info(
                    self.__analyzer.get_status()))

                if (self.__analyzer.is_alive() == False and
                        self.__analyzer.is_queue_empty()):
                    viewer.move_cursor_up(self.__analyzer.get_plugins_count())
                    viewer.string(self.__update_analysis_info(
                        self.__analyzer.get_status()))
                    self.__state = State.Input
                else:
                    time.sleep(DEF_MULIT_PROCESS_SELLP_TIMER)
                break
        return True
