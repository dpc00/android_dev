import functools
from hashlib import blake2b

import utils
from Dir import Dir
from Drive import Drive
from File import File

BLOCK_SIZE = 512
DIRS_DIGEST_SIZE = 8
FILE_DIGEST_SIZE = 8
FILES_DIGEST_SIZE = 8
PATH_DIGEST_SIZE = 8
USE_FILE_CONTENTS_DIGESTS = True


def dbHash(ci):
    txt = ''
    while ci is not None:
        if isinstance(ci, (File, Dir)):
            txt += ci.name
        elif isinstance(ci, Drive):
            txt += '{:0>8X}'.format(ci.serialnumber & 0xFFFFFFFF)
            break
        ci = ci.pd
    pihash = blake2b(
        depth=1,
        digest_size=PATH_DIGEST_SIZE,
        fanout=1,
        inner_size=64,
        last_node=True,
        leaf_size=260,
        node_depth=0,
        node_offset=0
    )
    pihash.update(txt.encode())
    return pihash.hexdigest().upper()


@functools.total_ordering
class Digest():
    __slots__ = ('_dh', '_fh', 'rtd', 'sdl')
    def __init__(self, rtd):
        self._dh = None
        self._fh = None
        self.rtd = rtd
        self.sdl = None

    @property
    def fh(self):
        if self._fh is None:
            self._fh = self.calcFilesHash()
        return self._fh

    @property
    def dh(self):
        if self._dh is None:
            self._dh = self.calcDirsHash()
        return self._dh

    def __str__(self):
        s = ''
        v1 = int(self.fh, 16) if not self.fh is None else 0
        v2 = int(self.dh, 16) if not self.dh is None else 0
        s = '{:+017X} {:+017X} {}'.format(v1, v2, utils.chop(self.rtd.path))
        return s

    # def __eq__(self, other):
    #     return self.dh == other.dh and self.fh == other.fh

    def ddiff(self, other):
        def sdiff(s1, s2):
            os = ''
            v1 = int(s1, 16) if not s1 is None else 0
            v2 = int(s2, 16) if not s2 is None else 0
            v3 = v2 - v1
            os = '{:+017X}'.format(v3)
            return os

        s = '{:17} {:17}'.format(
            sdiff(self.fh, other.fh),
            sdiff(self.dh, other.dh)
        )
        return s

    def __lt__(self, other):
        return self.rtd.name < other.rtd.name

    def __eq__(self, other):
        return self.rtd.name == other.rtd.name

    def calcFilesHash(self):
        fh = None
        files = self.rtd.contents.files
        if len(files):
            fihash = blake2b(
                depth=1,
                digest_size=FILES_DIGEST_SIZE,
                fanout=1,
                inner_size=64,
                last_node=False,
                leaf_size=260,
                node_depth=0,
                node_offset=0
            )
            cl = sorted(files)
            ti = ''
            for fe in cl:
                ti += fe.name
                ti += str(fe.mtime/8)
                ti += str(fe.size)
            fihash.update(ti.encode())
            fh = fihash.hexdigest().upper()
        # del self.rtd.contents
        return fh

    def calcDirsHash(self):
        dh = None
        dirs = self.rtd.contents.dirs
        if len(dirs):
            dihash = blake2b(
                depth=1,
                digest_size=DIRS_DIGEST_SIZE,
                fanout=1,
                inner_size=64,
                last_node=False,
                leaf_size=260,
                node_depth=0,
                node_offset=0
            )
            dl = sorted(dirs)
            self.sdl = []
            for de in dl:
                sd = de.digest
                self.sdl.append(sd)
            self.sdl = sorted(self.sdl)
            ti = None
            for di in self.sdl:
                if di.fh:
                    if ti is None:
                        ti = ''
                    ti += di.fh
                if di.dh:
                    if ti is None:
                        ti = ''
                    ti += di.dh
            if ti is not None:
                dihash.update(ti.encode())
                dh = dihash.hexdigest().upper()
        # del self.rtd.contents
        return dh
