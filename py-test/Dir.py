"""
Created on Jul 24, 2016

@author: Phil Chitester
"""

import datetime
import functools
import os
import re

from Drive import Drive, driveFromDL
from File import File
from WindowsScanDir import dirExists, scan_dir
from fcstats import fcstats
import utils


abortcalled = False
clog = {}
drives = None
restarting = True
tablesdeleted = False

VERBOSE = False
FILES_DIGEST_SIZE = 8
NEEDS_SCAN = 1

updateQ = []


def nind(l1, n):
    rv = [i for i in range(len(l1)) if l1[i].name == n]
    if len(rv):
        return rv[0]
    return None


def eE(run, *args):
    try:
        rv = run(*args)
        return rv
    except Exception as e:
        utils.errlog(e)
        raise


def eE2(run, *args):
    return run(*args)


def findDir(pd, name):
    if pd is None:
        raise ValueError("no pd in findDir")
    if isinstance(pd, Dir):
        dirs = pd.contents.dirs
        for dk in dirs:
            if dk.name.upper() == name.upper():
                return dk
    elif isinstance(pd, Drive):
        if name == "":
            return pd.rt


def findPath(p):
    l = re.split(r"[\\]+", p)
    pl = []
    if len(l[0]) == 2 and l[0][1] == ":":
        rv1 = driveFromDL(l[0][0])
        if rv1:
            pl.append(rv1)
            rv2 = findDir(rv1, "")
            if not rv2:
                return None
            if rv2:
                pl.append(rv2)
        l = l[1:]
    for i in range(len(l)):
        if len(l[i]):
            if len(pl) - 1 >= 0:
                rv3 = findDir(pl[len(pl) - 1], l[i])
                if not rv3:
                    if i == len(l) - 1:
                        from File import findFile

                        rv3 = findFile(pl[len(pl) - 1], l[i])
                if rv3:
                    pl.append(rv3)
                else:
                    return None
    return pl[len(pl) - 1]


def fromPath(p):
    l = re.split(r"[\\]+", p)
    pl = []
    if len(l[0]) == 2 and l[0][1] == ":":
        rv1 = driveFromDL(l[0][0])
        if rv1:
            pl.append(rv1)
            rv2 = findDir(rv1, "")
            if not rv2:
                rv2 = Dir(rv1, "")
            if rv2:
                pl.append(rv2)
        l = l[1:]
    for i in range(len(l)):
        if len(l[i]):
            if len(pl) - 1 >= 0:
                rv3 = findDir(pl[len(pl) - 1], l[i])
                if not rv3:
                    rv3 = Dir(pl[len(pl) - 1], l[i])
                if rv3:
                    pl.append(rv3)
            else:
                rv4 = findDir(None, l[i])
                if not rv4:
                    rv4 = Dir(None, l[i])
                if rv4:
                    pl.append(rv4)
    return pl[len(pl) - 1]


def fromRelPath(pd, p):
    l = re.split(r"[\\]+", p)
    pl = []
    pl.append(pd)
    for i in range(len(l)):
        if len(l[i]):
            if len(pl) - 1 >= 0:
                rv1 = findDir(pl[len(pl) - 1], l[i])
                if not rv1:
                    rv1 = Dir(pl[len(pl) - 1], l[i])
                if rv1:
                    pl.append(rv1)
            else:
                rv2 = findDir(None, l[i])
                if not rv2:
                    rv2 = Dir(None, l[i])
                if rv2:
                    pl.append(rv2)
    return pl[len(pl) - 1]


# def dbHash(ci):
#     txt = []
#     while ci is not None:
#         if isinstance(ci, (File, Dir)):
#             txt.insert(0, ci.name)
#         elif isinstance(ci, Drive):
#             txt.insert(0, '{:0>8X}'.format(ci.serialnumber & 0xFFFFFFFF))
#             break
#         ci = ci.pd
#     if len(txt):
#         pihash = blake2b(
#                 depth=1,
#                 digest_size=PATH_DIGEST_SIZE,
#                 fanout=1,
#                 inner_size=64,
#                 last_node=False,
#                 leaf_size=260,
#                 node_depth=0,
#                 node_offset=0
#                 )
#         for ti in txt:
#             pihash.update(ti.encode())
#         return pihash.hexdigest().upper()
#     return None

dlist = []


