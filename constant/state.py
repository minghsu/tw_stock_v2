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
    # Check DB Configurations
    DbCheck = 7
    # Exit
    Exit = 8
    # Re-Config DB
    Reconfigure = 9
    # Open Database
    Open = 10
    # Updating the stock symbol
    Updating = 11
    # show help message
    CmdHelp = 12
    # command error
    CmdError = 13
    # use command
    CmdUse = 14
    # fetch command
    CmdFetch = 15
    # Analying
    Analying = 16
    # Export
    CmdExport = 17
