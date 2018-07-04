#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from .. baseanalysis import BaseAnalyer


class macd(BaseAnalyer):
    def __init__(self):
        pass

    def name(self):
        return "MACD"

    def colnum_info(self):
        return (1, ("MACD"))
