#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from enum import Enum, unique


@unique
class State(Enum):
    # System Start Up
    Startup = 0
    # 1st time, to configure the arguments of database
    Configure = 1
    # Connect to database
    Connect = 2
    # Loading/Updating the stock code
    Update = 3
    # Waiting the command
    Input = 4
    # Fetching the record of the stock
    Fetching = 5
    # Stock analyzing ( Ex: KDJ, MACD, etc )
    Analyze = 6
    # Export the analyzed result
    Export = 7
    # Check DB Configurations
    DbCheck = 8
    # Exit
    Exit = 9
    # Re-Config DB
    Reconfigure = 10
    # Open Database
    Open = 11
    # Updating the stock symbol
    Updating = 12
    # Downloading the stock symbol data
    Downloading = 13
    # show help message
    CmdHelp = 14
    # command error
    CmdError = 15
    # use command
    CmdUse = 16
    # fetch command
    CmdFetch = 17
    # Analying
    Analying = 18
    # Export
    CmdExport = 19
