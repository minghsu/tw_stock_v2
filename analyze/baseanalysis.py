#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import abc


class BaseAnalyer(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def name(self):
        # must provide analyze name
        return NotImplemented

    @abc.abstractmethod
    def colnum_info(self):
        # must provide analyze result columns (Ex:  [3, ["K", "D", "J"]])
        return NotImplemented
