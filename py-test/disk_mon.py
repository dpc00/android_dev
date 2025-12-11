import functools
import os
import threading
import time
from collections import OrderedDict

import Dir
import DirSync
import Drive
import fcstats
import utils
from winwatcher.watcher import DirWatcher

interval_quit = False
copying = False
pd = utils.expES("%FLASH0%\\")
rdy = False
rfc3 = True
statsinited = False
watchers = []
threads = []
opq = []

OP_DIRDEL = 1
OP_DIRMOV = 2
OP_FILEMOV = 3
OP_DIRSYNC = 4
OP_DIRMIRROR = 5

ignored = {"clog_flash_CODE0.json", ".lock"}

wdirs = [pd + ""]


def setTimeout(f, n, t):
    t = threading.Timer(t / 1000.0, f)
    t.setDaemon(True)
    t.name = n
    t.start()


def setInterval(f, n, t):
    def f2():
        if not interval_quit:
            f()
            setTimeout(f2, n, t)

    setTimeout(f2, n, t)


@functools.total_ordering
class DSEvent:
    __slots__ = ["op", "_hash", "rp1", "rp2"]

    def __init__(self, op, ds, rp1, rp2=None):
        self.op = op
        self._hash = ds
        self.rp1 = rp1
        self.rp2 = rp2

    def __lt__(self, other):
        rv = self.op < other.op
        if not rv:
            rv = self._hash.srt < other._hash.srt
        if not rv:
            rv = self._hash.drt < other._hash.drt
        if not rv:
            rv = self.rp1 < other.rp1
        if not rv:
            rv = self.rp2 < other.rp1
        return rv

    def __eq__(self, other):
        rv = self.op == other.op
        if rv:
            rv = self._hash.srt == other._hash.srt
        if rv:
            rv = self._hash.drt == other._hash.drt
        if rv:
            rv = self.rp1 == other.rp1
        if rv:
            rv = self.rp2 == other.rp1
        return rv

    def __str__(self):
        opcodes = {
            1: "OP_DIRDEL",
            2: "OP_DIRMOV",
            3: "OP_FILEMOV",
            4: "OP_DIRSYNC",
            5: "OP_DIRMIRROR",
        }
        try:
            ps = opcodes[self.op]
            ps += " " + str(self._hash)
            ps += " " + self.rp1
            ps += " " + self.rp2
        except Exception as e:
            utils.errlog(e)
        return ps

    def digest(self):
        hc = 0
        try:
            hc ^= hash(self.op)
            hc ^= hash(self._hash)
            hc ^= hash(self.rp1)
            hc ^= hash(self.rp2)
        except AttributeError as e:
            utils.errlog(e)
        return hc


def cf1(ds, p1, p2):
    opq.append(DSEvent(OP_DIRMIRROR, ds, p1))
    p1 = os.path.dirname(p1)
    opq.append(DSEvent(OP_DIRSYNC, ds, p1))
    pass


def cf2(ds, p1, p2):
    opq.append(DSEvent(OP_DIRMIRROR, ds, p1, p2))
    pass


def cf3(ds, p1, p2):  # SHOULD BE OP_DIRMOVE
    opq.append(DSEvent(OP_DIRMOV, ds, p1, p2))
    p1 = os.path.dirname(p1)
    opq.append(DSEvent(OP_DIRSYNC, ds, p1))
    p2 = os.path.dirname(p2)
    opq.append(DSEvent(OP_DIRSYNC, ds, p2))
    pass


def cf4(ds, p1, p2):
    opq.append(DSEvent(OP_DIRDEL, ds, p1))
    p1 = os.path.dirname(p1)
    opq.append(DSEvent(OP_DIRSYNC, ds, p1))
    pass


def cf5(ds, p1, p2):
    p1 = os.path.dirname(p1)
    opq.append(DSEvent(OP_DIRSYNC, ds, p1))
    pass


def cf6(ds, p1, p2):
    p1 = os.path.dirname(p1)
    opq.append(DSEvent(OP_DIRSYNC, ds, p1))
    pass


def cf7(ds, p1, p2):  # should be OP_FILEMOVE
    opq.append(DSEvent(OP_FILEMOV, ds, p1, p2))
    pass


def cf8(ds, p1, p2):
    p1 = os.path.dirname(p1)
    opq.append(DSEvent(OP_DIRSYNC, ds, p1))
    pass


ftbl = {
    "DirectoryAdded": cf1,
    "DirectoryModified": cf2,
    "DirectoryMoved": cf3,
    "DirectoryRemoved": cf4,
    "FileAdded": cf5,
    "FileModified": cf6,
    "FileMoved": cf7,
    "FileRemoved": cf8,
}


