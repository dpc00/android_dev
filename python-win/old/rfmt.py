#!/data/data/com.termux/files/usr/bin/env python
from subprocess import run
from sys import exit

from config import pdir

print("-- rfmt.py --")

cmd = "yapf -i -r -vv " + str(pdir("python") / "*.py")
print(cmd)
res = run(cmd, shell=True)
exit(res)
