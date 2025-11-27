import json
from modulefinder import ModuleFinder

gobn = "inspect/imports1"

finder = ModuleFinder()
finder.run_script("pybackup.py")

moduleslist = {}
for name, mod in finder.modules.items():
    filename = mod.__file__
    if filename is None:
        continue
    if "__" in name:
        continue
    # if "python" in filename.lower():
    #    continue
    moduleslist[name] = mod
    # print '%s: %s' % (name, filename)
    # print ','.join(mod.globalnames.keys()[:3])

print("Loaded modules:")
ml = {}
for name, mod in moduleslist.items():
    if mod.__file__ is not None and "python3" not in mod.__file__:
        ml[name] = sorted(list(mod.globalnames.keys()))

with open(gobn + ".json", "w") as fh:
    json.dump(ml, fh, sort_keys=True, indent=4)