def getLists(cd):
    # utils.log('appending ' + cd.path)
    # try:
    #     dlist.remove(cd)
    #     dlist.append(cd)
    # except ValueError:
    #     dlist.append(cd)
    if cd._files is None:
        cd._files = []
    if cd._dirs is None:
        cd._dirs = []
    # if len(dlist) > 8192:
    #     cd = dlist.pop(0)
    #     # utils.log('deleting ' + cd.path)
    #     cd._files = None
    #     cd._dirs = None
    #     cd._flags |= NEEDS_SCAN


def scan(cd):
    if cd._dirs is None or cd._files is None:
        isupdate = False
    else:
        isupdate = True
    getLists(cd)
    if VERBOSE:
        tf = "scanning " + cd.name
        utils.writedata("\r" + utils.chop(tf))
    try:
        sdi = scan_dir(cd.path, False)
        if isupdate:
            sl = set()
        for de in sdi:  # WindowsScanDir
            if de[6]:  # isFile
                it1 = None
                if isupdate and de[0] in [it.name for it in cd._files]:
                    it1 = [it for it in cd._files if it.name == de[0]][0]
                    if it1.mtime != de[1] or it1.size != de[2]:  # modified
                        it1.mtime = de[1]
                        it1.size = de[2]
                        it1.attrib = de[3]
                        it1.res0 = de[4]
                        cd.clearDigest1()
                else:  # new
                    it1 = File(cd, de[0], de[1], de[2], de[3], de[4])
                    cd._files.append(it1)  # new
                    cd.clearDigest1()
                fcstats["w_file_scan"] += 1
            elif de[5]:
                it1 = None
                if de[0] not in (".", "..", ".sync"):
                    if isupdate and de[0] in [it.name for it in cd._dirs]:
                        it1 = [it for it in cd._dirs if it.name == de[0]][0]
                        if it1.mtime != de[1] or it1.size != de[2]:  # modified
                            it1.mtime = de[1]
                            it1.size = de[2]
                            it1.attrib = de[3]
                            it1.res0 = de[4]
                            cd.clearDigest2()
                    else:  # new
                        it1 = Dir(cd, de[0], de[1], de[2], de[3], de[4])
                        cd._dirs.append(it1)
                        cd.clearDigest2()
                fcstats["w_dir_scan"] += 1
            if isupdate:
                sl.add(it1)
        if isupdate:
            for it1 in cd._files:
                if it1 not in sl:
                    it2 = [it for it in cd._files if it.name == it1.name][0]
                    cd._files.remove(it2)
                    cd.clearDigest1()
            for it1 in cd._dirs:
                if it1 not in sl:
                    it2 = [it for it in cd._dirs if it.name == it1.name][0]
                    cd._dirs.remove(it2)
                    cd.clearDigest2()
    except OSError:
        pass
    fcstats["scan_dir"] += 1
    if isupdate:
        fcstats["update_dir"] += 1


def dirPrint(d):
    fs1 = " {:22.21} "
    fs2 = " {:10d} "
    fs3 = " {:%Y-%m-%d %H:%M} "

    def dline(d):
        ps = fs1.format(d.name)
        ps += fs3.format(datetime.datetime.fromtimestamp(d.de.mtime))
        utils.log(ps)

    utils.log("-----------------")

    def fline(file):
        ps = fs1.format(file.name)
        ps += fs2.format(file.de.size)
        ps += fs3.format(datetime.datetime.fromtimestamp(file.de.mtime))
        utils.log(ps)

    for de in sorted(d.contents.dirs):
        dline(de)
    for fe in sorted(d.contents.files):
        fline(fe)


class DC:
    def __init__(self, files, dirs):
        self.files = files
        self.dirs = dirs

    def __str__(self):
        s = "("
        s += "files: {}".format(repr(self.files))
        s += "dirs: {}".format(repr(self.dirs))
        s += ")"
        return s


