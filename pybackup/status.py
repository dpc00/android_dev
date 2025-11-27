import config
import ldsv as ls

def stsupdate(Si, Dh):
    # print(Si, end=' ')
    print(Si, end=" ")
    # N1 = srcts[Si]
    for e in [e for e in config.eDep if e.si == Si]:
        e.rtset()
    config.src(Si).sdhset(Dh)


def onestatus(Si):
    # TODO: update as per src_statuses
    tr = config.src(Si).sdhck()
    if tr is not None:
        (Dh, changed) = tr
        if changed:
            stsupdate(Si, Dh)
            print()


def src_statuses():
    SDl = []
    for Si in config.srcs:
        # print('calling lckers', Si)
        tr = config.src(Si).sdhck()
        if tr is not None:
            (Dh, changed) = tr
            if changed:
                SDl.append((Si, Dh))
    return SDl

def src_statuses2():
    import concurrent.futures as cf
    tpe = cf.ThreadPoolExecutor(max_workers=4)
    SDl = []
    def f1(Si):
        # print('calling lckers', Si)
        tr = config.src(Si).sdhck()
        if tr is not None:
            (Dh, changed) = tr
            if changed:
                SDl.append((Si, Dh))
    for Si in config.srcs:
        tpe.submit(f1, Si)
    tpe.shutdown()
    return SDl


def updatets(N):
    print("Status", N)
    Sl = src_statuses2()
    if len(Sl):
        print("changed: ", end="")
        for rv in Sl:
            (Si, Dh) = rv
            stsupdate(Si, Dh)
        print()


