import pickle
from queue import Empty, SimpleQueue
from threading import RLock
from time import sleep

import config

# from snoop import snoop

dl = RLock()
sev = SimpleQueue()


def pstats():
    print(f"{'dl1_cs':6} {config.dl1_cs:6d}")
    print(f"{'dl2_cs':6} {config.dl2_cs:6d}")
    print(f"{'h_miss':6} {config.h_miss:6d}")
    print(f"{'h_hits':6} {config.h_hits:6d}")
    print(f"{'upd_cs':6} {config.upd_cs:6d}")
    print(f"{'sfb':6} {config.sfb:6d}")


def loadldlls():
    with dl:
        try:
            with open(config.ldllsf, "rb") as fh:
                td = pickle.load(fh)
                LDlls = td["ldlls"]
                LDlls_xt = td["ldlls_xt"]
        except OSError as e:
            print("loadldlls failed", e)
            return
        for si in config.srcs:
            if si in LDlls:
                config.LDlls[si] = LDlls[si]
                config.LDlls_xt[si] = LDlls_xt[si]
        for di in config.tgts:
            if di in LDlls:
                config.LDlls[di] = LDlls[di]
                config.LDlls_xt[di] = LDlls_xt[di]


def loadrdlls():
    with dl:
        try:
            with open(config.rdllsf, "rb") as fh:
                td = pickle.load(fh)
                RDlls = td["rdlls"]
                RDlls_xt = td["rdlls_xt"]
        except OSError as e:
            print("loadrdlls failed", e)
            return
        for si in config.srcs:
            if si in RDlls:
                config.RDlls[si] = RDlls[si]
                config.RDlls_xt[si] = RDlls_xt[si]
        for di in config.tgts:
            if di in RDlls:
                config.RDlls[di] = RDlls[di]
                config.RDlls_xt[di] = RDlls_xt[di]


def saveldlls():
    with dl:
        # print('-saveldlls')
        try:
            with open(config.ldllsf, "wb") as fh:
                td = {"ldlls": config.LDlls, "ldlls_xt": config.LDlls_xt}
                pickle.dump(td, fh)
                config.sfb += fh.tell()
        except OSError as e:
            print("savedlls failed", e)


def saverdlls():
    with dl:
        try:
            with open(config.rdllsf, "wb") as fh:
                td = {"rdlls": config.RDlls, "rdlls_xt": config.RDlls_xt}
                pickle.dump(td, fh)
                config.sfb += fh.tell()
        except OSError as e:
            print("saverdlls failed", e)


def loadedges():
    with dl:
        try:
            with open(config.edgepf, "rb") as fh:
                leDep = pickle.load(fh)
        except OSError as e:
            print("loadedges failed", e)
            return
        for e in config.eDep:
            for le in leDep:
                if le == e:
                    e.ss = le.ss
                    e.ts = le.ts


def saveedges():
    with dl:
        try:
            with open(config.edgepf, "wb") as fh:
                pickle.dump(config.eDep, fh)
                config.sfb += fh.tell()
        except OSError as e:
            print("saveedges failed", e)


def loadldh():
    with dl:
        try:
            with open(config.ldhpf, "rb") as fh:
                config.LDhd = pickle.load(fh)
        except OSError as e:
            print("loadldh failed", e)


def loadrdh():
    with dl:
        try:
            with open(config.rdhpf, "rb") as fh:
                config.RDhd = pickle.load(fh)
        except OSError as e:
            print("loadrdh failed", e)


def saveldh():
    with dl:
        try:
            with open(config.ldhpf, "wb") as fh:
                pickle.dump(config.LDhd, fh)
                config.sfb += fh.tell()
        except OSError as e:
            print("saveldh failed", e)


def saverdh():
    with dl:
        try:
            with open(config.rdhpf, "wb") as fh:
                pickle.dump(config.RDhd, fh)
                config.sfb += fh.tell()
        except OSError as e:
            print("saverdh failed", e)


def load_all():
    loadrdlls()
    # loadldlls()
    loadedges()
    loadldh()
    loadrdh()


def save_all():
    with dl:
        saverdlls()
        # saveldlls()
        saveedges()
        saveldh()
        saverdh()
        pstats()


def save_bp():
    print("-savebp")
    svs = {}
    while True:
        try:
            qi = sev.get_nowait()
            try:
                svs[qi] += 1
            except KeyError:
                svs[qi] = 1
        except Empty:
            if config.quit_ev.is_set():
                break
            else:
                sleep(0.1)
    print("saves:", svs)
    for sv in svs:
        match sv:
            case "edges":
                saveedges()
            case "ldlls":
                saveldlls()
            case "rdlls":
                saverdlls()
            case "ldhd":
                saveldh()
            case "rdhd":
                saverdh()
    pstats()
