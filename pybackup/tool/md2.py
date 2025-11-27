from bisect import insort_right
from pathlib import Path

from module_dependencies import Source

import asyncrun as ar

# This creates a Source instance for this file itself


gobn = "inspect/md2"


p = Path.cwd()


class graph(dict):
    def add_edge(self, i1, i2):
        if i1 not in self:
            self[i1] = []
        insort_right(self[i1], i2)

    def write(self, fn):
        with open(fn, "w") as fh:
            fh.write("digraph md2 {\n")
            for n1 in sorted(self.keys()):
                fh.write('    "' + n1 + '" -> {')
                first = True
                for n2 in self[n1]:
                    if first:
                        fh.write('"' + n2 + '"')
                        first = False
                    else:
                        fh.write(', "' + n2 + '"')
                fh.write("}\n")
            fh.write("}\n")


g = graph()

for pf in p.glob("*.py"):
    src = Source.from_file(pf.name)
    source = pf.stem
    deps = src.imports()
    for dep in deps:
        sink = dep.strip()
        if sink:
            g.add_edge(source, sink)

g.write(gobn + ".gv")

cmd = "dot -Tsvg -Kfdp -o " + gobn + ".svg " + gobn + ".gv"
ar.run1(cmd)
