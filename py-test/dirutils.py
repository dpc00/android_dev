'''
Created on Jul 8, 2016

@author: Phil
'''

import filecmp
import os

from EventEmitter import EventEmitter
import diskutils
import fcopy
import fcstats
import utils
from Dos4 import Dos4


dmEE1 = EventEmitter('dmEE1')

edcnt = 0
odcnt = 0

def dirMatchCase(p):
    pd = os.path.dirname(p)
    if pd != p:
        v1 = os.path.basename(p).lower()
        (err, dl) = diskutils.readDir(pd)
        if err:
            return p
        def run(f2):
            b1 = f2.lower() == v1
            return b1
        fdd = [f3 for f3 in dl if run(f3)]
        return os.path.join(pd, fdd[0])
    else:
        return p


def dirTreeWalk(pth1, fn, norecurse, exc_dirs):
    pth2 = dirMatchCase(pth1)
    if pth1 != pth2:
        utils.log('case conflict:' + pth1 + ' changed to ' + pth2)
    dexc = False
    if exc_dirs is not None:
        if len(exc_dirs) > 0:
            def excl(pth3):
                def run(ex):
                    b1 = len(pth3) >= len(ex)
                    b2 = pth3[0:len(ex)].lower() == ex.lower()
                    return b1 and b2
                return len([ex for ex in exc_dirs if run(ex)]) > 0
            if excl(pth2):
                dexc = True
    if not dexc:
        if not norecurse:
            (err1, contents) = diskutils.dirsList(pth2)
            if not err1:
                for dr in contents:
                    dirTreeWalk(os.path.join(pth2, dr), fn, norecurse, exc_dirs)
        fn(pth2)


def showprogress():
    global edcnt, odcnt
    utils.writedata(str(odcnt) + ' contents scanned, ' + str(edcnt) + ' contents containing executables')
    utils.writedata('\r')


def dirsContainingType(sp, exs, norecurse, exc_dirs):
    bfp = []
    def adde(dp1, fl1):
        bfp.append({
            'path': dp1,
            'include': False,
            'files': fl1
        })
    def dwf(dp2):
        global odcnt, edcnt
        odcnt += 1
        (err1, fl) = diskutils.filesList(dp2, exs)
        if not err1:
            if len(fl) > 0:
                adde(dp2, fl)
                edcnt += 1
                showprogress()
    dirTreeWalk(sp, dwf, norecurse, exc_dirs)
    return bfp

'''
dct = dirsContainingType(
    '\\Projects',
    {'.bat', '.com', '.sublime-workspace'},
    True,
    [])
print(dct)
'''

def delDir(d2):
    (err1, d2dl) = diskutils.dirsList(d2)
    if err1:
        # print(str(err1))
        return (err1, None)
    else:
        for d2d in d2dl.keys():
            fp = os.path.join(d2, d2d)
            (err2, _) = delDir(fp)
            if err2:
                # print(str(err2))
                return (err2, None)
        (err3, d2fl) = diskutils.filesList(d2, None)
        if err3:
            # print(str(err3))
            return (err3, None)
        else:
            for d2f in d2fl.keys():
                fp = os.path.join(d2, d2f)
                (err4, _) = diskutils.delFile(fp)
                if err4:
                    # print(str(err4))
                    return (err4, None)
                else:
                    dmEE1.emit('fdel', fp)
            (err5, _) = diskutils.rmDir(d2)
            if err5:
                # print(str(err5))
                return (err5, None)
            else:
                dmEE1.emit('ddel', d2)
                return (None, d2)

def llookup(l, f):
    if f in l:
        return f
    else:
        return None

def llookup2(l, d):
    if d in l:
        return d
    else:
        return None


def delDirs(d1, d2):
    (err1, d1dl) = diskutils.dirsList(d1)
    if err1:
        # print(str(err1))
        return (err1, 0)
    else:
        (err2, d2dl) = diskutils.dirsList(d2)
        if err2:
            # print(str(err2))
            return (err2, 0)
        else:
            toDelete = [d for d in d2dl.keys() if not llookup2(d1dl, d)]
            for d in toDelete:
                fp = os.path.join(d2, d)
                (err3, _) = delDir(fp)
                if err3:
                    # print(str(err3))
                    return (err3, None)
            return (None, len(toDelete))

def delFiles(d1, d2, exs):
    (err1, d1fl) = diskutils.filesList(d1, exs)
    if err1:
        # print(str(err1))
        return (err1, None)
    else:
        (err2, d2fl) = diskutils.filesList(d2, exs)
        if err2:
            # print(str(err2))
            return (err2, None)
        else:
            toDelete = [f for f in d2fl.keys() if not llookup(d1fl, f)]
            for f in toDelete:
                fp = os.path.join(d2, f)
                (err3, _) = diskutils.delFile(fp)
                if err3:
                    # print(str(err3))
                    return (err3, None)
                else:
                    dmEE1.emit('fdel', fp)
            return (None, len(toDelete))


def dPath(d1, d2, p):
    r1 = os.path.relpath(p, d1)
    return os.path.join(d2, r1)


def fCompare(s, t):
    try:
        return filecmp.cmp(s, t, False)
    except Exception as e:
        utils.errlog(e)
        return False

def cc1(sd, td, s, t, sfl, tfl):
    if t is None:
        return False
    return True

def cc2(sd, td, s, t, sfl, tfl):
    if tfl[t]['mtime'] < sfl[s]['mtime']:
        return False
    return True

def cc4(sd, td, s, t, sfl, tfl):
    if tfl[t]['mtime'] != sfl[s]['mtime']:
        return False
    return True

