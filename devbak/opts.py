from bkenv import *
from status import *
from toposort import topological_sort
import asyncio

_pass = 1


def incp():
    global _pass
    i = _pass
    _pass += 1
    return i


def clean():
    res = len(list(dirty1())) == 0
    if res:
        print("clean")
    return res


def nodeps(T):
    # print('-nodeps')
    for T1, S1 in dep:
        if S1 == T:
            return False
    return True


def istgt(T):
    # print('-istgt')
    for T1, S1 in dep:
        if T1 == T:
            return True
    return False


def nts():
    print("-nts")
    p1 = topological_sort(dep)
    ts = [t for elem in p1 for t in elem]
    return [d for d in ts if istgt(d)]


running = set()


async def gproc3(L):
    print("-gproc3-", end="")
    if L[1] not in running:
        print(L[0], L[1])
        running.add(L[1])
        if nodeps(L[0]):

            async def f1(L):
                try:
                    L[2] = await L[1]()
                    running.remove(L[1])
                except Exception as e:
                    print(e)

            tsk = asyncio.create_task(f1(L))
        else:
            try:
                L[2] = await L[1]()
                running.remove(L[1])
            except Exception as e:
                print(e)

    # else:
    # print(Op, 'already running')


async def gproc2(T):
    # print('-gproc2')
    # print(T)
    L1 = list(dirty1(T))
    if len(L1) == 0:
        return True
    L2 = [[T, Op, (0, 0)] for Op in L1]
    for li in L2:
        await gproc3(li)
    L3 = [R for (T, Op, R) in L2 if R[1]]
    return len(L3) == 0


async def gproc(L):
    # print('-gproc')
    for T in L:
        if not await gproc2(T):
            return False
    return True


async def opexec():
    print("opexec")
    ic = 0
    G1 = nts()
    print(G1)
    p1 = incp()
    # updatets(p1)
    while True:
        if await gproc(G1):
            if clean():
                return True
            else:
                return False
        else:
            return False


if __name__ == "__main__":
    updatets(0)
    print(asyncio.run(opexec()))
