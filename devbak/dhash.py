import pickle
import hashlib

from bkenv import *
from ddb import *

dhd = None
dhpf = pre["FLAGS"] / "dhd.pp"


def dhstrf(si, dh=None):
    global dhd
    if si not in dhd:
        dhd[si] = None
    odh = dhd[si]
    if dh is not None:
        dhd[si] = dh
    return odh


def sha256sumd(dir):
    ho = hashlib.sha256()
    ho.update(getdlstr(dir))
    return ho.hexdigest()


def dhstrd(sil):
    if not isinstance(sil, list):
        rv = sha256sumd(pdir[sil])
    else:
        hs = ""
        ho = hashlib.sha256()
        for si in sil:
            hs = sha256sumd(pdir[si])
            ho.update(hs)
        rv = ho.hexdigest()
    return rv


def loaddh():
    global dhd
    try:
        dhd = {}
        with open(dhpf, "rb") as fh:
            dhd1 = pickle.load(fh)
            for si in dhd1:
                dhd[si] = dhd1[si]
    except:
        pass


def savedh():
    with open(dhpf, "wb") as fh:
        pickle.dump(dhd, fh)


def dhset(Si, Dh=None):
    if Dh is None:
        Dh = dhstrd(Si)
    dhstrf(Si, Dh)
    savedh()


def dhck(Si):
    Dh1 = dhstrf(Si)
    Dh2 = dhstrd(Si)
    rv = (Dh2, Dh1 != Dh2)
    return rv


loaddh()
