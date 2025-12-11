from asyncrun import run
from pathlib import Path
from opbase import OpBase
from shutil import make_archive
from os import walk, utime


def getfl(p):
    # print(str(p))
    fl = []
    try:
        if p.is_file():
            fl.append(p)
            return fl
        for pth, dirs, files in walk(p, topdown=True):
            for f in files:
                fl.append(Path(pth, f))
        return fl
    except Exception as e:
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
    return st[0]


class Mkzip(OpBase):
    async def __call__(self):
        from config import pdir, tdir, trunc2ms
        from edge import Edge, findEdge
        from status import onestatus
        from dirlist import ldlls, ldlls_dirty

        global ldlls_dirty
        print("Mkzip")
        anyd = False
        tc = 0
        fc = 0
        di1, si1 = self.npl1
        e = findEdge(di1, si1)
        if e.bctck():
            di2, si2 = self.npl2
            sd = pdir(si2)
            zf = self.opts.get("zipfile", "temp.zip")
            rp = Path(zf)
            zp = tdir(di2) / rp.stem
            try:
                fp = make_archive(zp, "zip", sd, ".", True)
                print(fp)
                maxt = maxmt(sd)
                utime(fp, ns=(maxt, maxt))
                e.clr()
                if di2 in ldlls:
                    del ldlls[di2]
                    ldlls_dirty = True
                tc += 1
            except Exception as e:
                print(e)
                fc += 1
        return (tc, fc)
