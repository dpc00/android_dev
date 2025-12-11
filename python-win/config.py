import json
import os

from cscopy import CSCopy
from gitops import GitOps
from localcopy import LocalCopy

pdirs = set()
tdirs = set()
srcs = set()
tgts = set()
codes = set()
lckers = {}
paths = {}
pres = set()
rckers = {}
opdep = []

from config_funcs import *

addPathPrefix("HOME", "C:\\")
addPathPrefix("USER", "C:\\Users\\Donald Chitester")
addPathPrefix("proj", pre("HOME") / "projects")
addPathPrefix("gd", "GoogleDrive:")
addPathPrefix("od", "OneDrive:")

# addSrcDir('docs', pre('USER') / 'Documents', False)
addSrcDir("docs", pre("USER") / "docs", False)
addSrcDir("refs", pre("HOME") / "Reference", False)

# addSrcDir('home', pre('HOME'), False) #

from dirlist import getdl
from functools import partial

dl = getdl(pre("proj"))
for d in dl:
    addSrcDir(d.name, d, True)
    addDep("git_index", d.name)
    addDep("proj", d.name)

from gitops import gitck1, gitck2, gitremoteck

srcs.add("git_index")
lckers["git_index"] = partial(gitck1, "git_index")

addSrcDir("git", pre("proj") / ".git", False)
lckers["git"] = partial(gitck2, "git")

tgts.add("bitbucket")
rckers["bitbucket"] = partial(gitremoteck, "bitbucket")

addSrcDir("proj", pre("proj"), False)

worktree = pre("HOME") / "projects"

if "NOGIT" not in os.environ:
    npl1 = ("git", "git_index")
    op1 = GitOps(npl1, None, {"wt": worktree, "add": True, "commit": True})
    addArc(op1)

    npl1 = ("bitbucket", "git")
    op1 = GitOps(
        npl1, None, {"wt": worktree, "rmt": "bitbucket", "pull": True, "push": True}
    )
    addArc(op1)


def cs_create(tgl, sil, dlf=False):
    for tg in tgl:
        for si in sil:  # ('proj', ):
            p1 = pdir(si).relative_to(pre("HOME"))
            addTgtDir(tg + "_" + si, pre(tg) / p1)
            npl1 = (tg + "_" + si, si)
            op1 = CSCopy(npl1, None, {"delete": dlf})
            addArc(op1)


cs_create(["gd"], ["proj"], False)
cs_create(["gd"], ["refs"], True)

# addSrcDir('qucs_src', pre('USER') / '.qucs', False)
# addTgtDir('qucs', pdir('qucs'))
# addDep('qucs', 'qucs_src')
# npl1 = ('qucs', 'qucs_src')
# op1 = LocalCopy(npl1, npl1, {'delete': False})
# addArc(op1)

from fmd5h import fmd5hd
from edge import dep
from opbase import OpBaseEncoder

config_dict = {}
config_dict["paths"] = paths
config_dict["pres"] = pres
config_dict["pdirs"] = pdirs
config_dict["tdirs"] = tdirs
config_dict["srcs"] = srcs
config_dict["tgts"] = tgts
config_dict["codes"] = codes

config_dict["dep"] = dep
config_dict["opdep"] = opdep
config_dict["worktree"] = worktree

config_dict["fmd5hd"] = fmd5hd


def round2ms(ns):
    return int(str(ns + 500000)[:-6]) / 1e3


def trunc2ms(ns):
    return int(str(ns)[:-6]) / 1e3


def save_config():
    with open("config.json", "w") as fh:
        json.dump(config_dict, fh, indent=2, cls=OpBaseEncoder)


if __name__ == "__main__":
    save_config()
    for k in config_dict:
        print(len(config_dict[k]), k)
