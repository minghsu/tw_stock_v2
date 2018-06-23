#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from constant.state import State
from constant.error import Error
from constant.stock import SymbolField, ClassSupportField
from res.stringfactory import StringFactory
from consoles import consoles
from utils.switch import Switch
from modeler import modeler
from databases.dbconfigure import DbConfigure
from stock.stocksymbol import StockSymbol
from datetime import datetime

import time
import os.path
import commander
import viewer as viewer

DEF_MULIT_PROCESS_SELLP_TIMER = 2

# For dynamic update percentage
# Ex: 正在更新股票代號 9% ...
DEF_SYMBOL_UI_UPDATE_COUNT = 1000
DEF_VIEWER_DELAY_TIMER = 0.1


class controller:
    def __init__(self):
        self.__strFactory = StringFactory()
        self.__model = modeler()
        self.__consoles = consoles(self.__strFactory)
        self.__state = State.Startup
        self.__strCmd = None
        self.__parameter = None

    def __updating_message(self, arg_status):
        retStatus = ""
        for status in arg_status:
            if (status[1] == Error.ERR_TIMEOUT):
                tmp = "%s: %s" % (
                    status[0], self.__strFactory.get_string('STR_REQUEST_TIMEOUT'))
            else:
                tmp = "%s: %3d%%" % (status[0], status[1])

            if (retStatus != ""):
                retStatus = retStatus + "\n"
            retStatus = retStatus + tmp

        return retStatus

    def do_job(self):
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
                viewer.string(
                    self.__strFactory.get_string('STR_SYMBOL_DOWNLOADING'))
                viewer.empty_string()
                self.__stocksymbol = StockSymbol(self.__strFactory)
                time.sleep(DEF_MULIT_PROCESS_SELLP_TIMER)
                viewer.string(self.__updating_message(
                    self.__stocksymbol.get_status()))
                self.__fetchCount = self.__stocksymbol.get_fetch_count()
                self.__state = State.Downloading
                self.__stocksymbol.run()
                break
            if case(State.Downloading):
                self.__stocksymbol.retrive_data()
                viewer.move_cursor_up(self.__fetchCount)
                viewer.string(self.__updating_message(
                    self.__stocksymbol.get_status()))
                if (self.__stocksymbol.is_alive() == False):
                    viewer.empty_string()
                    self.__state = State.Updating
                else:
                    time.sleep(DEF_MULIT_PROCESS_SELLP_TIMER)
                break
            if case(State.Updating):
                # get result
                self.__symbolResult = self.__stocksymbol.get_result()
                # update current symbol list
                self.__model.fetch_symbol_list()

                strUpdatedDate = datetime.today().strftime("%Y/%m/%d")
                nSymbolCount = len(self.__symbolResult)
                if (nSymbolCount > 0):
                    for idx in range(nSymbolCount):
                        self.__model.update_stock_symbol(
                            self.__symbolResult[idx], strUpdatedDate)

                        if (idx % DEF_SYMBOL_UI_UPDATE_COUNT == 0):
                            if (idx != 0):
                                viewer.move_cursor_up(1)
                            viewer.string(self.__strFactory.get_string(
                                'STR_SYMBOL_UPDATING') % (idx/nSymbolCount * 100))
                            time.sleep(DEF_VIEWER_DELAY_TIMER)

                    # Just for UI friendly ( show 100% finished )
                    viewer.move_cursor_up(1)
                    viewer.string(self.__strFactory.get_string(
                        'STR_SYMBOL_UPDATING') % (100))

                # update final symbol list and update lost count of stock symbol
                self.__model.fetch_symbol_list()
                viewer.string(self.__strFactory.get_string(
                    'STR_SYMBOL_UPDATED') % (self.__model.get_symbol_count()))

                self.__state = State.Input
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
            if case(State.CmdUse):
                symbol_info = self.__model.get_symbol_info(self.__parameter)
                if (symbol_info != None):
                    self.__consoles.set_used_symbol(self.__parameter)
                    self.__model.create_symbol_data_table(self.__parameter)
                    self.__model.fetch_symbol_trade_date_list(self.__parameter)

                    last_trade_date = self.__model.get_symbol_last_trade_date()
                    if (last_trade_date == None):
                        last_trade_date = self.__strFactory.get_string(
                            'STR_NOT_AVAILABLE')
                    viewer.string(
                        self.__strFactory.get_string('STR_SYMBOL_INFO') % (
                            symbol_info[SymbolField.IDX_SYMBOL.value],
                            symbol_info[SymbolField.IDX_NAME.value],
                            symbol_info[SymbolField.IDX_CREATE_DATE.value],
                            symbol_info[SymbolField.IDX_UPDATED_DATE.value],
                            self.__model.get_symbol_trade_count(),
                            last_trade_date))
                else:
                    viewer.string(
                        self.__strFactory.get_string('STR_SYMBOL_NOT_FOUND') % (self.__parameter))
                    self.__parameter = ""

                self.__state = State.Input
                break
        return True
