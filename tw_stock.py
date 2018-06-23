#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import freeze_support
from controller import controller
import platform

TwStockController = controller()

if __name__ == "__main__":

    platform_name = platform.system()
    if (platform_name == "Windows"):
        freeze_support()

    while (TwStockController.do_job()):
        pass
