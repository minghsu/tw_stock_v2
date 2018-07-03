#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import freeze_support
from datetime import datetime
from controller import controller

import platform
import logging
import os

DEF_LOG_FOLDER_NAME = "logfile"


TwStockController = controller()

if __name__ == "__main__":

    platform_name = platform.system()
    if (platform_name == "Windows"):
        freeze_support()

    if not os.path.exists(DEF_LOG_FOLDER_NAME):
        os.makedirs(DEF_LOG_FOLDER_NAME)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        handlers=[logging.FileHandler(datetime.today().strftime(DEF_LOG_FOLDER_NAME + os.sep + "tw_stock_%Y%m%d%H%M%S.log"), 'w', 'utf-8'), ])

    while (TwStockController.do_job()):
        pass
