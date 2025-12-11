from tokenize import tokenize
import os
import sys
import json
import token
from keyword import iskeyword

from collections import defaultdict


class Ni:
    def __init__(self):
        self.lns = defaultdict(list)
        self.cnt = 0


tf = defaultdict(Ni)

for fn in sys.argv[1:]:
    print(fn)
    with open(fn, "rb") as fh:
        for tok in tokenize(fh.readline):
            if not (tok.type == token.NAME):
                continue
            if not iskeyword(tok.string):
                tf[tok.string].cnt += 1
                tf[tok.string].lns[fn].append(tok.start[0])


def dumptf(tf):
    l = []
    tfl = list(tf.items())
    tfl.sort(key=lambda i: i[0], reverse=False)
    for k, v in tfl:
        s1 = "{:13} {:4}: ".format(k, v.cnt)
        for fn in v.lns:
            s1 += "{} ".format(fn)
        l.append(s1)
    for tp in l:
        fh.write(tp)
        fh.write("\n")


with open("index.tf", "w") as fh:
    dumptf(tf)
