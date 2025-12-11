#!/data/data/com.termux/files/usr/bin/env python

import asyncio
from os import walk
from pathlib import Path

from config import srcs, src
from dirlist import ldlls, saveldlls, saverdlls, getrdlls
from fmd5h import savefmd5h

# from inotify_simple import INotify, HOME
from opexec import clean, opexec
from status import updatets, onestatus, rupdatets

global cel

wdsi = {}
in1 = None


async def wsetup():
    global in1
    for si in srcs:
        try:
            p = src(si)
            rv = in1.add_watch(str(p), flags.MODIFY)
            # await asyncio.sleep(0)
            wdsi[rv] = (si, p)
            if not p.is_file():
                for pth, dirs, files in walk(p, topdown=True):
                    if ".git" in pth:
                        dirs = []
                        break
                    if ".git" in dirs:
                        dirs.remove(".git")
                    if "__pycache__" in dirs:
                        dirs.remove("__pycache__")
                    for d in dirs:
                        cp = Path(pth, d)
                        rv = in1.add_watch(str(cp), flags.MODIFY)
                        wdsi[rv] = (si, cp)
                        # await asyncio.sleep(0)
        except Exception as e:
            pass
            # print(e)
    # for k,v in wdsi.items():
    # print(v[0],str(v[1]))
    print(len(wdsi), "watches")


tr = 0


async def cb1():
    global tr
    sis = set()
    evs = await in1.read(1000, 1000)
    for ev in evs:
        # print(ev)
        si = wdsi[ev.wd][0]
        if si != "git":
            if si not in sis:
                sis.add(si)
                if si in ldlls:
                    del ldlls[si]
                print("cb1 onestatus", si)
                await onestatus(si)
    tr -= 1


def cb2():
    global tr
    if not tr:
        tr += 1
        cel.create_task(cb1())


ct1 = None


async def rt2():
    itc = 0
    while True:
        itc += 1
        cl = await clean()
        if cl:
            print("backups appear done")
        else:
            print("backups appear pending")
            rv1 = await opexec()
            print("rv1", rv1)
        savefmd5h()
        saveldlls()
        saverdlls()
        break
        await asyncio.sleep(12)


def main():
    global wdsi, in1, cel, ldlls_dirty, rdlls_dirty, hf_dirty
    print("-main")
    ldlls_dirty = True
    rdlls_dirty = True
    hf_dirty = True
    # with INotify() as in1:
    cel = asyncio.get_event_loop()
    # cel.add_reader(in1.fd, cb2)
    # cel.run_until_complete(wsetup())
    cel.run_until_complete(getrdlls())
    cel.run_until_complete(updatets(0))
    cel.run_until_complete(rupdatets(0))
    cel.run_until_complete(rt2())


if __name__ == "__main__":
    main()
