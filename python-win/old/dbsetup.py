import parser

from opclasses import *
from pyswip import Prolog, Functor, Variable, Query

import config as e

pl = Prolog()
pl.consult("/sdcard/projects/prolog/main.pl")

Opp = Variable()
Di = Variable()
Si = Variable()
Dd = Variable()
Sd = Variable()
OptL = Variable()
X = Variable()
Y = Variable()
Z = Variable()

opdep = Functor("opdep", arity=6)
svcs = Functor("svcs", arity=1)
pre = Functor("pre", arity=2)
pdir = Functor("pdir", arity=2)
tdir = Functor("tdir", arity=2)
srcts = Functor("srcts", arity=2)
dstts = Functor("dstts", arity=3)
snm = Functor("snm", arity=2)
codes = Functor("codes", arity=1)
srcs = Functor("srcs", arity=1)
worktree = Functor("worktree", 1)
dep = Functor("dep", 2)

fh = open('bkenv.py', 'w')
fh.write('from opclasses import *\n')
fh.write('from scopy import Scopy')
fh.write('from gitbackup import Gitbackup')
fh.write('from csbackup import Csbackup')

fh.write("\n\nsvcs = ")
qr = Query(svcs(X))
while qr.nextSolution():
    x = X.value
    x = [str(y.value) for y in x]
    fh.write(str(x) + '\n')
qr.closeQuery()

fh.write("\nsnm = {}\n")
qr = Query(snm(X, Y))
while qr.nextSolution():
    x = X.value
    y = Y.value
    x = str(x)
    y = str(y.decode())
    fh.write('snm[' + repr(x) + '] = ' + repr(y) + '\n')
qr.closeQuery()


def cksubst(s1, dl, td):
    #return repr(s1)
    for (sd, sdn) in dl:
        for rs in sd:
            if sd[rs] in s1 and not (sd == td and len(sd[rs]) == len(s1)):
                s2 = s1.replace(sd[rs], '')
                s3 = sdn + '[' + repr(rs) + '] + ' + repr(s2)
                print(s1, s2, s3)
                return s3
    return repr(s1)


fh.write("\npre = {}\n")
qr = Query(pre(X, Y))
while qr.nextSolution():
    x = X.value
    y = Y.value
    x = str(x)
    y = str(y.decode())
    y = cksubst(y, [(e.pre, 'pre')], e.pre)
    #y = repr(y)
    fh.write('pre[' + repr(x) + '] = ' + y + '\n')
qr.closeQuery()

fh.write("\npdir = {}\n")
qr = Query(pdir(X, Y))
while qr.nextSolution():
    x = X.value
    y = Y.value
    x = str(x)
    y = str(y.decode())
    y = cksubst(y, [(e.pdir, 'pdir'), (e.pre, 'pre')], e.pdir)
    #y = repr(y)
    fh.write('pdir[' + repr(x) + '] = ' + y + '\n')
qr.closeQuery()

fh.write("\ntdir = {}\n")
qr = Query(tdir(X, Y))
while qr.nextSolution():
    x = X.value
    y = Y.value
    x = str(x)
    try:
        y = str(y.decode())
    except:
        y = str(y)
        pass
    y = cksubst(y, [(e.tdir, 'tdir'), (e.pdir, 'pdir'), (e.pre, 'pre')],
                e.tdir)
    #y = repr(y)
    fh.write('tdir[' + repr(x) + '] = ' + y + '\n')
qr.closeQuery()

fh.write("\ncodes = ")
qr = Query(codes(X))
while qr.nextSolution():
    x = X.value
    x = [str(y.value) for y in x]
    fh.write(str(x) + '\n')
qr.closeQuery()

fh.write("\nsrcs = ")
qr = Query(srcs(X))
while qr.nextSolution():
    x = X.value
    x = [str(y.value) for y in x]
    fh.write(str(x) + '\n')
qr.closeQuery()

fh.write("\nworktree = ")
qr = Query(worktree(X))
while qr.nextSolution():
    x = X.value
    x = x.decode()
    fh.write(repr(x) + '\n')
qr.closeQuery()

fh.write("\nopdep = {}\n")


def dictwrite1(fh, var, dct):
    fh.write(var)
    fh.write('[')
    fh.write(repr(dct['di']))
    fh.write(',')
    fh.write(repr(dct['si']))
    fh.write('] = ')
    fh.write(dct['op'])
    fh.write('(')

    nf = False
    for k, v in dct.items():
        if k == 'op':
            continue
        if nf:
            fh.write(',')
        else:
            nf = True
        if isinstance(v, str):
            fh.write('"')
            fh.write(v)
            fh.write('"')
        else:
            fh.write(repr(v))
    fh.write(')')
    fh.write('\n')


qr = Query(opdep(Opp, Di, Si, Dd, Sd, OptL))
while qr.nextSolution():

    def decodeit(It):
        return str(It.decode())

    row = {}
    s = str(Opp.value)
    row["op"] = s[0].upper() + s[1:]
    if row["op"] == "Scpy":
        row["op"] = "Scopy"
    row["di"] = tuple(str(i) for i in Di.value)
    row["si"] = tuple(str(i) for i in Si.value)
    row["dd"] = tuple(str(i) for i in Dd.value)
    row["sd"] = tuple(str(i) for i in Sd.value)
    od = {}
    l = OptL.value

    def f1(Fl):
        Fl = list(map(decodeit, Fl))
        return {"files": Fl}

    def f2(p):
        return {"exec": True}

    def f3(p):
        return {"wt": str(p.decode())}

    def f4(p):
        return {"add": True}

    def f5(p):
        return {"commit": True}

    def f6(p):
        return {"push": True}

    def f7(Rmt):
        return {"rmt": Rmt.decode()}

    def f8(p):
        return {"zipfile": str(p.decode())}

    def f9(p):
        return {"sname": [str(i.decode()) for i in p]}

    for f in l:
        st = parser.expr(str(f))
        c = st.compile()
        o = eval(
            c, globals(), {
                "files": f1,
                "exec": f2,
                "wt": f3,
                "add": f4,
                "commit": f5,
                "push": f6,
                "rmt": f7,
                "local": b"local",
                "bitbucket": b"bitbucket",
                "zipfile": f8,
                "sname": f9,
                "true": "True",
                "false": "False"
            })
        od.update(o)
    row['opts'] = od
    for k, v in od.items():
        if k == "files":
            for gls in v:
                pass
        else:
            pass
    dictwrite1(fh, 'opdep', row)
qr.closeQuery()

fh.write("\ndep = set()\n")
qr = Query(dep(X, Y))
while qr.nextSolution():
    x = X.value
    y = Y.value
    fh.write('dep.add((' + repr(str(x)) + ',' + repr(str(y)) + '))\n')
qr.closeQuery()

fh.write("\nsrcts = {}\n")
qr = Query(srcts(X, Y))
while qr.nextSolution():
    x = X.value
    y = Y.value
    x = str(x)
    fh.write('srcts[' + repr(x) + '] = ' + str(y) + '\n')
qr.closeQuery()

fh.write("\ndstts = {}\n")
qr = Query(dstts(X, Y, Z))
while qr.nextSolution():
    x = X.value
    y = Y.value
    z = Z.value
    x = str(x)
    y = str(y)
    fh.write('dstts[' + repr(x) + ',' + repr(y) + '] = ' + str(z) + '\n')
qr.closeQuery()

fh.close()
