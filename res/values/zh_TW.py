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
                            "PS. 本設定將直接儲存為 XML 檔案。\n"),
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
    "STR_SYMBOL_DOWNLOADING": "下載中 ...",
    "STR_SYMBOL_UPDATING": "更新中 %3d %% ...",
    "STR_SYMBOL_UPDATED": "股票代號更新完成, 共有 %d 筆股票代號",
    "STR_HELP_MESSAGE": ("TW STOCK 命令交談模式幫助資訊:\n"
                         "輸入: help > 顯示幫助資訊\n"
                         "      exit > 離開系統\n"
                         "      config > 重新設定資料庫連線資訊\n"
                         "      use [股票代號] > 指定股票代號\n"
                         "      fetch > 下載股票收盤資料\n"
                         "      analyze ?> 顯示已支援的技術分析\n"
                         "      analyze > 執行技術分析\n"
                         "      export > 輸出分析計算結果至 csv 格式檔案"),
    "STR_SYMBOL_NOT_FOUND": "查無 %s 股票代號 ...",
    "STR_SYMBOL_INFO": " >>> 代號: %s, 名稱: %s, 上市日期: %s, 最後更新: %s, 交易總筆數: %d, 最後交易日: %s",
    "STR_SYMBOL_REQUEST_TIMEOUT": "連線要求逾時 ...",
    "STR_NOT_AVAILABLE": "不存在",
    "STR_PREPARE_FETCH_STOCK_DATA": "準備截取 '%s' 股市收盤資料, 由 %s/%s 至 %s/%s",
    "STR_STOCK_DATA_REQUEST_TIMEOUT": "%s: 截取 %s/%s 資料失敗, 預計 20 秒後重試.",
    "STR_STOCK_DATA_UPDATING": "%s: 正在更新 %s/%s 資料",
    "STR_STOCK_ANALYSIS_SUPPORTED": "支持的技術分析: %s",
    "STR_CALCULATING": "正在計算中 ...",
    "STR_CALCULATED": "已計算完成",
    "STR_EXPORT_OK": " >>> 匯出 %s 檔案成功",
    "STR_EXPORT_FAIL": " >>> 匯出檔案失敗",
}
