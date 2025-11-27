import functools
import math
import os
import threading

import utils
from Dir import fromPath, fromRelPath, findDir, NEEDS_SCAN
from File import File, findFile
from WindowsCopyFile import copy_file
from WindowsScanDir import scan_dir
from fcstats import clr, fcstats, oprint

sdrl = 0

def nind(l1, n):
    rv = [i for i in range(len(l1)) if l1[i].name == n]
    if len(rv):
        return rv[0]
    return None

interval_quit = False


def setInterval(f, t):
    def f2():
        if not interval_quit:
            f()
            setTimeout(f2, t)
    setTimeout(f2, t)

def dualPrint(l1, l2):
    for i in range(0, max(len(l1),len(l2))):
        s = ''
        if i < len(l1):
            s += '{:10}'.format(l1[i].name)
        else:
            s += '{:10}'.format('')
        if i < len(l2):
            s += ' {:10}'.format(l2[i].name)
        else:
            s += ' {:10}'.format('')
        utils.log(s)

def dualPrint2(l1, l2):
    for i in range(0, max(len(l1),len(l2))):
        s = ''
        if i < len(l1):
            s += '{:10}'.format(l1[i].rtd.name)
        else:
            s += '{:10}'.format('')
        if i < len(l2):
            s += ' {:10}'.format(l2[i].rtd.name)
        else:
            s += ' {:10}'.format('')
        utils.log(s)

def setTimeout(f, t):
    t = threading.Timer(t / 1000.0, f)
    t.setDaemon(True)
    t.start()


