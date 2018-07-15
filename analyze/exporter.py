#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from constant.analysis import AnalyzeFieldIdx
from pandas.core.frame import DataFrame
import pandas as pd

DEF_STOCK_COULMN_NAME = ["Date", "Volumn", "Money", "Open",
                         "Max", "Min", "Close", "Spread", "Count"]


def get_column_name(arg_name, arg_plugins):
    for plugin in arg_plugins:
        if arg_name == plugin[AnalyzeFieldIdx.IDX_ANALYE_NAME.value]:
            return plugin[AnalyzeFieldIdx.IDX_COLUMN_INFO.value]

    return None


def export_analyze_result(arg_filename, arg_data, arg_plugins, arg_result):
    main_data = DataFrame(list(arg_data))
    main_data.columns = DEF_STOCK_COULMN_NAME

    result_data = []
    result_data.append(main_data)
    for result in arg_result:
        df = DataFrame(result[1])
        df.columns = get_column_name(result[0], arg_plugins)
        result_data.append(df)

    df = pd.concat(result_data, axis=1)
    print(df)
