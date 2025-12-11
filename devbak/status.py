from bkenv import *
from dhash import *
from tstamp import *
from status import *


def dirty1(T=None):
    yielded = {}
    for Npl, Op in opdep.items():
        for di, si in Npl:
            (N2, N1) = ts2(di, si)
            try:
                if bctck(N2, N1) and (T is None or T == di) and (Op not in yielded):
                    yield Op
                    yielded[Op] = True
            except:
                print(di, si, N2, N1)


def stsupdate(Si, Dh):
    print(Si, end=" ")
    N1 = srcts[Si]
    rtset(N1)
    dhset(Si, Dh)


def onestatus(Si):
    (Dh, changed) = dhck(Si)
    if changed:
        stsupdate(Si, Dh)


def statuses():
    SDl = []
    for Si in srcs:
        (Dh, changed) = dhck(Si)
        if changed:
            SDl.append((Si, Dh))
    return SDl


def statuses():
    SDl = []
    for Si in srcs:
        (Dh, changed) = dhck(Si)
        if changed:
            SDl.append((Si, Dh))
    return SDl


def updatets(N):
    print("Status", N)
    Sl = statuses()
    if len(Sl):
        print("changed: ", end="")
        for Si, Dh in Sl:
            stsupdate(Si, Dh)
        print()


if __name__ == "__main__":
    updatets(1)
    for i in dirty1():
        print(i)
