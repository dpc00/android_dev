#!/data/data/com.termux/files/usr/bin/env python
from sys import exit
from bkenv import pdir
from subprocess import run
print("-- rfmt.py --")

cmd = 'yapf -i -r -vv ' + \
    str(pdir['pyth']) + '/*.py'
print(cmd)
res = run(cmd, shell=True)
exit(res)
