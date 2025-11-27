import sys
import token
from collections import defaultdict
from keyword import iskeyword
from tokenize import tokenize


class _Ni:
    def __init__(self):
        self.lns = defaultdict(list)
        self.cnt = 0
        self.isdef = False
        self.deffn = set()


TF = defaultdict(_Ni)

for fn in sys.argv[1:]:
    print(fn)
    with open(fn, "rb") as fh:
        for tok in tokenize(fh.readline):
            if tok.type != token.NAME:
                continue

            if iskeyword(tok.string):
                continue

            cn = TF[tok.string]
            cn.cnt += 1
            if tok.type == token.NAME and tok.string == "def":
                cn.isdef = True
                cn.deffn.add(fn)
            cn.lns[fn].append(tok.start[0])


def _dumptf(tf):
    l = []
    tfl = list(tf.items())
    tfl.sort(key=lambda i: i[0].lower(), reverse=False)
    for k, v in tfl:
        if v.isdef:
            s1 = "*"
        else:
            s1 = " "
        s1 += "{:13} {:4}: ".format(k, v.cnt)
        for fn in v.lns:
            s1 += "{}".format(fn)
            if v.isdef and fn in v.deffn:
                s1 += "*"
            s1 += " "
        l.append(s1)
    for tp in l:
        fh.write(tp)
        fh.write("\n")


with open("index.tf", "w") as fh:
    _dumptf(TF)
