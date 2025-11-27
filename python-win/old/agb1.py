#!/data/data/com.termux/files/usr/bin/env python
print("-- agb1.py --")

from sys import modules

from csbackups import *


def statuses():
    def f1(si):
        rc = dhck(si)
        if rc == 0:
            with open(pre['bklog'], "a") as fh:
                fh.write(si + " changed\n")
            return True
        return False

    return [si for si in srcs if f1(si)]


def stsupdate(sr):
    print(sr, end=' ')
    n1 = srcts[sr]
    dhset(sr)
    rtset(n1)


def mdp(l2):
    for sr in l2:
        stsupdate(sr)


def updatets(n):
    sl = statuses()
    print("Status", str(n), sl, end=' ')
    if len(sl):
        print("changed:", end=' ')
        mdp(sl)
    print()


def dirty1():
    for t in depop:
        for s in depop[t]:
            op = depop[t][s]
            (n2, n1) = ts2(t, s)
            res = bctck(n2, n1)
            if res == 0:
                yield t, s, op


def dirty2():
    for (t, s, op) in dirty1():
        yield op


def oplst():
    ol = []
    for op in dirty2():
        if not op in ol:
            ol.append(op)
    return ol


jj = 0


def doops(opl):
    global jj
    for op in opl:
        print('call', op)
        getattr(modules[__name__], op)()


def main():
    global jj
    for i in range(1, 1 + ddepth()):
        jj += 1
        updatets(jj)
        l1 = oplst()
        doops(l1)


if __name__ == '__main__':
    res = main()
    print("agb1.py rc: " + str(res))
    exit(res)
