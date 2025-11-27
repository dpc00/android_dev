import pickle
import json

from config import *
from dirlist import *
from bhash import bhash
import asyncrun
import config

ldhd = None
ldhpf = pre('FLAGS') / 'ldhd.pp'

rdhd = None
rdhpf = pre('FLAGS') / 'rdhd.pp'

def ldh_f(si, dh=None):
    global ldhd
    if si not in ldhd:
        ldhd[si] = None
    odh = ldhd[si]
    if dh is not None:
        ldhd[si] = dh
    return odh


def rdh_f(di, dh=None):
    global rdhd
    if di not in rdhd:
        rdhd[di] = None
    odh = rdhd[di]
    if dh is not None:
        rdhd[di] = dh
    return odh


async def ldh_d(si):
    st1 = await ldlld(si)
    return bhash(st1)


async def rdh_d(di):
    st1 = await rdlld(di)
    if st1 is not None:
        return bhash(st1)
    return None


def loadldh():
    global ldhd
    try:
        ldhd = {}
        with open(ldhpf, "rb") as fh:
            ldhd = pickle.load(fh)
    except:
        pass


def loadrdh():
    global rdhd
    try:
        rdhd = {}
        with open(rdhpf, "rb") as fh:
            rdhd = pickle.load(fh)
    except:
        pass


def saveldh():
    with open(ldhpf, "wb") as fh:
        pickle.dump(ldhd, fh)


def saverdh():
    with open(rdhpf, "wb") as fh:
        pickle.dump(rdhd, fh)


async def ldhset(Si, Dh=None):
    if Dh is None:
        Dh = await ldh_d(Si)
    ldh_f(Si, Dh)
    saveldh()


async def rdhset(Di, Dh=None):
    if Dh is None:
        Dh = await rdh_d(Di)
    if Dh is not None:
        rdh_f(Di, Dh)
        saverdh()


async def ldhck(Si):
    Dh1 = ldh_f(Si)
    Dh2 = await ldh_d(Si)
    rv = (Dh2, Dh1 != Dh2)
    return rv


async def rdhck(Di):
    Dh1 = rdh_f(Di)
    Dh2 = await rdh_d(Di)
    if Dh2 is not None:
        return (Dh2, Dh1 != Dh2)
    return (None, False)


loadldh()
loadrdh()

if __name__ == '__main__':
    ldhd = {}
    for si in srcs:
        asyncio.run(ldhset(si))
    saveldh()
    for di in tdirs:
        if di.startswith('gd_'):
            asyncio.run(rdhset(di))
    saverdh()
