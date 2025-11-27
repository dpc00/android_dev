from modulefinder import ModuleFinder

finder = ModuleFinder()
finder.run_script("pybackup.py")

moduleslist = {}
for name, mod in finder.modules.items():
    filename = mod.__file__
    moduleslist[name] = mod
    # print '%s: %s' % (name, filename)
    # print ','.join(mod.globalnames.keys()[:3])

print("Loaded modules:")
for name, val in sorted(moduleslist.items()):
    print(name)
