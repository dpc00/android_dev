#!/data/data/com.termux/files/usr/bin/env python

print("-- scpy.py --")

from glob import glob
from os import getenv, lstat, mkdir
from os.path import exists
from sys import exit

from funcs import srun, ts2, bctck, clr
from gb_env import pdir, binsrc

st = getenv("HOME") + "/bin"


def hcpy(hcl, si):
    for fn in hcl:
        srun("cp -u -p " + pdir[si] + "/" + fn + " " + getenv("HOME"))
    srun("cp -u -r -p " + pdir[si] + "/.termux " + getenv("HOME"))


def sc(exl, si, st):
    for ex in exl:
        if not exists(st):
            mkdir(st)
        gl1 = glob(pdir[si] + "/*" + ex)
        if len(gl1) > 0:
            srun("cp -u " + " ".join(gl1) + " " + st)
        gl2 = glob(st + "/*" + ex)
        if len(gl2) > 0:
            srun("chmod +x " + " ".join(gl2))


def scpy():
    if not exists(st):
        mkdir(st)
    hcl = [".bashrc", ".bashrc", ".profile", ".swiplrc"]
    hcpy(hcl, "scrdev")
    sc([".sh", ".env"], "scrdev", st + "/sh")
    sc([".py"], "pyth", st + "/py")
    sc([".pl"], "pro", st + "/pl")
    sc([".js"], "js", st + "/js")
    for bfn in [st + "/sh/termux-url-opener", st + "/sh/termux-file-editor"]:
        fe1 = exists(bfn + ".sh")
        fe2 = exists(bfn)
        fo = False
        if fe2:
            ts2 = lstat(bfn).st_mtime_ns
            if fe1:
                ts1 = lstat(bfn + ".sh").st_mtime_ns
                fo = ts1 > ts2
        if (not fe2) or fo:
            if fe2:
                srun("rm " + bfn)
            srun("mv " + bfn + ".sh " + bfn)
        else:
            if fe1:
                srun("rm " + bfn + ".sh")
        srun("mv " + bfn + " " + bfn.replace("/sh", ""))
    return 0


def dscf():
    for si in binsrc():
        (n2, n1) = ts2("bin", si)
        if bctck(n2, n1) == 0:
            return 0
    return 1


def scbc():
    fres = 0
    for si in binsrc():
        (n2, n1) = ts2("bin", si)
        res = clr(n2, n1)
        if res != 0:
            fres += 1
    return fres


def r_scpy():
    # if not dscf() == 0:
    #   return 0
    res = scpy()
    # if res == 0:
    # res = scbc()
    return res


if __name__ == "__main__":
    exit(r_scpy())
