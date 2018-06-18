#!/usr/bin/env python3
# -*- coding:utf-8 -*-

DICT_TEXT_STYLE = {
    "RESET": "\33[0m",
    "BOLD": "\33[1m",
    "RED": "\33[31m",
    "CLEAR_SCREEN": "\033[2J\033[H",
    "CURSOR_UP": "\033[%sA"
}

from colorama import init, Fore, Back, Style, Cursor
init()


def string(arg_string):
    print(arg_string)


def bold_string(arg_string):
    # print(DICT_TEXT_STYLE['BOLD'] + arg_string + DICT_TEXT_STYLE['RESET'])
    print(Style.BRIGHT + arg_string + Style.NORMAL)


def warning_string(arg_string):
    #print(DICT_TEXT_STYLE['RED'] + arg_string + DICT_TEXT_STYLE['RESET'])
    print(Fore.RED + arg_string + Fore.RESET)


def empty_string():
    print("")


def move_cursor_up(arg_line=1):
    #print(DICT_TEXT_STYLE['CURSOR_UP'] % (argLine), end='', flush=True)
    print(Cursor.UP(arg_line), end='', flush=True)
