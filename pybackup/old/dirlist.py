import datetime
import json
import time
from bisect import bisect_left
from fnmatch import fnmatch
from os import walk
from pathlib import Path

import asyncrun as ar
import config
from de import DE, FSe

rto1 = 60 * 0
rto2 = 60 * 0


def getfl(p):
    pt = type(p)
    # print(str(p))
    fl = []
    try:
        if p.is_file():
            fl.append(p)
            return fl
        for pth, dirs, files in walk(p, topdown=True):
            pth = pt(pth)
            if not v.isbaddir(pth):
                v.cull_dirs(dirs, pt)
                for f in files:
                    fl.append(pth / f)
            else:
                dirs.clear()
                files.clear()
        return fl
    except IOError as e:
        print(e)
        return fl


def getdll0():  # remote-entire-drive
    v.dl0_cs += 1
    td = v.ppre("gd")
    # print('getdll0',td)
    cmd = 'rclone lsjson "' + str(td) + '" --recursive --files-only '
    for ex in v.dexs:
        cmd += ' --exclude "**/' + ex + '/*" '
    rc = ar.run1(cmd)
    if rc == 0:
        l1 = json.loads(ar.txt)

        def es(it: dict):
            it1 = Path(it["Path"])
            it2 = it["Size"]
            it3 = it["ModTime"][:-1] + "-00:00"
            it3 = datetime.datetime.fromisoformat(it3).timestamp()
            it3 = v.ts_trunc2ms(it3)
            fse = FSe(it2, it3)
            return DE(it1, fse)

        st = list(map(es, l1))
        st.sort(key=lambda de: de.nm)
        print(len(st), "de's")
        return st
    return None


def sepdlls(dlls):
    print("-sepdlls")
    for di in v.tgts:
        bd = v.tgt(di)
        if bd.isremote:
            v.RDlls[di] = []
            v.RDlls_xt[di] = time.time()
            v.RDlls_changed = True
            rd = bd.relative_to(v.ppre("gd"))
            tds = str(rd) + "/"
            i = bisect_left(dlls, tds, key=lambda de: de.nm)
            # print(tds, i)
            if i == len(dlls):
                continue
            de = dlls[i]
            if not fnmatch(de.nm, tds + "*"):
                print("error")
                print(rd, tds, i, de.nm)
                # TODO: apply panic procedure
                continue
            while fnmatch(de.nm, tds + "*"):
                v.ppre("gd") / de.nm
                fse = FSe(de.i.sz, de.i.mt)
                de2 = DE(de.nm, fse)
                # TODO: use Path
                de2.nm = de2.nm.relative_to(rd)
                v.TDlls[di].append(de2)
                i += 1
                if i == len(dlls):
                    break
                de = dlls[i]
    print(len(v.TDlls), "rdlls")


def getdll1(di):  # remote-target
    v.dl1_cs += 1
    td = v.tgt(di)
    # print('getdll1', di, str(td))
    cmd = 'rclone lsjson "' + str(td) + '" --recursive --files-only --fast-list '
    for ex in v.dexs:
        cmd += ' --exclude "**/' + ex + '/*" '
    # print(cmd)
    rc = ar.run1(cmd)
    if rc == 0:
        l1 = json.loads(ar.txt)
        if l1 is None:
            l1 = []

        def es(it: dict):
            # TODO: use Path
            it1 = Path(it["Path"])
            it2 = it["Size"]
            it3 = it["ModTime"][:-1] + "-00:00"
            it3 = datetime.datetime.fromisoformat(it3).timestamp()
            it3 = v.ts_trunc2ms(it3)
            fse = FSe(it2, it3)
            return DE(it1, fse)

        st = list(map(es, l1))
        st.sort(key=lambda de: de.nm)
        return st
    if rc == 3:
        return []
    return None


def getdll5(si):  # remote-source
    v.dl5_cs += 1
    td = v.src(si)
    # print('getdll1', di, str(td))
    cmd = 'rclone lsjson "' + str(td) + '" --recursive --files-only --fast-list '
    for ex in v.dexs:
        cmd += ' --exclude "**/' + ex + '/*" '
    # print(cmd)
    rc = ar.run1(cmd)
    if rc == 0:
        l1 = json.loads(ar.txt)
        if l1 is None:
            l1 = []

        def es(it: dict):
            # TODO: use Path
            it1 = Path(it["Path"])
            it2 = it["Size"]
            it3 = it["ModTime"][:-1] + "-00:00"
            it3 = datetime.datetime.fromisoformat(it3).timestamp()
            it3 = v.ts_trunc2ms(it3)
            fse = FSe(it2, it3)
            return DE(it1, fse)

        st = list(map(es, l1))
        st.sort(key=lambda de: de.nm)
        return st
    if rc == 3:
        return []
    return None


def getdll2(si):  # remote-source
    v.dl2_cs += 1
    td = v.src(si)
    # print('getdll2', si, str(td))
    cmd = 'rclone lsjson "' + str(td) + '" --recursive --files-only --fast-list '
    if not td.is_file():
        for ex in v.dexs:
            cmd += ' --exclude "**/' + ex + '/*" '
    # print(cmd)
    rc = ar.run1(cmd)
    if rc == 0:
        l1 = json.loads(ar.txt)

        def es(it: dict):
            # TODO: use Path
            it1 = Path(it["Path"])
            it2 = it["Size"]
            it3 = it["ModTime"][:-7] + "-00:00"
            it3 = datetime.datetime.fromisoformat(it3).timestamp()
            it3 = v.ts_trunc2ms(it3)
            fse = FSe(it2, it3)
            return DE(it1, fse)

        st = list(map(es, l1))
        st.sort(key=lambda de: de.nm)
        return st
    if rc == 3:
        return []
    return None


def getrdlls():  # remote entire drive
    t1 = time.time()
    rv = getdll0()
    if rv is not None:
        t2 = time.time()
        sepdlls(rv)
        t3 = time.time()
        print(round(t2 - t1, 3), round(t3 - t2, 3))
