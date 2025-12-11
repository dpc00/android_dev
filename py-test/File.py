import datetime
import functools
import os

import utils
from Drive import Drive
from WindowsScanDir import fileExists, scan_dir

FAT32_GRANULARITY = 20000000


def nind(l1, n):
    rv = [i for i in range(len(l1)) if l1[i].name == n]
    if len(rv):
        return rv[0]
    return None


@functools.total_ordering
class File:
    __slots__ = ["_path", "attrib", "mtime", "name", "pd", "res0", "size"]
    csp = None

    def __init__(self, pd, name, mtime=None, size=None, attrib=None, res0=None):
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
        ps = "File {:12} {:25} {:12} {:4} {:4}".format(
            self.name, self.mtime, self.size, self.attrib, self.res0
        )
        ps += ", in "
        ps += self.pd.path
        return ps

    def exists(self):
        return fileExists(self.path)

    @property
    def path(self):  # File
        from Dir import Dir

        if self._path is None:
            if self.pd is None:
                self._path = self.name
            else:
                if isinstance(self.pd, Drive):  # error
                    self._path = self.name
                    utils.errlog(Exception("file in root dir location" + self.pd.path))
                else:
                    if isinstance(self.pd, Dir):
                        self._path = self.pd.path + os.path.sep + self.name
        return self._path

    def relPath(self, rpd):
        return os.path.relpath(self.path, rpd.path)

    def getDrive(self):
        cd = self
        while not isinstance(cd, Drive):
            cd = cd.pd
        return cd

    def fline(self):
        fs1 = " {:22.21} "
        fs2 = " {:10d} "
        fs3 = " {:%Y-%m-%d %H:%M} "

        def fline2(file):
            ps = fs1.format(file.name)
            ps += fs2.format(file.de.size)
            ps += fs3.format(datetime.datetime.fromtimestamp(file.de.mtime))
            return ps

        return fline2(self)

    def clearDigest(self):
        cd = self.pd
        if cd._digest is not None:
            cd._digest._fh = None
        cd = self.pd
        while not isinstance(cd, Drive):
            if cd._digest is not None:
                cd._digest._dh = None
            cd = cd.pd

    def update(self):
        from Dir import NEEDS_SCAN

        ccnt = 0
        if self.exists():
            de = None
            try:
                de = list(scan_dir(self.path, True))[0]
            except FileNotFoundError:
                pass
            if de:
                it2 = findFile(self.pd, de[0])
                if it2 is None:
                    it2 = self
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
                # fcstats['fcpy'] += 1
                # fcstats['bcpy'] += it2.size
                # dirEE.emit('fcopy', self.path, other.path)
                if ccnt:
                    it2.pd._flags |= NEEDS_SCAN
                    it2.clearDigest()
            else:
                it2 = findFile(self.pd, self.name)
                if it2 is not None:
                    tmp = set(it2.pd.contents.files)
                    tmp.remove(it2)
                    it2.pd.contents.files = list(tmp)
                    ccnt += 1
                if ccnt:
                    it2.pd._flags |= NEEDS_SCAN
                    it2.clearDigest()


def findFile(pd, name):
    from Dir import Dir

    if pd is None:
        raise ValueError("no pd in findFile")
    if isinstance(pd, Dir):
        files = pd.contents.files
        for fk in files:
            if fk.name.upper() == name.upper():
                return fk
    elif isinstance(pd, Drive):
        return None
