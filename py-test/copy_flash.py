"""
Created on Jul 11, 2016

@author: Phil
"""

import datetime
import math
import os
import random
import threading

from EventEmitter import EventEmitter
import dirutils
import fcstats
import json2
import utils


clog = {}
cfn = utils.prjDir("py-test") + "\\clog_flash_CODE0.json"

interval_quit = False


def getClog():
    global clog
    clog = json2.readConfig(cfn)


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


def writeClog():
    try:
        json2.writeConfig(clog, cfn)
    except Exception as e:
        utils.errlog(e)


def addListeners():
    ee = dirutils.dmEE1

    def run(p1, p2):
        utils.log(utils.chop("ds: " + p1 + " done."))

    ee.on("dcopy", run)

    def f2(p2):
        v = p2.replace(os.environ["CLONE_DIR"], "%FLASH0%")
        if v in clog:
            del clog[v]
        v = os.path.dirname(v)
        if v.endswith("%FLASH0%"):
            v += "\\"
        if v not in clog:
            clog[v] = 0
        clog[v] += 1

    # ee.on('ddel', f2)
    def f3(p1):
        utils.log("dir skipped: " + p1)

    ee.on("dskipped", f3)

    def f4(err):
        utils.log(str(err))

    ee.on("error", f4)

    def f5(p1, p2):
        v = p1.replace(os.environ["FLASH0"], "%FLASH0%")
        v = os.path.dirname(v)
        if v.endswith("%FLASH0%"):
            v += "\\"
        if v not in clog:
            clog[v] = 0
        clog[v] += 1

    # ee.on('fcopy', f5)
    def f6(p2):
        v = p2.replace(os.environ["CLONE_DIR"], "%FLASH0%")
        v = os.path.dirname(v)
        if v.endswith("%FLASH0%"):
            v += "\\"
        if v not in clog:
            clog[v] = 0
        clog[v] += 1

    # ee.on('fdel', f6)


def removeDMListeners():
    ee = dirutils.dmEE1
    ee.removeAll()


def dirCopy(d1, d2):
    getClog()
    fcstats.clr()
    addListeners()
    dirutils.dirCopy(d1, d2, [])
    removeDMListeners()
    fcstats.oprint()
    json2.writeConfig(clog, cfn)


def flashSync1(d1, d2, exc_dirs):
    global interval_quit
    interval_quit = False
    dirutils.dm_excl = {}
    getClog()
    setInterval(writeClog, 60000)
    setInterval(fcstats.oprint, 1000)
    fcstats.clr()
    addListeners()
    dirutils.dirMirror(d1, d2, exc_dirs)
    removeDMListeners()
    interval_quit = True
    writeClog()


def flashSync2(d1, d2, exc_dirs):
    global interval_quit
    interval_quit = False
    dirutils.dm_excl = {}
    getClog()
    setInterval(writeClog, 60000)
    setInterval(fcstats.oprint, 1000)
    fcstats.clr()
    addListeners()

    tclog = clog.copy()

    for k in tclog:

        def f(kt):
            cp = utils.expES(kt)
            sfp = cp
            dfp = dirutils.dPath(d1, d2, sfp)
            dirutils.dirSync(sfp, dfp, None, exc_dirs)

        f(k)
    removeDMListeners()
    interval_quit = True
    writeClog()


exc_dirs = [
    utils.expES("%FLASH0%\\Programs\\GoogleChromePortable"),
    utils.expES("%FLASH0%\\GitRepos"),
]


def fcopy1():
    sda = utils.establish()
    src = sda[0]
    sda = sda[1:]
    for dest in sda:
        flashSync1(src, dest, exc_dirs)


def fcopy2():
    sda = utils.establish()
    src = sda[0]
    sda = sda[1:]
    for dest in sda:
        flashSync2(src, dest, exc_dirs)


def fcopy3():
    sda = utils.establish()
    src = sda[0]
    sda = sda.slice(1)
    if src.endswith("\\"):
        src = src[:-1]
    for dest in sda:
        if dest.endswith("\\"):
            dest = dest[:-1]
        src2 = src + "\\Programs\\GoogleChromePortable"
        dest2 = dest + "\\Programs\\GoogleChromePortable"
        flashSync1(src2, dest2, exc_dirs)


# if __name__ == "__main__":
#    fcopy1()
