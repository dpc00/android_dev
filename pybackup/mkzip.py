import math
from os import utime, walk
from pathlib import Path
from shutil import make_archive

import config
from edge import Edge, findEdge
from findde import updateDEs
from opbase import OpBase
from status import onestatus


def getfl(p):
    # print(str(p))
    fl = []
    try:
        if p.is_file():
            fl.append(p)
            return fl
        for pth, _dirs, files in walk(p, topdown=True):
            for f in files:
                fl.append(Path(pth, f))
        return fl
    except OSError as e:
        print(e)
        return None


def maxmt(sd):
    l1 = getfl(sd)

    def es(it):
        # TODO: use Path
        fs = it.stat()
        it3 = fs.st_mtime_ns
        return it3

    st = list(map(es, l1))
    st.sort(reverse=True)
    return int(math.floor(st[0] / 1.0e6) * 1.0e6)


class Mkzip(OpBase):
    def __init__(self, npl1, npl2, opts={}) -> None:
        super().__init__(npl1, npl2, opts)

    def ischanged(self, e: Edge):
        return e.chk_ct()

    def __call__(self):
        print("Mkzip")
        sc = 0
        fc = 0
        di1, si1 = self.npl1
        e: Edge = findEdge(di1, si1)
        if e.chk_ct():
            di2, si2 = self.npl2
            sd = config.src(si2)
            td = config.tgt(di2)
            zf = self.opts.get("zipfile", "temp.zip")
            zp = td / Path(zf).stem
            try:
                fp = Path(make_archive(zp, "zip", sd, ".", True))
                print(fp)
                maxt = maxmt(sd)
                utime(fp, ns=(maxt, maxt))
                sc += 1
                updateDEs(td, [zf])
            except OSError as er:
                print(er)
                fc += 1
            if sc > 0:
                onestatus(di2)
        if fc == 0:
            e.clr()
        return (sc, fc)
