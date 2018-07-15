#!/usr/bin/env python3
# -*- coding:utf-8 -*-

DICT_STR_RESOURCE = {
    "STR_NOT_DEFINED": "The string was not defined",
    "STR_WELCOME": ("Welcome to use %s, (C)Copyright 2018, Hsu Chih-Ming\n"
                    "Type 'help' for help."),
    "STR_CLI_PREFIX": "TW STOCK [%s] >",
    "STR_CLI_NONE": "None",
    "STR_VERSION": "TW STOCK Version %d.%d",
    "STR_UNKNOWN_COMMAND": "Unkonwn command or invalid parameter!",
    "STR_DB_CONNECT_ERROR": "Can't connected to database, please help to check the configurations.",
    "STR_CONFIG_DATABASE": ("The database connection info is configurating.\n"
                            "Please follow the indicate to provide the HOST, ID & PW info.\n"
                            "Please confirm the ID have the CREATE DATABASE/TABLE permissions.\n"
                            "PS. The LOGIN info were store in XML file.\n"),
    "STR_DB_SUPPORT_LIST": "System detected below DB packages for Python:",
    "STR_DB_SELECT": "Pleass select which DB system will be use?",
    "STR_DB_NOT_DETECTED": "System can't detect the database pacakges!!",
    "STR_DB_HOST": "Please input the DB host address:",
    "STR_DB_ID": "Please input the ID:",
    "STR_DB_PW": "Please input the PW:",
    "STR_DB_CONF_SAVE_ERROR": "Can't save the configuration of database!",
    "STR_DB_RE_CONFIG": "Do you want to re-configure the database connect info?",
    "STR_DB_CONNECTED": "%s database connected",
    "STR_DB_OPEN_FAIL": "Can't open the database file!",
    "STR_DB_MODULE_MISSED": "The %s package not installed, system can't connect to database!",
    "STR_LISTED_COMPANY": "Listed Company",
    "STR_OTC_COMPANY": "OTC Company",
    "STR_MODULE_MISSED": "The '%s' package missed!",
    "STR_SYMBOL_DOWNLOADING": "Downloading ...",
    "STR_SYMBOL_UPDATING": "Updating %3d %% ...",
    "STR_SYMBOL_UPDATED": "The stock symbol already updated, there are %d stock symbols.",
    "STR_HELP_MESSAGE": ("The help information of TW STOCK in the interaction mode:\n"
                         "Type: help > Show this help information\n"
                         "      exit > Exit\n"
                         "      config > Re-configuration the database connection info."
                         "      use [symbol] > Set to use withc stock symbol\n"
                         "      fetch > Fetch the historical closing information\n"
                         "      analyze ?> Display all supported technical analysis\n"
                         "      analyze > Start to execute the technical analysis.\n"
                         "      export [file name] > Export the analysis result to .csv file.\n"),
    "STR_SYMBOL_NOT_FOUND": "Can't found the %s stock symbol ...",
    "STR_SYMBOL_INFO": " >>> Symbol: %s, Name: %s, Listed Date: %s, Last Update: %s, Total Trade Count: %d, Last Trade Date: %s",
    "STR_SYMBOL_REQUEST_TIMEOUT": "Download request timeout.",
    "STR_NOT_AVAILABLE": "Not Available",
    "STR_PREPARE_FETCH_STOCK_DATA": "Preparing to fetch '%s' stock data from %s/%s to %s/%s",
    "STR_STOCK_DATA_REQUEST_TIMEOUT": "%s: Download %s/%s data fail, will try again after 20s.",
    "STR_STOCK_DATA_UPDATING": "%s: Updating %s/%s data",
    "STR_STOCK_ANALYSIS_SUPPORTED": "Supported stock analysis: %s",
    "STR_CALCULATING": "Calculating ...",
    "STR_CALCULATED": "Calculated !",
}
