import os
from math import floor
from os import walk
from pathlib import Path
from threading import Event, RLock
from typing import TypeAlias


from cscopy import CSCopy
from de import DE, FSe
from edge import Edge, addArc, addDep
from gitclasses import GitIndex, GitRemote, GitRepo, GitWT
from gitops import GitAdd, GitCommit, GitPush
from ldsv import load_all
from localcopy import LocalCopy
from opbase import OpBase
from sd import CS, SD, Ext3, Fat32

quit_ev = Event()
rclk = RLock()

NodeTag: TypeAlias = str
Hash: TypeAlias = bytes
Hdt1: TypeAlias = dict[NodeTag, int]
Hdt2: TypeAlias = dict[Path, FSe]
Hdt3: TypeAlias = dict[NodeTag, Event]

# any/all mostly local directory path(s)
# paths: Dict[NodeTag, Path] = {}


class SetDict(dict):
    paths: dict[NodeTag, SD] = {}

    def __init__(self, *args) -> None:
        super().__init__(*args)

    def add(self, tg: str, sd: SD):
        if not hasattr(sd, "tag"):
            sd.tag = tg
        if tg in self.paths and sd != self.paths[tg]:
            raise ValueError("tag " + tg + " already in paths-dict with different path")
        self[tg] = sd
        self.paths[tg] = sd


pres = SetDict()
srcs = SetDict()
tgts = SetDict()
codes = SetDict()


def ppre(s):
    return pres[s]


def src(s):
    return srcs[s]


def tgt(s):
    return tgts[s]


def cdir(s):
    return codes[s]


def addSrcDir(tg, pth, iscode=False):
    if not isinstance(pth, SD):
        raise ValueError("not an SD subclass")
    srcs.add(tg, pth)
    pth.issrc = True
    if iscode:
        codes.add(tg, pth)
    if pth.isremote:
        RDlls[tg] = None
        RDlls_xt[tg] = 0
        RDhd[tg] = 0
    else:
        LDlls[tg] = None
        LDlls_xt[tg] = 0
        LDhd[tg] = 0
    Dllc[tg] = Event()


def addTgtDir(tg, pth):
    if not isinstance(pth, SD):
        raise ValueError("not an SD subclass")
    tgts.add(tg, pth)
    pth.istgt = True
    if pth.isremote:
        RDlls[tg] = None
        RDlls_xt[tg] = 0
        RDhd[tg] = 0
    else:
        LDlls[tg] = None
        LDlls_xt[tg] = 0
        LDhd[tg] = 0
    Dllc[tg] = Event()


def addPre(tg, frag):
    if not isinstance(frag, SD):
        raise ValueError("not an SD subclass")
    pres.add(tg, frag)
    Dllc[tg] = Event()


# operations (function objects)
opdep: list[OpBase] = []

# dependencies as edge set
eDep: set[Edge] = set()

# dependencies as stored by di,si
edges: dict[tuple[NodeTag, NodeTag], Edge] = {}


# directory lists hashes

LDhd: Hdt1 = {}
RDhd: Hdt1 = {}

Dllc: Hdt3 = {}


# files lists
LDlls: dict[NodeTag, list["DE"]] = {}
RDlls: dict[NodeTag, list["DE"]] = {}

# update times of directory lists
LDlls_xt: dict[NodeTag, float] = {}
RDlls_xt: dict[NodeTag, float] = {}

# pickle file filenames
edgepf: Path | None = None
ldllsf: Path | None = None
rdllsf: Path | None = None

ldhpf: Path | None = None
rdhpf: Path | None = None

# worktree of git repo
worktree: Path | None = None

# directory list hashing stats

sfb: int = 0

# directory list getting stats

dl1_cs = 0
dl2_cs = 0

# hashing stats
h_hits = 0
h_miss = 0

upd_cs = 0

home: Ext3 | None = None
sdcard: Fat32 | None = None
cloud1: CS | None = None
cloud2: CS | None = None
cloud3: CS | None = None
dsbog: Fat32 | None = None


