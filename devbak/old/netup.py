#!/data/data/com.termux/files/usr/bin/env python

print("-- netup.py --")

from funcs import srun
from sys import exit

rc = srun(
    'dig @8.8.4.4 +notcp www.google.com 2>&1 | grep -q "status: NOERROR"')
print("netup rc: " + str(rc))
exit(rc)