def process_event(ev, ds):
    if len(ev) == 3:
        ftbl[ev[0]](ds, ev[1], ev[2])
    else:
        ftbl[ev[0]](ds, ev[1], None)


def do_watch(watcher, ds):
    global interval_quit
    while not interval_quit:
        ev = watcher.observe()
        if not ev[0] in ftbl:
            continue
        process_event(ev, ds)


def initStats():
    global statsinited
    if not statsinited:
        setInterval(fcstats.oprint, "fcstats.oprint", 1000)
        fcstats.clr()
        # Dir.addListeners()
        statsinited = True


def cleanseQ(k1, v1):
    ndel = 0
    for i in range(len(opq) - 1, -1, -1):
        (k2, v2) = opq[i]
        if k2 == k1 and v2 == v1:
            opq.pop(i)
            ndel += 1
    if ndel > 0:
        utils.log("ndel: " + ndel)


ds = None


def f0():
    global opq, copying, ds

    if copying:
        return
    copying = True
    opqc = OrderedDict()
    while len(opq) > 0:
        qv = opq.pop(0)
        if qv not in opqc:
            opqc[qv] = 1
        else:
            opqc[qv] += 1
    if len(opqc):
        for k, v in opqc.items():
            utils.log(str(k) + ":" + str(v))
    while len(opqc) > 0:
        dse = opqc.popitem(last=False)
        if r"\Temp" in dse._hash.path or r"\.sync" in dse._hash.path:
            continue
        if dse.op == OP_DIRDEL:
            try:
                v1 = dse._hash.srt
                v2 = dse.rp1
                v3 = Dir.fromRelPath(v1, v2)
                v4 = v3.path
                v5 = ds.dstDir(v4)
                v5.delete()
                v5.pd.refreshContents()
                v5.pd.refreshStats()
            except OSError:
                pass
        elif dse.op == OP_DIRMOV or dse.op == OP_FILEMOV:
            try:
                v1 = dse._hash
                v2 = dse.rp1
                v3 = dse.rp2
                v4 = Dir.fromRelPath(v1, v2)
                v5 = v4.pd.path
                v6 = dse._hash
                v7 = dse.rp2
                v8 = Dir.fromRelPath(v6, v7)
                v9 = v8.pd.path
                os.rename(v5, v9)
                v4.pd.refreshContents()
                v4.pd.refreshStats()
                v8.pd.refreshContents()
                v8.pd.refreshStats()
            except OSError:
                pass
        elif dse.op == OP_DIRSYNC:
            try:
                dse._hash.syncDir(dse.rp1, includesubdirs=False)
            except OSError:
                pass
        elif k == OP_DIRMIRROR:
            try:
                dse._hash.syncDir(dse.rp1, includesubdirs=True)
            except OSError:
                pass
    # Drive.saveDrives()
    copying = False


def process_event2(evn, ds, fn1, fn2=None):
    if fn2:
        ftbl[evn](ds, fn1, fn2)
    else:
        ftbl[evn](ds, fn1, None)


def startup():
    global ds
    Drive.getDrives(True)
    sda = utils.establish()
    d1 = Dir.fromPath(sda[0])
    d2 = Dir.fromPath(sda[1])
    initStats()
    for dp1 in wdirs:
        dp2 = os.path.abspath(dp1)
        dp2 = os.path.relpath(dp2, d1.path)
        if dp2 == ".":
            dp2 = ""
        wd1 = Dir.fromRelPath(d1, dp2)
        wd2 = Dir.fromRelPath(d2, dp2)
        try:
            # opq.append((OP_DIRMIRROR, dp2))
            dsn = "CODE0_CODEn\\" + dp2
            cds = DirSync.DirSync(dsn, wd1, wd2, clearstats=False)
            # dirsyncs[dsn] = cds
            w1 = DirWatcher(wd1.path, recursive=True)
            watchers.append(w1)
            w1.start_watching()
            t1 = threading.Thread(
                target=do_watch, args=(w1, cds), daemon=True, name="DW_" + dp2
            )
            threads.append(t1)
            t1.start()
        except Exception as e:
            utils.errlog(e)
    setInterval(f0, "f0", 12000)
    utils.log("generating sync events")
    dsn = "CODE0->CODEn"
    ds = DirSync.DirSync(dsn, d1, d2, clearstats=False)
    ds.syncFromDigests("", includesubdirs=True)
    utils.log("done generating sync events")
    pass


def run():
    startup()
    tbs = 60
    while True:
        time.sleep(tbs)
        # Drive.saveDrives()


def background():
    from threading import Thread

    t = Thread(target=run, name="disk_mon", daemon=True)
    t.start()


if __name__ == "__main__":
    run()
