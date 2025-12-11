import contextlib
import os
import time

import utils
from ChangeNotification import dmonitor
from Dir import fromPath
from DirSync import DirSync
from Drive import getDrives

sda = None

# utils.log(hashlib.algorithms_available)

dsn1 = "667AB765"  # CODE0 (NOT UP TO DATE)
dsn2 = "34625CA3"  # CODE1 (NOT VALID)


def proc1(*args):
    global sda
    sda = utils.establish()
    getDrives(True)

    rp = r""
    dir1 = fromPath(sda[0] + rp)
    dir2 = fromPath(sda[1] + rp)
    if dir2 is None:
        mode = int("0777")
        os.makedirs(sda[1] + rp, mode, True)
        dir2 = fromPath(sda[1] + rp)
        if dir2 is None:  # failure to instantiate target dir
            return

    ds = DirSync("CODE0-CODEn", dir1, dir2, clearstats=False)
    # dmonitor(ds.srt)
    # dmonitor(ds.drt)
    ec = 0
    while True:
        ec += 1
        utils.log("=" * 100)
        utils.log("pass " + str(ec))
        utils.log("=" * 100)
        ds.run(True)
        time.sleep(1.0)
        if ec >= 3:
            break
        ds.markStale(ds.srt)
        ds.markStale(ds.drt)


def proc2(*args):
    global sda
    sda = utils.establish()
    getDrives(True)

    rp = r""
    dir1 = fromPath(sda[0] + r"\PortableApps\EclipsePortable\App\eclipse")
    dir2 = fromPath(utils.expES(r"%APPDATA%\Eclipse"))
    if dir2 is None:
        mode = int("0777")
        os.makedirs(sda[1] + rp, mode, True)
        dir2 = fromPath(sda[1] + rp)
        if dir2 is None:
            return

    ds = DirSync("Install-Eclipse", dir1, dir2, clearstats=False)
    dmonitor(ds.srt)
    # dmonitor(ds.drt)
    ec = 0
    while True:
        ec += 1
        utils.log("=" * 100)
        utils.log("pass " + str(ec))
        utils.log("=" * 100)
        ds.run(True)
        time.sleep(1.0)
        if (
            ds.srt.digest.fh == ds.drt.digest.fh
            and ds.srt.digest.dh == ds.drt.digest.dh
        ):
            break
        if ec > 2:
            break


def proc3(*args):
    global sda
    sda = utils.establish()
    getDrives(True)

    rp = r""
    dir2 = fromPath(sda[0] + r"\PortableApps\EclipsePortable\App\eclipse")
    dir1 = fromPath(utils.expES(r"%APPDATA%\Eclipse"))
    if dir2 is None:
        mode = int("0777")
        os.makedirs(sda[1] + rp, mode, True)
        dir2 = fromPath(sda[1] + rp)
        if dir2 is None:
            return

    ds = DirSync("Save-Eclipse", dir1, dir2, clearstats=False)
    dmonitor(ds.srt)
    # dmonitor(ds.drt)
    ec = 0
    while True:
        ec += 1
        utils.log("=" * 100)
        utils.log("pass " + str(ec))
        utils.log("=" * 100)
        ds.run(True)
        time.sleep(20.0)
        if (
            ds.srt.digest.fh == ds.drt.digest.fh
            and ds.srt.digest.dh == ds.drt.digest.dh
        ):
            break
        if ec > 256:
            break


def proc4(*args):
    global sda
    sda = utils.establish()
    getDrives(True)

    rp = r""
    dir1 = fromPath(utils.expES(r"%USERPROFILE%\scala"))
    dir2 = fromPath(sda[0] + r"\Projects\lib\scala")
    if dir2 is None:
        mode = int("0777")
        os.makedirs(sda[1] + rp, mode, True)
        dir2 = fromPath(sda[1] + rp)
        if dir2 is None:
            return

    ds = DirSync("Copy-Scala", dir1, dir2, clearstats=False)
    dmonitor(ds.srt)
    # dmonitor(ds.drt)
    ec = 0
    while True:
        ec += 1
        utils.log("=" * 100)
        utils.log("pass " + str(ec))
        utils.log("=" * 100)
        ds.run(True)
        time.sleep(1.0)
        if (
            ds.srt.digest.fh == ds.drt.digest.fh
            and ds.srt.digest.dh == ds.drt.digest.dh
        ):
            break
        if ec > 2:
            break


@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print("Total elapsed time for {}: {:3.3f}".format(message, t1 - t0))


proggies = {
    "eclipse-install": proc2,
    "eclipse-backup": proc3,
    "flash-backup": proc1,
    "copy-scala": proc4,
}

# saveDrives()
if __name__ == "__main__":
    proggie = "flash-backup"
    with stopwatch("proc " + proggie + " with file/dir change notifications"):
        proggies[proggie]()
    utils.log("quit")
