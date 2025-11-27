from pathlib import Path
from functools import partial

def pre(s):
    from config import pres, paths
    if s in pres:
        return paths[s]


def pdir(s):
    from config import pdirs, paths
    if s in pdirs:
        return paths[s]


def tdir(s):
    from config import tdirs, paths
    if s in tdirs:
        return paths[s]


def src(s):
    from config import srcs, paths
    if s in srcs:
        return paths[s]


def tgt(s):
    from config import tgts, paths
    if t in tgts:
        return paths[t]


def code(s):
    from config import codes, paths
    if s in codes:
        return paths[s]

def addDep(j, i):
    from edge import Edge, dep
    e = Edge(j, i)
    if e not in dep:
        dep.add(e)


def addArc(op1):
    from edge import Edge, dep
    from config import opdep
    if op1 not in opdep:
        opdep.append(op1)
    j, i = op1.npl1
    e = Edge(j, i)
    if e not in dep:
        dep.add(e)


def addTgtDir(tg, pth):
    from config import paths, tgts, tdirs, rckers
    from statushash import rdhck
    if not isinstance(pth, Path):
        pth = Path(pth)
    if tg in paths and paths[tg] != pth:
        raise Exception('path tag collision', tg, pth, paths[tg])
    paths[tg] = pth
    tgts.add(tg)
    rckers[tg] = partial(rdhck, tg)
    tdirs.add(tg)


def addSrcDir(tg, pth, iscode=False):
    from config import paths, pdirs, srcs, codes, lckers
    from statushash import ldhck
    global ni1
    if not isinstance(pth, Path):
        pth = Path(pth)
    if tg in paths and paths[tg] != pth:
        raise Exception('path tag collision', tg, pth, paths[tg])
    paths[tg] = pth
    pdirs.add(tg)
    srcs.add(tg)
    lckers[tg] = partial(ldhck, tg)
    if iscode:
        codes.add(tg)


def addPathPrefix(tg, frag):
    from config import paths, pres
    if not isinstance(frag, Path):
        frag = Path(frag)
    if tg in paths and paths[tg] != frag:
        raise Exception('path tag collision', tg, pth, paths[tg])
    paths[tg] = frag
    pres.add(tg)
