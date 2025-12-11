import contextlib
import datetime
import json
from bisect import bisect_left
from pathlib import Path

import asyncrun as ar
import config
import ldsv as ls
from de import DE, FSe
from sd import FS_Mixin


def findDE(dl, rp: Path):
    tde = DE(rp, FSe(0, 0))
    i = bisect_left(dl, tde)
    if i < len(dl) and tde.nm == dl[i].nm:
        return (dl[i], i)
    return (None, i)


def getOneJSde(rd: Path, fn):
    cmd = 'rclone lsjson "' + str(rd / fn) + '"'
    # cmd += " --stat"
    print(cmd)
    rc, txt = ar.run1(cmd)

    jsl = json.loads(txt) if rc == 0 and txt != "" else []
    return jsl


def getRemoteJSde(rd: Path, fn: str):
    fp = rd / fn
    l1 = getOneJSde(fp.parent, fp.name)
    if len(l1):
        it = l1[0]
        it["Path"] = str(fp.relative_to(rd))
        return [it]
    else:
        return []


def getRemoteDEs(rd: Path, fl: list[str]):
    import concurrent.futures as cf

    tpe = cf.ThreadPoolExecutor(max_workers=4)
    jsl = []

    def f1(fn):
        jsl.extend(getRemoteJSde(rd, fn))

    for fn in fl:
        tpe.submit(f1, fn)
    tpe.shutdown()

    pt = Path
    delst = []
    for it in jsl:
        it1 = pt(it["Path"])
        it2 = it["Size"]
        it3 = it["ModTime"][:-1] + "-00:00"
        it3 = datetime.datetime.fromisoformat(it3).timestamp()
        it3 = config.ts_trunc2ms(it3)
        fse = FSe(it2, it3)
        nde = DE(it1, fse)
        delst.append(nde)
    print(len(delst), "des")
    return delst


def findSis(fp1: Path):
    l1 = {}
    for si, p in config.srcs.items():
        if isinstance(p, FS_Mixin):
            with contextlib.suppress(ValueError):
                l1[si] = fp1.relative_to(p)
    print("l1:", l1)
    return l1


def findDis(fp1: Path):
    l1 = {}
    for di, p in config.tgts.items():
        if isinstance(p, FS_Mixin):
            with contextlib.suppress(ValueError):
                l1[di] = fp1.relative_to(p)
    print("l1:", l1)
    return l1


def findSDEs(fp: Path):
    sil = findSis(fp)
    de_l = []
    for si in sil:
        p = config.src(si)
        rp = sil[si]

        if isinstance(p, FS_Mixin) and p.Dll:
            de, i = findDE(p.Dll, rp)
            de_l.append((p.Dll, rp, de, i, si))
    return de_l


def findTDEs(fp: Path):
    dil = findDis(fp)
    de_l = []
    for di in dil:
        p = config.tgt(di)
        rp = dil[di]

        if isinstance(p, FS_Mixin) and p.Dll:
            de, i = findDE(p.Dll, rp)
            de_l.append((p.Dll, rp, de, i, di))
    return de_l


def updateDEs(rd: Path, flst: list[str]):
    def doSOne(dl, rp, tde, i, si):
        if tde:
            sde = [sde for sde in sdel if sde.nm.name == tde.nm.name]
            sde = sde[0] if len(sde) else None
        else:
            sde = None
        p = config.src(si)
        print("sde", sde, "tde", tde)
        if sde:
            if tde:
                if tde.i.sz != sde.i.sz:
                    print(tde.nm, "mod", "sz")
                    tde.i.sz = sde.i.sz
                    if p.isremote:
                        ls.sev.put("rdlls")
                        config.Dllc[si].set()
                    else:
                        ls.sev.put("ldlls")
                        config.Dllc[si].set()
                    config.upd_cs += 1
                if tde.i.mt != sde.i.mt:
                    print(tde.nm, "mod", "mt")
                    tde.i.mt = sde.i.mt
                    if p.isremote:
                        ls.sev.put("rdlls")
                        config.Dllc[si].set()
                    else:
                        ls.sev.put("ldlls")
                        config.Dllc[si].set()
                    config.upd_cs += 1
            else:
                fse = FSe(sde.i.sz, sde.i.mt)
                tde = DE(rp, fse)
                print(tde.nm, "ins")
                dl.insert(i, tde)
                if p.isremote:
                    ls.sev.put("rdlls")
                    config.Dllc[si].set()
                else:
                    ls.sev.put("ldlls")
                    config.Dllc[si].set()
                config.upd_cs += 1
        else:
            if tde:
                # dl.pop(i)
                pass

    def doTOne(dl, rp, tde, i, di):
        if tde:
            sde = [sde for sde in sdel if sde.nm.name == tde.nm.name]
            sde = sde[0] if len(sde) else None
        else:
            sde = None
        p = config.tgt(di)
        print("sde", sde, "tde", tde)
        if sde:
            if tde:
                if tde.i.sz != sde.i.sz:
                    print(tde.nm, "mod", "sz")
                    tde.i.sz = sde.i.sz
                    if p.isremote:
                        ls.sev.put("rdlls")
                        config.Dllc[di].set()
                    else:
                        ls.sev.put("ldlls")
                        config.Dllc[di].set()
                    config.upd_cs += 1
                if tde.i.mt != sde.i.mt:
                    print(tde.nm, "mod", "mt")
                    tde.i.mt = sde.i.mt
                    if p.isremote:
                        ls.sev.put("rdlls")
                        config.Dllc[di].set()
                    else:
                        ls.sev.put("ldlls")
                        config.Dllc[di].set()
                    config.upd_cs += 1
            else:
                fse = FSe(sde.i.sz, sde.i.mt)
                tde = DE(rp, fse)
                print(tde.nm, "ins")
                dl.insert(i, tde)
                if p.isremote:
                    ls.sev.put("rdlls")
                    config.Dllc[di].set()
                else:
                    ls.sev.put("ldlls")
                    config.Dllc[di].set()
                config.upd_cs += 1
        else:
            if tde:
                # dl.pop(i)
                pass

    sdel = getRemoteDEs(rd, flst)
    with ls.dl:
        for fi in flst:
            fp = rd / fi
            print("fp", fp)
            sdes = findSDEs(fp)
            # print('sdes', sdes)
            tdes = findTDEs(fp)
            # print('tdes', tdes)

            for it in sdes:
                doSOne(*it)
            for it in tdes:
                doTOne(*it)
