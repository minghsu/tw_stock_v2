#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import freeze_support
from controller import controller
import platform

TwStockController = controller()

if __name__ == "__main__":
    if (platform.system() == "Windows"):
        freeze_support()

    while (TwStockController.do_job()):
        pass
