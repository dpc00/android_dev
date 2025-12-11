#!/data/data/com.termux/files/usr/bin/python

from rope.base.project import Project
from rope.contrib.findit import find_occurrences
from rope.refactor.rename import Rename

f1 = "gitops.py"
f2 = "dirlist"

proj = Project(".")
mod1 = proj.get_resource(f1)
# mod2 = proj.get_resource(f2)

idx = None
idx = mod1.read().index("gitck3", 0)
print(idx)

rv = find_occurrences(proj, mod1, idx)

for i in rv:
    print(i.resource.name, i.region)

changes = Rename(proj, mod1, idx).get_changes("gitremoteck")

# changes = create_move(proj, mod1, idx).get_changes(mod2)
print(changes.get_description())

proj.do(changes)

proj.close()
