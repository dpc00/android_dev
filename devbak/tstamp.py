import time
import pickle

from bkenv import *

tsd = None
tspf = pre["FLAGS"] / "tsd.pp"


def tstime(pre, n, ft=None):
    global tsd
    if (pre, n) not in tsd:
        tsd[pre, n] = time.time()
        # print(pre, n, 'not found, injecting current time')
    oft = tsd[pre, n]
    if ft is not None:
        tsd[pre, n] = ft
    return oft


def n2ts(n2, n1):
    for t, s in dstts:
        if n2 == dstts[t, s]:
            if n1 == srcts[s]:
                return (t, s)


def clr(n2, n1):
    global tsd
    t1 = tstime("rtbk", n1)
    t2 = tstime("ct", n2)
    if t1 != t2:
        t, s = n2ts(n2, n1)
        print("-clr", n2, n1, t, s)
        tstime("ct", n2, t1)
        savets()
    return True


def loadts():
    global tsd
    try:
        tsd = {}
        with open(tspf, "rb") as fh:
            tsd1 = pickle.load(fh)
            for pre, n in tsd1:
                tstime(pre, n, tsd1[pre, n])
    except:
        tsd = {}


def savets():
    with open(tspf, "wb") as fh:
        pickle.dump(tsd, fh)


def bctck(N2, N1):
    Ft1 = tstime("rtbk", N1)
    Ft2 = tstime("ct", N2)
    return Ft1 > Ft2


def ts2(T, S):
    N2 = dstts[T, S]
    N1 = srcts[S]
    # print(T, S, N2, N1)
    return (N2, N1)


def rtset(N=None, Mt=None):
    if N is None:
        for k, N1 in srcts.items():
            rtset(N1)
        return
    else:
        if Mt is None:
            tstime("rtbk", N, time.time())
            savets()
        else:
            tstime("rtbk", N, Mt)
            savets()


loadts()

if __name__ == "__main__":
    print(repr(tsd))
