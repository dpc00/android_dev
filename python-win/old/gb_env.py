from os import getenv

pre = {}
pre["proj"] = "/sdcard/projects"

pre["FLAGS"] = getenv("HOME") + "/.tstamps"
pre["bkx"] = pre["FLAGS"] + "/.bkx"
pre["rtbk"] = pre["FLAGS"] + "/.rtbk"
pre["ct"] = pre["FLAGS"] + "/.ct"
pre["dh"] = pre["FLAGS"] + "/.dh"
pre["bklog"] = pre["FLAGS"] + "/.bklog"

codes = ["blog", "scrdev", "pyth", "scrdev2", "pro", "js", "pytest"]


def code():
    for c in codes:
        yield c


binsrcs = ["scrdev", "pyth", "pro"]


def binsrc():
    for bs in binsrcs:
        yield bs


svcs = ["db", "gd", "od"]


def svc():
    for s in svcs:
        yield s


ops = ["r_scpy", "r_fdbackup", "r_csbackups", "r_gitbackup"]


def op():
    for o in ops:
        yield o


pdir = {}

pdir["fdb"] = "/sdcard/Documents/Finance.db"
pdir["blog"] = pre["proj"] + "/blog"
pdir["scrdev"] = pre["proj"] + "/bash"
pdir["pyth"] = pre["proj"] + "/python"
pdir["scrdev2"] = pre["proj"] + "/bash2"
pdir["pro"] = pre["proj"] + "/prolog"
pdir["js"] = pre["proj"] + "/js"
pdir["pytest"] = pre["proj"] + "/py-test"
pdir["git"] = pre["proj"] + "/.git"

snms = {}
snms["db"] = "DropBox"
snms["gd"] = "GoogleDrive"
snms["od"] = "OneDrive"

srcts = {}
srcts["fdb"] = 1
srcts["git"] = 2
n = 3
for st in codes:
    srcts[st] = n
    n += 1

srcs = []
for s in srcts:
    srcs.append(s)


def src():
    for k in srcs:
        yield k


depop = {}

for i in binsrc():
    depop["bin", i] = "r_scpy"

depop["blog", "fdb"] = "r_fdbackup"

for c in code():
    depop["git", c] = "r_gitbackup"
    depop["zip", c] = "r_mkzip"
for s in svc():
    for c in code():
        depop[s, c] = "r_csbackups"
    depop[s, "docs"] = "r_csbackups"
    depop[s, "zip"] = "r_csbackups"
    depop[s, "refs"] = "r_csbackups"


def dep():
    for t, s in depop:
        yield t, s


dstts = {}
i = 1
for t, s in dep():
    if t not in dstts:
        dstts[t] = {}
    dstts[t][s] = i
    i += 1
