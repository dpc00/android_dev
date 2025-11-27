from os.path import isdir
from subprocess import run, Popen, PIPE

from gb_env import *

print("-- funcs.py --")


def lk(n):
    dir = pre['bkx'] + str(n)
    print(dir)
    if not isdir(dir):
        try:
            from os import mkdir
            mkdir(dir)
            return 0
        except:
            return 1


def unlk(n):
    dir = pre['bkx'] + str(n)
    print(dir)
    if isdir(dir):
        try:
            from os import rmdir
            rmdir(dir)
            return 0
        except:
            return 1


def clr(n2, n1):
    if not bctck(n2, n1) == 0:
        return 0
    print("clearing ct" + str(n2) + " from rtbk" + str(n1))
    return bctclr(n2, n1)


def ts2(t, s):
    n2 = dstts[t][s]
    n1 = srcts[s]
    return n2, n1


def prefn(p, n):
    return pre[p] + str(n)


def dhfn(p):
    return pre['dh'] + '_' + p


def bctck(n2, n1):
    try:
        from os import lstat
        ts1 = lstat(prefn('rtbk', n1)).st_mtime_ns
        ts2 = lstat(prefn('ct', n2)).st_mtime_ns
        if ts1 > ts2:
            return 0
        return 1
    except Exception as e:
        print(e)
        return 2


def bctclr(n2, n1):
    try:
        from os import lstat
        fs1 = lstat(prefn('rtbk', n1))
        from os import utime
        utime(prefn('ct', n2), ns=(fs1.st_atime_ns, fs1.st_mtime_ns))
        return 0
    except Exception as e:
        print(e)
        return 2


def rtset(n1):
    from os import utime
    utime(prefn('rtbk', n1))
    return 0


def sha256sum(d):
    aproc = Popen([
        'ls', '-AgGlR', '--block-size=1', '--time-style=+%s', '--color=never',
        d
    ],
                  stdout=PIPE)
    bproc = Popen(['sha256sum'], stdin=aproc.stdout, stdout=PIPE)
    aproc.stdout.close()
    from os import fsdecode
    return fsdecode(bproc.communicate()[0])


def dhstrd(si):
    return sha256sum(pdir[si])


def dhstrf(si):
    try:
        with open(dhfn(si), 'r') as fh:
            return fh.read()
    except:
        with open(dhfn(si), 'w') as fh:
            fh.write('first write')
            return ''


def dhck(si):
    dh1 = dhstrf(si)
    dh2 = dhstrd(si)
    if dh1 != dh2:
        return 0
    return 1


def dhsv(si):
    return dhfn(si), pdir[si]


def dhmsg(ofn, dir):
    print("updating " + ofn + " from " + dir)


def dhset(si):
    (ofn, dir) = dhsv(si)
    # dhmsg(ofn, dir)
    dh = dhstrd(si)
    with open(ofn, 'w') as fh:
        fh.write(dh)
    return 0


def srun(cmd):
    return run(cmd, shell=True).returncode


def btest():
    for (t, s) in dep():
        (n2, n1) = ts2(t, s)
        res = bctck(n2, n1)
        print(t + ': ct' + str(n1) + ' ' + s + ': rtbk' + str(n2) + ' res: ' +
              str(res))


def depchk(k1, d1):
    dd = 0
    if k1 in d1:
        dd = 1
        d2 = depop[k1]
        for k2 in d2:
            dd += depchk(k2, d1)
    return dd


def ddepth():
    for k1 in depop:
        dd = max(1, depchk(k1, depop))
    return dd