def initConfig():
    global home, sdcard, cloud1, cloud2, cloud3, dsblog
    home = Ext3(os.environ["HOME"], tag="home")
    sdcard = Fat32("/sdcard", tag="sdcard")
    cloud1 = CS("G:", tag="cloud1")
    # cloud2 = CS("OneDrive:", tag="cloud2")
    # cloud3 = CS("DropBox:", tag="cloud3")
    # dsblog = Fat32(os.environ["FDB_PATH"])

    addPre("FLAGS", home)
    # print("FLAGS=" + str(ppre('FLAGS')))

    global edgepf, ldllsf, rdllsf, ldhpf, rdhpf

    edgepf = home / "edges.pp"
    ldllsf = home / "ldlls.pp"
    rdllsf = home / "rdlls.pp"

    ldhpf = home / "ldhd.pp"
    rdhpf = home / "rdhd.pp"
    # print("pf's set now")
    # for pf in [edgepf, ldllsf, rdllsf, ldhpf, rdhpf]:
    #    print(pf.name, str(pf))

    addPre("sd", sdcard)
    addPre("gd", cloud1)
    # addPre("od", cloud2)
    # addPre("db", cloud3)

    addSrcDir("home", home, False)
    addSrcDir("bin", home / "bin", False)
    addSrcDir("sh", home / "bin/sh")
    addSrcDir("proj", sdcard / "projects", False)
    addSrcDir("bash", src("proj") / "bash")
    # addSrcDir("blog", src("proj") / "blog")
    addSrcDir("docs", sdcard / "Documents", False)
    addSrcDir("netspend", sdcard / "Documents" / "netspend", False)
    addSrcDir("directexpress", sdcard / "Documents" / "directexpress", False)
    # addSrcDir("blogds", dsblog, False)
    addSrcDir("backups", sdcard / "backups", False)
    addSrcDir("vids", sdcard / "vids", False)
    addSrcDir("zips", sdcard / "zips", False)
    # addSrcDir(".git", src("proj") / ".git", False)

    def f1():
        dl = getDL(src("proj"))
        for d in dl:
            dn = "proj" + "/" + d.name
            addSrcDir(dn, d, True)
            addDep("git_worktree", dn)
            addDep("zips", dn)
            addDep("proj", dn)

    # f1()

    addDep("git_worktree", "proj")

    global worktree
    worktree = sdcard / "projects"

    ga1 = GitWT(worktree, tag="git_worktree")
    addSrcDir("git_worktree", ga1)

    gc1 = GitIndex(worktree, tag="git_index")
    addSrcDir("git_index", gc1)

    gre1 = GitRepo(worktree, tag="git_repo", rmts=["github"])
    addSrcDir("git_repo", gre1)

    #gre2 = GitRemote(
        #worktree,
        #url="https://www.bitbucket.org/dpchitester/android_dev.git",
        #tag="bitbucket",
        #rmt="bitbucket",
    #)
    #    addTgtDir("bitbucket", gre2)
    
    gre3 = GitRemote(
        worktree,
        url="https://github.com/dpc00/android_dev.git",
        tag="github",
        rmt="github",
    )
    addTgtDir("github", gre3)

    addTgtDir("home", home)
    addTgtDir("bin", home / "bin")
    addTgtDir("sh", home / "bin/sh")
    addTgtDir("pl", home / "bin/pl")
    addTgtDir("backups", sdcard / "backups")
    addTgtDir("termux-backup", tgt("backups") / "termux-backup")
    addTgtDir("zips", sdcard / "zips")
    # addTgtDir("blogds", dsblog)
    # addTgtDir("blog", src("proj") / "blog")
    addTgtDir("bash", src("proj") / "bash")
    addTgtDir("plaid-node", src("proj") / "plaid-node")
    addTgtDir("docs", sdcard / "Documents")
    addTgtDir("blog2", src("proj") / "blog2")
    addTgtDir("blog2netspend", tgt("blog2") / "netspend")
    addTgtDir("blog2directexpress", tgt("blog2") / "directexpress")
    
    npl1 = ("bash", "home")
    op1 = LocalCopy(
        npl1,
        npl1,
        {
            "files": [
                ".termux/*",
                ".bashrc",
                ".bashrc0",
                ".profile",
                #".plaid-cli/**/*",
                #".plaidrc",
                #".git-credentials",
                #".gitconfig",
            ]
        },
    )
    addArc(op1)

    npl1 = ("home", "bash")
    op2 = LocalCopy(
        npl1,
        npl1,
        {
            "files": [
                ".termux/*",
                ".bashrc",
                ".bashrc0",
                ".profile",
                ".config/rclone/*",
                #".plaid-cli/**/*",
                #".plaidrc",
                #".git-credentials",
                # ".gitconfig",
            ]
        },
    )
    addArc(op2)

    #npl1 = ("bin", "bash")
    #op3 = LocalCopy(
        #npl1,
        #npl1,
        #{
            #"files": ["termux-*", "pbu", "ppc", "rbu", "rcu", "qe", "ftp*", "nt"],
            #"exec": True,
        #},
    #)
    #addArc(op3)

    npl1 = ("bash", "bin")
    op4 = LocalCopy(
        npl1,
        npl1,
        {
            "files": ["termux-*", "pbu", "ppc", "rcu", "rbu", "qe", "ftp*", "nt"],
            "exec": False,
        },
    )
    addArc(op4)

    #npl1 = ("sh", "bash")
    #op5 = LocalCopy(npl1, npl1, {"files": ["*.sh", "*.env"], "exec": True})
    #addArc(op5)

    #npl1 = ("bash", "sh")
    #op6 = LocalCopy(npl1, npl1, {"files": ["*.sh", "*.env"], "exec": True})
    #addArc(op6)

    #npl1 = ("blogds", "blog")
    #op7 = LocalCopy(npl1, npl1, {"files": ["blog.js"]})
    #addArc(op7)

    #npl1 = ("blog", "blogds")
    #op8 = LocalCopy(npl1, npl1, {"files": ["*.db", "blog.js"]})
    #addArc(op8)

    #npl1 = ("plaid-node", "blogds")
    #op9 = LocalCopy(npl1, npl1, {"files": ["*.db"]})
    #addArc(op9)

    # npl1 = ('termux-backup', 'home')
    # op1 = LocalCopy(npl1, npl1, {'files': ['**/*.*']})
    # addArc(op1)

    #npl1 = ("backups", "blogds")
    #op10 = LocalCopy(npl1, npl1, {"files": ["*.db"]})
    #addArc(op10)

    npl1 = ("blog2", "docs")
    op11 = LocalCopy(npl1, npl1, {
        "files": ["*.py", "*.csv", "finance.db", "*.txt"]
    })
    addArc(op11)
    
    npl1 = ("blog2netspend", "netspend")
    op12 = LocalCopy(npl1, npl1, {
        "files": ["*.py", "*.csv", "test.db", "*.txt"]
    })
    addArc(op12)
    
    npl1 = ("blog2directexpress", "directexpress")
    op13 = LocalCopy(npl1, npl1, {
        "files": ["*.py", "*.csv", "test.db", "*.txt"]
    })
    addArc(op13)

    if "NOGIT" not in os.environ:
        npl1 = ("git_index", "git_worktree")
        op11 = GitAdd(npl1, npl1, {"wt": worktree})
        addArc(op11)

        npl1 = ("git_repo", "git_index")
        op12 = GitCommit(npl1, npl1, {"wt": worktree})
        addArc(op12)

        # npl1 = ("bitbucket", "git_repo")
        # op13 = GitPush(
            # npl1,
            # None,
            # {"wt": worktree, "rmt": "bitbucket"},
        # )
        # addArc(op13)

        npl1 = ("github", "git_repo")
        op14 = GitPush(
            npl1,
            None,
            {"wt": worktree, "rmt": "github"},
        )
        addArc(op14)

    # for si in codes:
    # npl1 = ("zips", si)
    # op1 = Mkzip(npl1, npl1, {"zipfile": si + ".zip"})
    # addArc(op1)

    # for si in (".git",):
    # npl1 = ("zips", si)
    # op1 = Mkzip(npl1, npl1, {"zipfile": "projects-git.zip"})
    # addArc(op1)

    # for cs in ("gd", "db", "od"):
    for cs in ("gd",):
        for si in ("proj", "vids", "zips",):
            if src(si).is_relative_to(ppre("sd")):
                p1 = src(si).relative_to(ppre("sd"))
            elif src(si).is_relative_to(src("home").parent):
                p1 = src(si).relative_to(src("home").parent)
            else:
                print("relative dir not found")
                raise ValueError()
            addTgtDir(cs + "_" + si, ppre(cs) / p1)
            npl1 = (cs + "_" + si, si)
            # op15 = CSRestore(npl1, None, {})
            # addArc(op15)
            op16 = CSCopy(npl1, npl1, {"delete": False})
            addArc(op16)

    load_all()


