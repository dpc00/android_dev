"""
Created on Aug 1, 2016

@author: libraryuser
"""

import threading
import time


class EventEmitter:
    def __init__(self, tname):
        self.events = {}
        self.queue = []
        self.task = threading.Thread(
            target=self.eventLoop, args=(), daemon=True, name=tname
        )
        self.task.start()

    def eventLoop(self):
        while True:
            while len(self.queue) > 0:
                ev = self.queue.pop(0)
                ev[0](*ev[1])
            time.sleep(1)

    def emit(self, ename, *args):
        if ename in self.events:
            f = self.events[ename]
            if f is not None:
                self.queue.append((f, args))

    def on(self, ename, f):
        self.events[ename] = f

    def removeAll(self):
        self.events = {}
