#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Queue
from constant.stock import RetriveType


class BaseStock:
    def __init__(self):
        self.mp = []
        self.status = []
        self.result = Queue()
        self.queue = Queue()

    def get_fetch_count(self):
        return len(self.mp)

    def run(self):
        for mp in self.mp:
            mp.start()

    def retrive_data(self):
        while not self.queue.empty():
            dataItem = self.queue.get()
            if (dataItem[0] == RetriveType.DATA):
                self.result.put(dataItem[1])
            elif (dataItem[0] == RetriveType.INFO):
                for i in range(len(self.status)):
                    if (self.status[i][0] == dataItem[1][0]):
                        self.status[i][1] = dataItem[1][1]

    def is_queue_empty(self):
        return self.queue.empty()

    def get_status(self):
        return self.status

    def get_result(self):
        if (not self.result.empty()):
            return self.result.get()
        return None

    def is_alive(self):
        while any(i.is_alive() for i in self.mp):
            return True

        return False
