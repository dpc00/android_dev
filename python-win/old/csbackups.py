#!/data/data/com.termux/files/usr/bin/env python

print("-- csbackups.py --")

from sys import exit

from funcs import *


# csname projsubdir
def csb(spn, pjd):
    print(pjd + " -> " + spn)
    res = srun('rclone copy ' + pre['proj'] + '/' + pjd + ' ' + spn +
               ':/projects/' + pjd + ' ' +
               '--exclude ".git/**" --delete-excluded --progress')
    return res


def oneps(dst, src, spn, pjd):
    if not bctck(dst, src) == 0:
        return 0
    print('oneps ' + str(dst) + " " + str(src) + " " + spn + " " + pjd)
    res = csb(spn, pjd)
    if res == 0:
        clr(dst, src)
    return res


def getpdir(si):
    return pdir[si].replace(pre['proj'] + '/', '')


def r_csbackups():
    rc = 0
    res = srun('netup.py')
    if res == 0:
        for t in svc():
            sn = snms[t]
            for s in code():
                dstr = getpdir(s)
                (n2, n1) = ts2(t, s)
                res = oneps(n2, n1, sn, dstr)
                if res != 0:
                    rc += 1
            s = 'git'
            dstr = getpdir(s)
            (n2, n1) = ts2(t, s)
            res = oneps(n2, n1, sn, dstr)
            if res != 0:
                rc += 1
    return rc


def dcsb():
    for t in svc():
        for s in code():
            (n2, n1) = ts2(t, s)
            if bctck(n2, n1) == 0:
                return 0
        (n2, n1) = ts2(t, 'git')
        if bctck(n2, n1) == 0:
            return 0
    return 1


if __name__ == '__main__':
    exit(r_csbackups())
