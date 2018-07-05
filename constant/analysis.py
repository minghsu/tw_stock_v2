#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from enum import Enum, unique


@unique
class AnalyzeFieldIdx(Enum):
    IDX_MODULE_NAME = 0
    IDX_ANALYE_NAME = 1
    IDX_COLUMN_INFO = 2
    IDX_IS_EXECUTE = 3
