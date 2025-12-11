import config
from edge import Edge, findEdge
from opbase import OpBase
from status import updatets
from toposort2 import topological_sort

_pass = 1


def changed_ops(T=None) -> list[OpBase]:
    rv: list[OpBase] = []
    for Op in config.opdep:
        di, si = Op.npl1
        if T is None or di == T:
            e: Edge = findEdge(di, si)
            if Op.ischanged(e):
                rv.append(Op)
    return rv


def incp():
    global _pass
    i = _pass
    _pass += 1
    return i


def clean():
    res = len(changed_ops()) == 0
    if res:
        print("clean")
    return res


def nodeps(T):
    return not any(e.si == T for e in config.eDep)


def istgt(T, dep2=None):
    if dep2 is None:
        dep2 = config.eDep
    return any(e.di == T for e in dep2)


def nts():
    print("-nts")
    p1 = topological_sort(config.eDep)
    ts = [t for elem in p1 for t in elem]
    ts = [d for d in ts if istgt(d)]
    ts.reverse()
    return ts


n = 1


def proc_nodes(L):
    import concurrent.futures as cf

    global n
    tpe = cf.ThreadPoolExecutor(max_workers=4)

    def f1(op):
        global n
        sc, fc = op()
        updatets(n)
        n += 1

    for node in L:
        # print("node:", node)
        ss = changed_ops(node)
        for op in ss:
            if nodeps(op.npl1[0]):
                tpe.submit(f1, op)
                # f1(op)
            else:
                f1(op)
    tpe.shutdown()
    updatets(n)
    n += 1


def opExec():
    print("-opexec")
    g1 = nts()
    incp()
    return proc_nodes(g1)


if __name__ == "__main__":
    config.initConfig()
    print(opExec())
