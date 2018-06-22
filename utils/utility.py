#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from constant.stock import SymbolField


def util_is_symbol_exist(argStockList, argSymbol):
    # (('911613', '特藝-DR', '2011/02/25'), ('9949', '琉園', '2003/11/21'))
    lo, hi = 0, len(argStockList) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if argStockList[mid][0] < argSymbol:
            lo = mid + 1
        elif argSymbol < argStockList[mid][0]:
            hi = mid - 1
        elif argSymbol == argStockList[mid][0]:
            return mid

    return None
