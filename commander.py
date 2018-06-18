#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from constant.state import State
from utils.switch import Switch


def cmdParser(argCommand):

    retState = State.Input

    splitCmd = argCommand.split(" ")

    for case in Switch(splitCmd[0]):
        if case("exit"):
            retState = State.Exit
            break
        if case("help"):
            retState = State.Help
            break
        if case("config"):
            retState = State.Configure
            break

    return retState
