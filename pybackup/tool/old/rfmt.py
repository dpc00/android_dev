#!/data/data/com.termux/files/usr/bin/env python
from pathlib import Path
from subprocess import run
from sys import exit

print("-- rfmt.py --")

cmd = "black -t py311 *.py"
print(cmd)
res = run(cmd, shell=True)
exit(res)
