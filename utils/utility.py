#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from constant.stock import SymbolField


def util_binary_search_idx(arg_stock_list, arg_list_idx, arg_com_data):

    if (isinstance(arg_stock_list, (tuple, list))):
        lo, hi = 0, len(arg_stock_list) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arg_stock_list[mid][0] < arg_com_data:
                lo = mid + 1
            elif arg_com_data < arg_stock_list[mid][0]:
                hi = mid - 1
            elif arg_com_data == arg_stock_list[mid][0]:
                return mid

    return None


def util_convert_roc_to_ad_year(arg_roc_year):
    tmpYear = arg_roc_year[0:arg_roc_year.find("/")]
    return str((int(tmpYear)+1911)) + arg_roc_year[arg_roc_year.find("/"):]
