#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import abc


class Analyer(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def name(self):
        # must provide analyze name
        return NotImplemented

    @abc.abstractmethod
    def result_colnums(self):
        # must provide analyze result columns (report by list)
        return NotImplemented
