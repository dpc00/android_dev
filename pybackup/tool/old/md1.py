from pathlib import Path

import pygraphviz

import asyncrun as ar

gobn = "inspect/md1"

graph = pygraphviz.AGraph(strict=False, directed=True)

p = Path.cwd()

for pf in p.glob("*.py"):
    source = pf.stem
    cmd = f"python -m import_deps {p / pf}"
    print(cmd)
    ar.run1(cmd)
    deps = ar.txt.splitlines()
    print(deps)
    for dep in deps:
        print(source, dep)
        sink = dep.strip()
        if sink:
            graph.add_edge(source, sink)

graph.write(gobn + ".gv")
# cmd='dot -Tsvg -Kfdp -o '+gobn+'.svg '+gobn+'.gv'
# ar.run1(cmd)