dexs = {
    ".cargo",
    ".cache",
    ".git",
    "go",
    "node_modules",
    "__pycache__",
    ".ropeproject",
    ".mypyproject",
    ".mypy_cache",
    ".ruff_cache",
    ".vite",
    ".yarnclean",
    "storage",
    "ldlls.pp",
    "rdlls.pp",
    "rdhd.pp",
    "ldhd.pp",
    "edges.pp",
    "rclone.conf",
}


def cull_DEs(des):
    des[:] = [de for de in des if not any(sd for sd in de.nm.parts if sd in dexs)]


def cull_files(files, pt):
    files[:] = [
        pt(f) for f in files if not any(sd for sd in f.parent.parts if sd in dexs)
    ]


def cull_dirs(dirs, pt):
    dirs[:] = [pt(d) for d in dirs if not isbaddir(pt(d))]


def isbaddir(dir):
    return any(dp for dp in dir.parts if dp in dexs)


def getDL(p):
    pt = type(p)
    # print(str(p))
    fl = []
    try:
        for pth, dirs, _files in walk(p, topdown=True):
            if not isinstance(pth, pt):
                pth = pt(pth)
            cull_dirs(dirs, pt)
            for d in dirs:
                fl.append(pth / d)
            dirs.clear()
        return fl
    except OSError as e:
        print("getDL", e)
        return fl


def ts_trunc2ms(s):
    return floor(s * 1.0e3) / 1.0e3


def ns_trunc2ms(ns):
    return floor(ns / 1.0e6) / 1.0e3


def dllcmp(do, dn):
    dns = set(dn)
    dos = set(do)
    tocopy = dns - dos
    todelete = dos - dns
    return (todelete, tocopy)
