#!/usr/bin/env python3
# -*- coding:utf-8 -*-

DICT_TEXT_STYLE = {
    "RESET": "\33[0m",
    "BOLD": "\33[1m",
    "RED": "\33[31m",
    "CLEAR_SCREEN": "\033[2J\033[H",
    "CURSOR_UP": "\033[%sA"
}


def string(arg_string):
    print(arg_string)


def bold_string(arg_string):
    print(DICT_TEXT_STYLE['BOLD'] + arg_string + DICT_TEXT_STYLE['RESET'])


def warning_string(arg_string):
    print(DICT_TEXT_STYLE['RED'] + arg_string + DICT_TEXT_STYLE['RESET'])


def empty_string():
    print("")


def clear_screen():
    print(DICT_TEXT_STYLE['CLEAR_SCREEN'], end='', flush=True)


def move_cursor_up(argLine=1):
    print(DICT_TEXT_STYLE['CURSOR_UP'] % (argLine), end='', flush=True)
