import asyncio

from config import opdep, srcs, tgts, lckers, rckers
from csrestore import CSRestore
from edge import findEdge, dep
from gitops import GitOps
from statushash import ldhset, rdhset


def changed_ops(T=None):
    rv = []
    for Op in opdep:
        di, si = Op.npl1
        if T is None or T == di:
            cf = False
            e = findEdge(di, si)
            if type(Op) == GitOps:
                cf |= e.bctck() or e.rbctck()
            elif type(Op) == CSRestore:
                cf |= e.bctck() or e.rbctck()
            else:
                cf |= e.bctck()
            if cf:
                rv.append(Op)
                break
    return rv


async def stsupdate(Si, Dh):
    # print(Si, end=' ')
    print(Si, end=" ")
    # N1 = srcts[Si]
    for e in dep:
        if e.si == Si:
            e.rtset()
    await ldhset(Si, Dh)


async def rstsupdate(Di, Dh):
    # print(Si, end=' ')
    print(Di, end=" ")
    # N1 = srcts[Si]
    for e in dep:
        if e.di == Di:
            e.rrtset()
    await rdhset(Di, Dh)


async def onestatus(Si):
    # TODO: update as per statuses
    (Dh, changed) = await lckers[Si]()
    if changed:
        await stsupdate(Si, Dh)
        print()


async def ronestatus(Di):
    # TODO: update as per rstatuses
    (Dh, changed) = await rckers[Di]()
    if changed:
        await rstsupdate(Di, Dh)
        print()


async def statuses():
    SDl = []
    for Si in srcs:
        # print('calling lckers', Si)
        (Dh, changed) = await lckers[Si]()
        if changed:
            SDl.append((Si, Dh))
    return SDl


async def rstatuses():
    SDl = []
    for Di in tgts:
        if Di.startswith("gd_") or Di == "bitbucket":
            (Dh, changed) = await rckers[Di]()
            if changed:
                SDl.append((Di, Dh))
            return SDl


async def updatets(N):
    print("Status", N)
    Sl = await statuses()
    if Sl:
        print("changed: ", end="")
        for Si, Dh in Sl:
            await stsupdate(Si, Dh)
        print()


async def rupdatets(N):
    print("RStatus", N)
    Dl = await rstatuses()
    if Dl:
        print("rchanged: ", end="")
        for Di, Dh in Dl:
            await rstsupdate(Di, Dh)
        print()


if __name__ == "__main__":
    from dirlist import saveldlls, saverdlls
    from fmd5h import savefmd5h

    asyncio.run(updatets(1))
    asyncio.run(rupdatets(1))
    print(changed_ops())
    savefmd5h()
    saveldlls()
    saverdlls()
