#!/usr/bin/env python3
# -*- coding:utf-8 -*-

DEF_CONSOLES_SUFFIX = " "


class consoles:
    def __init__(self, arg_string_factory):
        self.__resString = arg_string_factory
        self.__used = self.__resString.get_string('STR_CLI_NONE')

    def getCommand(self):
        return input(self.__resString.get_string('STR_CLI_PREFIX') % (self.__used) + DEF_CONSOLES_SUFFIX)

    def getValue(self, arg_string, arg_min, arg_max):
        num = 0
        while (True):
            # Just to avoid none value input
            try:
                num = int(input(arg_string + DEF_CONSOLES_SUFFIX))
                if (num >= arg_min and num <= arg_max):
                    break
            except:
                continue
        return num

    def get_string(self, arg_string, arg_def_string):
        retString = ""

        if (len(arg_def_string) > 0):
            promptString = arg_string % ("[" + arg_def_string + "]")
        else:
            promptString = arg_string % (arg_def_string)

        while (True):
            inputString = input(promptString + DEF_CONSOLES_SUFFIX)

            if (len(inputString) > 0):
                retString = inputString
                break
            if (len(inputString) == 0 and len(arg_def_string) > 0):
                retString = arg_def_string
                break

        return retString

    def get_confirm(self, arg_string, arg_def_value):
        nRet = arg_def_value
        if (arg_def_value):
            promptString = arg_string + " [Y/n]:"
        else:
            promptString = arg_string + " [y/N]:"

        while (True):
            inputKey = input(promptString + DEF_CONSOLES_SUFFIX)
            if (len(inputKey) == 0):
                return nRet
            elif (inputKey == "Y" or inputKey == "y"):
                return True
            elif (inputKey == "N" or inputKey == "n"):
                return False

    def set_used_symbol(self, arg_symbol):
        self.__used = arg_symbol
