from config import *
from status import *
from toposort import topological_sort
import asyncio
from netup import netup

_pass = 1

tsks = []


def incp():
    global _pass
    i = _pass
    _pass += 1
    return i


async def clean():
    res = len(changed_ops()) == 0
    if res:
        print('clean')
    return res


def nodeps(T):
    # print('-nodeps')
    for e in dep:
        if e.si == T:
            return False
    return True


def istgt(T, dep=dep):
    # print('-istgt')
    for e in dep:
        if e.di == T:
            return True
    return False


def nts():
    print('-nts')
    p1 = topological_sort(dep)
    ts = [t for elem in p1 for t in elem]
    ts = [d for d in ts if istgt(d)]
    ts.reverse()
    return ts


async def proc_nodes(L):
    # print('-gproc')
    n = 1
    for node in L:
        print('node', node)
        srcs = changed_ops(node)
        for op in srcs:
            tc, fc = await op()
            if tc:
                await updatets(n)
                await rupdatets(n)
                n += 1
    return True


async def opexec():
    print('-opexec')
    ic = 0
    G1 = nts()

    # print(G1)
    p1 = incp()

    if await proc_nodes(G1):
        if await clean():
            return True
    else:
        False


if __name__ == '__main__':

    async def f1():
        print(await opexec())

    asyncio.run(f1())
