#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from enum import Enum, unique


@unique
class Error(Enum):
    ERR_NONE = 0
    ERR_TIMEOUT = 1
