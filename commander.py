#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from constant.state import State
from utils.switch import Switch


def cmdParser(argCommand):

    retState = State.CmdError
    retParameter = None

    splitCmd = argCommand.split(" ")

    for case in Switch(splitCmd[0]):
        if case("exit"):
            retState = State.Exit
            break
        if case("help"):
            retState = State.CmdHelp
            break
        if case("config"):
            retState = State.Configure
            break
        if case("use"):
            if (len(splitCmd) > 1):
                retParameter = splitCmd[1]
                retState = State.CmdUse
            break
        if case("fetch"):
            retState = State.CmdFetch
            break

    return (retState, retParameter)