@functools.total_ordering
class DirSync():
    __slots__ = ['name', 'srt', 'drt', 'clearstats']
    def __init__(self, name, srt, drt, clearstats=True):
        if srt is None or drt is None:
            raise ValueError('src or dst is None')
        self.srt = srt
        self.drt = drt
        self.clearstats = clearstats
        self.name = name

    def markStale(self, d):
        def run(cd):
            cd._flags |= NEEDS_SCAN
            cd._digest = None
        d.dfWalk(run)

    def __hash__(self):
        return hash(self.srt.path + self.drt.path)

    def __lt__(self, other):
        rv = self.srt < other.srt
        if not rv:
            rv = self.drt < other.drt
        return rv

    def __eq__(self, other):
        rv = self.srt == other.srt
        if rv:
            rv = self.drt == other.drt
        return rv

    def __str__(self):
        ps = 'DirSync'
        ps += ' ' + self.name
        ps += ' ' + str(self.srt)
        ps += ' ' + str(self.drt)
        return ps

    def srcDir(self, p):
        r1 = p.replace(self.drt.path, '')
        r2 = os.path.join(self.srt.path, r1)
        return fromPath(r2)

    def dstDir(self, p):
        r1 = p.replace(self.srt.path, '')
        r2 = os.path.join(self.drt.path, r1)
        return fromPath(r2)

    def run(self, includesubdirs=True, controlstats=True):
        global interval_quit, sdrl
        if controlstats:
            interval_quit = False
            setInterval(oprint, 3000)
            if self.clearstats:
                clr()
        self.syncDir('', includesubdirs)
        oprint()
        if controlstats:
            interval_quit = True

    # def run2(self, includesubdirs=True, controlstats=True):
        # global interval_quit, sdrl
        # if controlstats:
            # interval_quit = False
            # setInterval(oprint, 3000)
            # if self.clearstats:
                # clr()
        # self.syncFromDigests('', True)
        # oprint()
        # if controlstats:
            # interval_quit = True

    def syncDir(self, rd, includesubdirs=False):
        cd1 = fromRelPath(self.srt, rd)
        cd2 = fromRelPath(self.drt, rd)
        # dirEE.emit('dsync', cd1.path, cd2.path)
        if cd1.exists():
            if not cd2.exists():
                cd2.create()
            self.handleFiles(cd1, cd2)
            fcstats['sdhf'] += 1
            if includesubdirs:
                self.handleDirs1(cd1, cd2, rd, includesubdirs)
                fcstats['sdhd'] += 1
            fcstats['syncdir'] += 1
            # dirEE.emit('dcopy', cd1.path, cd2.path)

    def handleFiles(self, cd1, cd2):
        scf = set(cd1.contents.files)
        ocf = set(cd2.contents.files)

        def fc1(f1, f2):
            if f1.name == f2.name:
                if f2.mtime - f1.mtime >= 0:
                    if f1.size == f2.size:
                        return False
            return True

        ca = []
        da = []
        for si in scf:
            if si in ocf:
                for di in ocf:
                    if di.name == si.name:
                        copy = fc1(si, di)
                        break
            else:
                copy = True
            if copy:
                ca.append(si)
        for di in ocf:
            if di not in scf:
                da.append(di)
        if len(ca):
            for si in ca:
                f1f = si
                f1 = si.name
                f2f = None
                for di in ocf:
                    if di.name == si.name:
                        f2f = di
                        f2 = di.name
                        break
                if f2f is None:
                    f2f = File(cd2, f1)
                    f2 = f2f.name
                self.fileCopy(f1f, f2f)
        if len(da):
            for si in da:
                for di in ocf:
                    if di.name == si.name:
                        f2f = di
                        f2 = di.name
                        break
                if f2f is not None:
                    self.fileDelete(f2f)
        pass

    def handleDirs1(self, cd1, cd2, rd, includesubdirs):
        scd = set(cd1.contents.dirs)
        ocd = set(cd2.contents.dirs)

        def dc1(d1, d2):
            if d1.name == d2.name:
                return False
            return True

        ca = []
        da = []
        for si in scd:
            ca.append(si)
        for di in ocd:
            if di not in scd:
                da.append(di) # deleting missing directories
        if len(ca):
            for si in ca:
                d1d = si
                self.syncDir(d1d.relPath(self.srt), includesubdirs)
        if len(da):
            for si in da:
                for di in ocd:
                    if di.name == si.name:
                        d2d = di
                        d2 = di.name
                        break
                if d2d is not None:
                    self.dirDelete(d2d)
        pass

    def fileCopy(self, f1, f2):
        # from Dir import dirEE
        src = f1.path
        dst = f2.path
        try:
            utils.log(utils.chop('copying ' + src))
            utils.log('')
        except Exception as e:
            utils.errlog(e)
        tt = '0'
        try:
            tt += '1'
            try:
                tt += '2'
                #                 with open(src, 'rb') as fsrc:
                #                     tt += '3'
                #                     with open(dst, 'wb') as fdst:
                #                         tt += '4'
                #                         shutil.copyfileobj(fsrc, fdst, length=(2 ** 26 - 2 ** 15))
                #                 tt += '5'
                #                 shutil.copystat(src, dst, follow_symlinks=False)
                rc = copy_file(src, dst)
                tt += '6'
            except OSError as e:
                dstd = f2.pd.path
                if dstd.find(' ') != -1:
                    dstd = '\"' + dstd + '\"'
                srcd = f1.pd.path
                if srcd.find(' ') != -1:
                    srcd = '\"' + srcd + '\"'
                rv = os.system('robocopy ' + srcd + ' ' + dstd + ' ' + f1.name + ' /r:1 /w:3 /dcopy:t')
                tt += '7'
                if rv != 0:
                    tt += '8'
                    utils.log(tt)
                    raise OSError('robocopy rc: ' + str(rv))
                else:
                    utils.log(tt)
            tt += '9'
            ccnt = 0
            if f2.exists():
                de = list(scan_dir(f2.path, True))[0]
                if de:
                    it2 = findFile(f2.pd, de[0])
                    if it2 is None:
                        it2 = f2
                        tmp = set(it2.pd.contents.files)
                        tmp.add(it2)
                        it2.pd.contents.files = list(tmp)
                        ccnt += 1
                    elif it2.mtime != de[1] or it2.size != de[2]:
                        ccnt += 1
                    it2.mtime = de[1]
                    it2.size = de[2]
                    it2.attrib = de[3]
                    it2.res0 = de[4]
                    fcstats['fcpy'] += 1
                    fcstats['bcpy'] += it2.size
                    # dirEE.emit('fcopy', self.path, other.path)
                    if ccnt:
                        it2.clearDigest()
        except OSError as e:
            tt += 'D'
            utils.log(tt)
            utils.errlog(e)


    def fileDelete(self, f1):
        # from Dir import dirEE
        if f1.exists():
            try:
                try:
                    utils.log(utils.chop('deleting ' + f1.path))
                except Exception as e:
                    utils.errlog(e)
                try:
                    os.unlink(f1.path)
                except OSError as e:
                    rv = os.system('del ' + self.path)
                    if rv != 0:
                        raise OSError('del rc: ' + str(rv))
                if not f1.exists():
                    it2 = findFile(f1.pd, f1.name)
                    if it2 is not None:
                        f1.pd.contents.files.remove(it2)
                        it2.clearDigest()
                    fcstats['fdel'] += 1
                    fcstats['bdel'] += f1.size
                    # dirEE.emit('fdel', self.path)
            except OSError as e:
                utils.errlog(e)
                raise


    def dirDelete(self, d1):
        if d1.exists():
            try:
                c = d1.contents
                for d1d in c.dirs.copy():
                    self.dirDelete(d1d)
                for f1f in c.files.copy():
                    self.fileDelete(f1f)
                os.rmdir(d1.path)
                if not d1.exists():
                    it1 = findDir(d1.pd, d1.name)
                    if it1 is not None:
                        it1.pd.contents.dirs.remove(it1)
                        it1.clearDigest2()
                    fcstats['ddel'] += 1
            except OSError as e:
                utils.errlog(e)