@functools.total_ordering
class Dir:
    __slots__ = [
        "_dbhash",
        "_digest",
        "_dirs",
        "_files",
        "_flags",
        "_path",
        "attrib",
        "mtime",
        "name",
        "pd",
        "res0",
        "size",
    ]

    def __init__(self, pd, name, mtime=None, size=None, attrib=None, res0=None):
        self._dbhash = None
        self._digest = None
        self._dirs = None
        self._files = None
        self._flags = NEEDS_SCAN
        self._path = None
        self.attrib = attrib
        self.mtime = mtime
        self.name = name
        self.pd = pd
        self.res0 = res0
        self.size = size

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        ps = ""
        try:
            if self.name == "":
                ps += " " + "\\"
            else:
                ps += " " + self.name
            ps += ", in " + self.pd.path
        except AttributeError as e:
            utils.errlog(e)
        return ps

    def create(self):
        if not self.exists():
            self.make()

    def exists(self):
        return dirExists(self.path)

    def getDrive(self):
        cd = self
        while not isinstance(cd, Drive):
            cd = cd.pd
        fcstats["getdrv"] += 1
        return cd

    def getRoot(self):
        ocd = self
        cd = ocd.pd
        while not isinstance(cd, Drive):
            ocd = cd
            cd = ocd.pd
        fcstats["getrt"] += 1
        return ocd

    @property
    def path(self):  # Dir
        if self._path is None:
            if not self.pd:
                if self.name == "":
                    self._path = os.path.sep
                else:
                    self._path = self.name
            else:
                if isinstance(self.pd, Drive):
                    if self.name == "":
                        self._path = self.pd.path + os.path.sep
                    else:
                        self._path = self.pd.path + self.name
                else:
                    if isinstance(self.pd, Dir):
                        if self.pd.name == "":
                            self._path = self.pd.path + self.name
                        else:
                            self._path = self.pd.path + os.path.sep + self.name
                    else:
                        e = TypeError("path")
                        raise e
            fcstats["path"] += 1
        return self._path

    def make(self):
        dp = self.path
        mode = int("0777")
        os.makedirs(dp, mode, True)
        self.clearDigest1()
        fcstats["dirmake"] += 1

    def relPath(self, rpd):
        fcstats["relpth"] += 1
        return os.path.relpath(self.path, rpd.path)

    def dfWalk(self, f, *args):
        for de in sorted(self.contents.dirs):
            de.dfWalk(f, *args)
        f(self, *args)

    @property
    def dbHash(self):
        if self._dbhash is None:
            from Digest import dbHash

            self._dbhash = dbHash(self)
        return self._dbhash

    @property
    def contents(self):
        global VERBOSE
        if self._flags & NEEDS_SCAN:
            scan(self)
            self._flags &= ~NEEDS_SCAN
        rv = DC(self._files, self._dirs)
        # self._files = None
        # self._dirs = None
        return rv

    @contents.deleter
    def contents(self):
        self._flags |= NEEDS_SCAN
        self._files = None
        self._dirs = None

    @property
    def digest(self):
        if self._digest is None:
            from Digest import Digest

            self._digest = Digest(self)
        return self._digest

    def clearDigest1(self):
        if self._digest is not None:
            if self._digest._fh is not None:
                self._digest._fh = None
        cd = self.pd
        while not isinstance(cd, Drive):
            if cd._digest is not None:
                if cd._digest._dh is not None:
                    cd._digest._dh = None
                else:
                    break
            cd = cd.pd
        fcstats["clrd1"] += 1

    def clearDigest2(self):
        if self._digest is not None:
            if self._digest._dh is not None:
                self._digest._dh = None
        cd = self.pd
        while not isinstance(cd, Drive):
            if cd._digest is not None:
                if cd._digest._dh is not None:
                    cd._digest._dh = None
                else:
                    break
            cd = cd.pd
        fcstats["clrd2"] += 1

    def update(self):
        ccnt = 0
        if self.exists():
            de = None
            try:
                de = list(scan_dir(self.path, True))[0]
            except FileNotFoundError:
                pass
            if de:
                it2 = findDir(self.pd, de[0])
                if it2 is None:
                    it2 = self
                    tmp = set(it2.pd.contents.dirs)
                    tmp.add(it2)
                    it2.pd.contents.dirs = list(tmp)
                    ccnt += 1
                elif it2.mtime != de[1] or it2.size != de[2]:
                    ccnt += 1
                it2.mtime = de[1]
                it2.size = de[2]
                it2.attrib = de[3]
                it2.res0 = de[4]
                # fcstats['fcpy'] += 1
                # fcstats['bcpy'] += it2.size
                # dirEE.emit('fcopy', self.path, other.path)
                if ccnt:
                    it2._flags |= NEEDS_SCAN
                    it2.clearDigest1()
            else:
                it2 = findDir(self.pd, self.name)
                if it2 is not None:
                    tmp = set(it2.pd.contents.dirs)
                    tmp.remove(it2)
                    it2.pd.contents.dirs = list(tmp)
                    ccnt += 1
                if ccnt:
                    it2._flags |= NEEDS_SCAN
                    it2.clearDigest1()
