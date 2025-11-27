import asyncio
from pathlib import Path
from bisect import insort
import json
import datetime
import time

import asyncrun as ar
from opbase import OpBase
from netup import netup


async def fsync(sd, td, tcfc):
    if (await netup()):
        # print('fsync', sd, td)
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


async def fcopy(sd, td, tcfc):
    if (await netup()):
        # print('fcopy', sd, td)
        cmd = 'rclone copy "' + str(sd) + '" "' + str(
            td) + '" --ignore-times --no-traverse --progress'
        # if not sd.is_file():
        #    cmd += ' --exclude ".git/**" --exclude "__pycache__/**"'
        print(cmd)
        rc = await ar.run2(cmd)
        if rc == 0:
            tcfc[0] += 1
            return True
        else:
            tcfc[1] += 1
    return False


async def fdel(td, tcfc):
    if (await netup()):
        cmd = 'rclone delete "' + str(td) + '" --progress'
        print(cmd)
        rc = await ar.run2(cmd)
        if rc == 0:
            tcfc[0] += 1
            return True
        else:
            tcfc[1] += 1
    return False


class BVars():
    def __init__(self, di, si, tcfc):
        from config import pdir, tdir
        self.si = si
        self.di = di
        self.sd = pdir(si)
        self.td = tdir(di)
        self.dls = None
        self.dld = None
        self.f2d = None
        self.f2c = None
        self.tcfc = tcfc
        self.ac1 = 0
        self.ac2 = 0

    async def init2(self):
        from dirlist import ldlld, rdlld, dllcmp
        self.dls = await ldlld(self.si)
        if self.dls is None:
            return
        self.dld = await rdlld(self.di)
        if self.dld is None:
            return
        self.f2d, self.f2c = dllcmp(self.dld, self.dls)

    def skip_matching(self):
        # handle slip through mismatched on times or more recent
        from config import trunc2ms
        from os import utime
        from dirlist import DE
        for rf in self.f2d.copy():
            for lf in self.f2c.copy():
                # TODO: use Path
                if rf.nm == lf.nm:  # names match
                    if rf.md5 == lf.md5:  # hashes match
                        # TODO: correct for conflicting times
                        self.f2d.remove(rf)
                        self.f2c.remove(lf)
                        print('time conflict', rf.nm)
                        print(rf.mt, '--', lf.mt)
                        b1 = abs(rf.mt - lf.mt) <= .00101
                        b2 = rf.mt < lf.mt
                        if b1:
                            print('time diff is only', rf[2] - lf[2])
                        if b1 or b2:
                            print('retrograding local timestamp', lf.nm)
                            nt = int(rf.mt * 1000) * 1000000
                            print('to', nt)
                            utime(self.sd / lf.nm, ns=(nt, nt))
                            self.ac1 += 1
                    else:
                        b1 = rf.mt > lf.mt
                        if b1:
                            print('newer file on cloud', rf.nm)
                            self.f2d.remove(rf)
                            self.f2c.remove(lf)

    async def do_copying(self):
        for lf in self.f2c.copy():
            # TODO: use Path
            cfp = lf.nm
            # print(cfp)
            if await fsync(self.sd / cfp, self.td / cfp.parent, self.tcfc):
                self.ac2 += 1
                self.f2c.remove(lf)
                for rf in self.f2d.copy():
                    if rf.nm == lf.nm:
                        self.f2d.remove(rf)

    async def do_deletions(self):
        for rf in self.f2d.copy():  # do deletions
            cfp = rf.nm
            if await fdel(self.td / cfp, self.tcfc):
                self.f2d.remove(rf)
                self.ac2 += 1


class CSCopy(OpBase):
    async def __call__(self):
        from edge import findEdge
        from statushash import rdhset, ldhset
        from dirlist import ldlls, rdlls, ldlls_dirty, rdlls_dirty
        global ldlls_dirty, rdlls_dirty
        tcfc = [0, 0]
        print('CSCopy')
        if not await netup():
            return (0, 1)
        di, si = self.npl1
        e = findEdge(di, si)
        while e.bctck():
            e.clr()
            bv = BVars(di, si, tcfc)
            await bv.init2()
            if bv.dld is None:
                return (0, 1)
            bv.ac1 = 0
            bv.ac2 = 0
            print(len(bv.f2d), 'todelete', len(bv.f2c), 'tocopy')
            bv.skip_matching()
            await bv.do_copying()
            if 'delete' in self.opts and self.opts['delete']:
                await bv.do_deletions()
            if bv.ac2:
                del rdlls[di]
                rdlls_dirty = True
                pass # await rnoc(di)
            if bv.ac1:
                del ldlls[si]
                ldlls_dirty = True
                pass # await noc(si)
            tcfc[0] += bv.tcfc[0]
            tcfc[1] += bv.tcfc[1]
            if bv.tcfc[1] != 0:
                bv.tcfc[1] = 0
                e.rtset()
        return (tcfc[0], tcfc[1])
