import asyncio
from pathlib import Path
from bisect import insort
import json
import time
from math import floor
from os import makedirs, utime

import asyncrun as ar
from opbase import OpBase
from netup import netup


async def fsync(sd, td, tcfc):
    if await netup():
        # print('fsync', sd, td)
        if not td.exists():
            makedirs(td, exist_ok=True)
        cmd = 'rclone sync "' + str(sd) + '" "' + str(td) + '" --progress'
        # cmd += ' --exclude ".git/**" --exclude "__pycache__/**"'
        print(cmd)
        rc = await ar.run2(cmd)
        if rc == 0:
            tcfc[0] += 1
            return True
        else:
            tcfc[1] += 1
    return False


class BVar:
    def __init__(self, di, si, tcfc):
        from config import pdir, tdir

        self.si = si
        self.di = di
        self.sd = pdir(si)
        self.td = tdir(di)
        self.dln = None
        self.dhn = None
        self.dlo = None
        self.dho = None
        self.f2d = None
        self.f2c = None
        self.tcfc = tcfc
        self.ac1 = 0

    async def init2(self):
        from statushash import ldh_d, rdh_d, saverdh
        from dirlist import rdlld, dllcmp, ldlld

        self.dhn = await ldh_d(self.si)
        if self.dhn is None:
            return 1
        self.dho = await rdh_d(self.di)
        if self.dho is None:
            return 1
        if self.dho == self.dhn:
            return 2
        self.dln = await ldlld(self.si)
        if self.dln is None:
            return 3
        self.dlo = await rdlld(self.di)
        if self.dlo is None:
            return 3
        self.f2d, self.f2c = dllcmp(self.dlo, self.dln)
        return 4


class CSRestore(OpBase):
    async def __call__(self):
        from edge import Edge, findEdge
        from config import pdir, tdir
        from statushash import ldh_d, rdh_d, rdh_f, saverdh, ldhset
        from dirlist import ldlld, rdlld, dllcmp, ldlls, ldlls_dirty, rdlls_dirty

        global ldlls_dirty, rdlls_dirty
        tcfc = [0, 0]
        print("CSRestore")
        if not await netup():
            return (tcfc[0], tcfc[1])
        di, si = self.npl1
        e = findEdge(di, si)
        if e.rbctck():
            print("r", di, si)
            bv = BVar(di, si, tcfc)
            rv = await bv.init2()
            # sd = pdir(si)
            if rv == 1:  # couldn't get remote hash
                pass
            else:
                if rv == 2:  # hashes match
                    e.rclr()
                else:
                    print("hash mismatch")
                    print(bv.si, bv.dho, bv.dhn)
                    if rv == 3:  # dlo not obtainable
                        pass
                    else:
                        if len(bv.f2d):
                            print(len(bv.f2d), "todelete")
                            for it in bv.f2d:
                                print("\t", it.nm)
                        if len(bv.f2c):
                            print(len(bv.f2c), "tocopy")
                            for it in bv.f2c:
                                print("\t", it.nm)

                        for rf in bv.f2d.copy():
                            found = False
                            for lf in bv.f2c.copy():
                                # TODO: use Path
                                if rf.nm == lf.nm:  # names match
                                    found = True
                                    if rf.md5 == lf.md5:  # hashes match
                                        if rf.mt < lf.mt:
                                            print(
                                                "hashes match but it has older file time!"
                                            )
                                            print(
                                                "retrograding local copy",
                                                rf.nm,
                                                rf.mt,
                                                lf.mt,
                                            )
                                            nt = int(rf.mt * 1000) * 1000000
                                            utime(bv.sd / lf.nm, ns=(nt, nt))
                                            bv.ac1 += 1
                                            tcfc[0] += 1
                                        elif abs(rf.mt - lf.mt) <= 0.00101:
                                            print(
                                                "hashes match but remote has newer file time",
                                                lf.nm,
                                                rf.mt,
                                                lf.mt,
                                            )
                                            print("time diff is only", rf.mt - lf.mt)
                                            print(
                                                "retrograding local copy",
                                                lf.nm,
                                                rf.mt,
                                                lf.mt,
                                            )
                                            nt = int(rf.mt * 1000) * 1000000
                                            utime(bv.sd / lf.nm, ns=(nt, nt))
                                            bv.ac1 += 1
                                            tcfc[0] += 1
                                        bv.f2d.remove(rf)
                                        bv.f2c.remove(lf)
                                    else:
                                        if rf.mt > lf.mt:
                                            if await fsync(
                                                bv.td / rf.nm,
                                                bv.sd / lf.nm.parent,
                                                tcfc,
                                            ):
                                                bv.f2d.remove(rf)
                                                bv.f2c.remove(lf)
                                                bv.ac1 += 1
                            if not found:
                                if await fsync(
                                    bv.td / rf.nm, bv.sd / rf.nm.parent, tcfc
                                ):
                                    bv.f2d.remove(rf)
                                    bv.ac1 += 1
            if bv.ac1:
                del ldlls[si]
                ldlls_dirty = True
            if tcfc[1] == 0:
                e.rclr()
        return (tcfc[0], tcfc[1])


if __name__ == "__main__":
    from os import environ
    import time
    from config import opdep

    t1 = time.time()
    environ["TSREST"] = "True"
    from config import *

    if asyncio.run(netup()):
        for op in opdep:
            if isinstance(op, CSRestore):
                asyncio.run(op())
    t2 = time.time()
    print(t2 - t1)
