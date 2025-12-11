from bkenv import *
from inotify_simple import *
from status import *
from netup import *
from opts import *
from time import sleep
import os
from os import path
from pathlib import Path
import asyncio
from asyncio import sleep

wdsi = {}


async def wsetup(in1):
    for si in srcs:
        try:
            rv = in1.add_watch(str(pdir[si]), flags.MODIFY)
            # await asyncio.sleep(0)
            wdsi[rv] = (si, pdir[si])
            if not pdir[si].is_file():
                for pth, dirs, files in os.walk(pdir[si], topdown=True):
                    if ".git" in pth:
                        break
                    if ".git" in dirs:
                        dirs.remove(".git")
                    if "__pycache__" in dirs:
                        dirs.remove("__pycache__")
                    for dir in dirs:
                        cp = path.join(pth, dir)
                        rv = in1.add_watch(cp, flags.MODIFY)
                        wdsi[rv] = (si, cp)
                        # await asyncio.sleep(0)
        except:
            pass
    print(len(wdsi), "watches")


async def updts():
    try:
        updatets(0)
    except Exception as e:
        print(e)


sis = set()


async def rt1():
    global cel, in1, sis

    def cb1():
        evs = in1.read(100, 100)
        for ev in evs:
            print(ev)
            cwd = ev.wd
            si = wdsi[cwd][0]
            sis.add(si)
        for si in sis.copy():
            cel.run_in_executor(None, onestatus(si))
            sis.remove(si)

    cel.add_reader(in1.fd, cb1)


ct1 = None


async def rt2():
    global cel
    cl = await cel.run_in_executor(None, clean)
    if cl:
        print("backups appear done")
    else:
        print("backups appear pending")
        rv1 = await opexec()
        print("rv1", rv1)
    await sleep(20)
    cel.create_task(rt2())


def main():
    global cel, wdsi, in1
    print("-main")
    with INotify() as in1:
        cel = asyncio.get_event_loop()
        print(cel)
        cel.create_task(wsetup(in1))
        cel.create_task(updts())
        cel.create_task(rt1())
        cel.create_task(rt2())
        cel.run_forever()


if __name__ == "__main__":
    main()
