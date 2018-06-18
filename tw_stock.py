#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from controller import controller
TwStockController = controller()

while (TwStockController.do_job()):
    pass
