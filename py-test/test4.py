
from Dir import *

print(repr(drives))

dl = findDL('CODE0')
d = findDrive(dl)

print(repr(d.serialnumber))

print(dbHash(d))