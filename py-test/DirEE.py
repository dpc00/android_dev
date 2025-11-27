'''
Created on Sep 25, 2016

@author: libraryuser
'''

import os
import threading

from EventEmitter import EventEmitter
import utils


clog = {}
# dirEE = EventEmitter('dirEE')
interval_quit = False

def setTimeout(f, t):
    t = threading.Timer(t / 1000.0, f)
    t.setDaemon(True)
    t.start()

def setInterval(f, t):
    def f2():
        if not interval_quit:
            f()
            setTimeout(f2, t)
    setTimeout(f2, t)

def addListeners():
    # ee = dirEE
    def f0(p1, p2):
        # utils.log(utils.chop('dsync: ' + p1 + '->' + p2))
        pass
    ee.on('dsync', f0)
    def run(p1, p2):
        pass
    ee.on('dcopy', run)
    def f2(p2):
        v = p2.replace(os.environ['CLONE_DIR'], "%FLASH0%")
        if v in clog:
            del clog[v]
        v = os.path.dirname(v)
        if v.endswith('%FLASH0%'):
            v += '\\'
        if v not in clog:
            clog[v] = 0
        clog[v] += 1
    ee.on('ddel', f2)
    def f3(p1):
        utils.log('dir skipped: ' + p1)
    ee.on('dskipped', f3)
    def f4(err):
        utils.log(str(err))
    ee.on('error', f4)
    def f5(p1, p2):
        v = p1.replace(os.environ['FLASH0'], "%FLASH0%")
        v = os.path.dirname(v)
        if v.endswith('%FLASH0%'):
            v += '\\'
        if v not in clog:
            clog[v] = 0
        clog[v] += 1
    ee.on('fcopy', f5)
    def f6(p2):
        v = p2.replace(os.environ['CLONE_DIR'], "%FLASH0%")
        v = os.path.dirname(v)
        if v.endswith('%FLASH0%'):
            v += '\\'
        if v not in clog:
            clog[v] = 0
        clog[v] += 1
    ee.on('fdel', f6)
    def f7(p1):
        pass
    ee.on('dscn', f7)

def removeDMListeners():
    # ee = dirEE
    # ee.removeAll()

