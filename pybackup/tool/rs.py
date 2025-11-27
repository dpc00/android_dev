import math
import pathlib as pl
import random
import subprocess as sp

p = pl.Path(".")

fl = p.glob("*.py")
fl = list(fl)

i = math.floor(random.random() * len(fl))

fn = fl[i].name

# print(fl)
print(fn)
print()

sp.run(["python", "tool/md.py", fn])
