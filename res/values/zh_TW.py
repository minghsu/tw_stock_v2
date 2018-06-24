#!/usr/bin/env python3
# -*- coding:utf-8 -*-

DICT_STR_RESOURCE = {
    "STR_NOT_DEFINED": "未定義的字串",
    "STR_WELCOME": ("歡迎使用 %s, (C)Copyright 2018, Hsu Chih-Ming\n"
                    "輸入 'help' 指令以取得求助訊息"),
    "STR_CLI_PREFIX": "TW STOCK [%s] >",
    "STR_CLI_NONE": "未指定",
    "STR_VERSION": "TW STOCK 版本 %d.%d",
    "STR_UNKNOWN_COMMAND": "無法理解的指令或是不正確的參數!",
    "STR_DB_CONNECT_ERROR": "無法連接資料庫，請確認設定值是否正確?",
    "STR_CONFIG_DATABASE": ("資料庫連線資訊設定作業，請依指示提供伺服器位址，帳號與密碼。\n"
                            "請確保該帳密有建立資料庫和資料表的權限，系統將自行產生相關資料。\n"
                            "PS. 本設定將直接儲存為純文字檔案，請妥善保存。\n"),
    "STR_DB_SUPPORT_LIST": "系統偵測到下列 Python 資料庫套件:",
    "STR_DB_SELECT": "請選擇欲使用的資料庫系統?",
    "STR_DB_NOT_DETECTED": "系統無法偵測到相關資料庫套件!!",
    "STR_DB_HOST": "請輸入資料庫伺服器位址%s:",
    "STR_DB_ID": "請輸入資料庫帳號%s:",
    "STR_DB_PW": "請輸入資料庫密碼%s:",
    "STR_DB_CONF_SAVE_ERROR": "寫入資料庫設定檔失敗!",
    "STR_DB_RE_CONFIG": "是否重新設定資料庫連線資訊?",
    "STR_DB_CONNECTED": "%s 資料庫已連線",
    "STR_DB_OPEN_FAIL": "無法開啟資料庫檔案!",
    "STR_DB_MODULE_MISSED": "%s 未安裝, 無法連接資料庫!",
    "STR_LISTED_COMPANY": "上市公司",
    "STR_OTC_COMPANY": "上櫃公司",
    "STR_MODULE_MISSED": "'%s' 套件未安裝!",
    "STR_SYMBOL_DOWNLOADING": "正在下載股票代號資料 ...",
    "STR_SYMBOL_UPDATING": "正在更新股票代號 %d%% ...",
    "STR_SYMBOL_UPDATED": "股票代號更新完成, 共有 %d 筆股票代號",
    "STR_HELP_MESSAGE": ("TW STOCK 命令交談模式幫助資訊:\n"
                         "輸入: help > 顯示幫助資訊\n"
                         "      show > 顯示系統, 資料庫等基本資訊\n"
                         "      exit > 離開系統\n"
                         "      config > 重新設定資料庫連線資訊\n"
                         "      use [symbol] > 指定股票代號\n"
                         "      fetch > 下載股票收盤資料\n"
                         "      analyze > 顯示已支援的技術分析, 以及目前已設定的狀態\n"
                         "      add [analyze type] > 設定要執行的技術分析\n"
                         "      remove [analyze type] > 移除要執行的技術分析"),
    "STR_SYMBOL_NOT_FOUND": "查無 %s 股票代號 ...",
    "STR_SYMBOL_INFO": " >>> 代號: %s, 名稱: %s, 上市日期: %s, 最後更新: %s, 交易總筆數: %d, 最後交易日: %s",
    "STR_REQUEST_TIMEOUT": "連線要求逾時.",
    "STR_DOWNLOADING": "下載中 ...",
    "STR_NOT_AVAILABLE": "不存在",
    "STR_STOCK_DATA_FROM_1993": "收盤資料從1993年開始收錄, 系統將依情況自動調整擷取日期."
}
