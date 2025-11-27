#!/data/data/com.termux/files/usr/bin/env python
print("-- fdbackup.py --")

from funcs import *
from gb_env import *
from sys import exit


def r_fdb2(n2, n1):
    if not bctck(n2, n1) == 0:
        return 0
    res = srun('cp -u -p ' + pdir['fdb'] + ' ' + pdir['blog'] + '/dist')
    if res == 0:
        res = bctclr(n2, n1)
    return res


def r_fdbackup():
    (n2, n1) = ts2('blog', 'fdb')
    return r_fdb2(n2, n1)


if __name__ == '__main__':
    exit(r_fdbackup())