def cc8(sd, td, s, t, sfl, tfl):
    if tfl[t]['size'] != sfl[s]['size']:
        return False
    return True

def cc16(sd, td, s, t, sfl, tfl):
    return fCompare(os.path.join(sd, s), os.path.join(td, t))

copycrit = [cc1, cc2, cc4, cc8, cc16]

ccrit = 1 | 2

def copyFiles(d1, d2, exs, ccrit):
    (err1, d1fl) = diskutils.filesList(d1, exs)
    if err1:
        # print(str(err1))
        return (err1, None)
    else:
        (err2, d2fl) = diskutils.filesList(d2, exs)
        if err2:
            # print(str(err2))
            return (err2, None)
        else:
            fc = 0
            toCopy = []
            for d1f in d1fl.keys():
                d2f = llookup(d2fl, d1f)
                for k in range(len(copycrit)):
                    bit = 1 << k
                    if ccrit & bit:
                        if not copycrit[k](d1, d2, d1f, d2f, d1fl, d2fl):
                            toCopy.append(d1f)
                            break
            err4 = False
            for d1f in toCopy:
                sfp = os.path.join(d1, d1f)
                dfp = dPath(d1, d2, sfp)
                (err3, fs) = fcopy.copyFile(sfp, dfp)
                if err3:
                    # print(str(err3))
                    utils.flog('fcopy', err3)
                    err4 = err3
                else:
                    fcstats.fcstats['fcpy'] += 1
                    fcstats.fcstats['bcpy'] += fs
                    dmEE1.emit('fcopy', sfp, dfp)
                    fc += 1
            if err4:
                return (err4, fc)
            else:
                return (None, fc)

def mirrorDirs(d1, d2, exc_dirs):
    if not exc_dirs is None and d1 in exc_dirs:
        return (None, False)
    (err1, toCopy) = diskutils.dirsList(d1)
    # d2dl = diskutils.dirsList(d2)
    dc = 0
    if err1:
        # print(str(err1))
        return (err1, None)
    else:
        err3 = False
        for d1d in toCopy.keys():
            sdp = os.path.join(d1, d1d)
            ddp = dPath(d1, d2, sdp)
            (err2, _) = dirMirror(sdp, ddp, exc_dirs)
            if err2:
                # print(str(err2))
                err3 = err2
            else:
                dc += 1
        if err3:
            return (err3, dc)
        else:
            return (None, dc)

def dirCopy(d1, d2, exs):
    # fcstats.clr()
    (err1, de) = diskutils.dirExists(d2)
    if err1:
        # print(str(err1))
        return (err1, None)
    else:
        if not de:
            (err2, _) = diskutils.mkDirs(d2, None)
            if err2:
                # print(str(err2))
                return (err2, None)
        (err3, _) = copyFiles(d1, d2, exs, 1 | 2)
        if err3:
            # print(str(err3))
            return (err3, None)
        else:
            fcstats.fcstats['dsyn'] += 1
            dmEE1.emit('dcopy', d1, d2)

def dirSync(d1, d2, exs, exc_dirs):
    if exc_dirs is not None:
        if d1 in exc_dirs:
            return (None, False)
    (err1, de) = diskutils.dirExists(d2)
    if err1:
        # print(str(err1))
        return (err1, None)
    else:
        if not de:
            (err2, _) = diskutils.mkDirs(d2, None)
            if err2:
                # print(str(err2))
                return (err2, None)
        (err3, _) = copyFiles(d1, d2, exs, 1 | 2 | 4 | 8)
        err5 = False
        if err3:
            # print(str(err3))
            err5 = err3
        (err4, _) = delFiles(d1, d2, exs)
        if err4:
            # print(str(err4))
            err5 = err4
        if err5:
            return (err5, None)
        else:
            fcstats.fcstats['dcpy'] += 1
            dmEE1.emit('dcopy', d1, d2)
            return (None, d1)

def dirMirror(d1, d2, exc_dirs):
    if exc_dirs is not None:
        if d1 in exc_dirs:
            return (None, False)
    (err1, de) = diskutils.dirExists(d2)
    if err1:
        # print(str(err1))
        return (err1, None)
    else:
        if not de:
            (err2, _) = diskutils.mkDirs(d2, None)
            if err2:
                # print(str(err2))
                return (err2, None)
        (err3, _) = dirSync(d1, d2, None, exc_dirs)
        err6 = False
        if err3:
            # print(str(err3))
            err6 = err3
        (err4, _) = delDirs(d1, d2)
        if err4:
            # print(str(err4))
            err6 = err4
        (err5, _) = mirrorDirs(d1, d2, exc_dirs)
        if err5:
            # print(str(err5))
            err6 = err5
        if err6:
            return (err6, None)
        else:
            return (None, d1)

def touchBats():
    exe = ''
    def setExe():
        nonlocal exe
        ps = utils.expES('%FLASH0%\\Programs\\Git\\usr\\bin')
        exe = ps + '\\touch.exe'
        return True
    if setExe():
        d = utils.expES('%FLASH0%\\')
        (err1, fl) = diskutils.filesList(d, {'.bat'})
        if err1:
            return (err1, None)
        else:
            fl = [os.path.join(d, f) for f in fl.keys() if f]
            rv = Dos4({
                'cmd': exe,
                'args': fl,
                'collect': False,
                'echo': True,
                'print': True
            })
            if rv.rejected:
                return (OSError(rv.returncode(), 'touch bats failed'), None)
            else:
                return (None, len(fl))
