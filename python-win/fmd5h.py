import asyncio
import pickle
from hashlib import md5

from config import *

fmd5hf = pre("USER") / "fmd5h.pp"
fmd5hd = {}

hf_dirty = False


def md5sumf(Fn):
    if Fn.exists():
        # print('-md5sumf', Fn)
        ho = md5()
        try:
            with open(Fn, "rb") as fh:
                b = fh.read(1 << 12)
                while len(b) > 0:
                    ho.update(b)
                    b = fh.read(1 << 12)
            return ho.digest()
        except:
            return 0
    return None


hf_dm = 0
hf_dh = 0
hf_pm = 0
hf_ph = 0
hf_stm = 0
hf_sth = 0


def pstats():
    print("fp miss", hf_dm)
    print("fp hit", hf_dh)
    print("szmt miss", hf_stm)
    print("szmt hit", hf_sth)
    print("sfb", sfb)


def finddict(d1, fp):
    ta = fp.parent.parts
    for dir in ta:
        if dir not in d1:
            d1[dir] = {}
        d1 = d1[dir]
    return d1


def fmd5f(fp, sz, mt):
    global fmd5hd, hf_dirty, hf_dm, hf_dh, hf_stm, hf_sth
    d1 = finddict(fmd5hd, fp)
    try:
        (osz, omt, oh) = d1[fp.name]
        hf_dh += 1
    except KeyError:
        hf_dm += 1
        (osz, omt, oh) = (-1, -1, b"")
    if osz == sz and omt == mt:
        hf_sth += 1
        return oh
    else:
        hf_stm += 1
        nh = md5sumf(fp)
        d1[fp.name] = (sz, mt, nh)
        hf_dirty = True
        return nh


def loadfmd5h():
    global fmd5hd
    try:
        fmd5hd = {}
        with open(fmd5hf, "rb") as fh:
            fmd5hd = pickle.load(fh)
    except:
        hf_dirty = True
        pass


sfb = 0


def savefmd5h():
    global sfb, hf_dirty
    if hf_dirty:
        with open(fmd5hf, "wb") as fh:
            pickle.dump(fmd5hd, fh)
        sfb += fmd5hf.stat().st_size
        pstats()
        hf_dirty = False


if __name__ == "__main__":
    from dirlist import ldlld

    for si in srcs:
        dll = asyncio.run(ldlld(si))
else:
    loadfmd5h()
