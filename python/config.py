import os
import json

from localcopy import LocalCopy
from gitops import GitOps
from cscopy import CSCopy
from csrestore import CSRestore
from mkzip import Mkzip

paths = {}
pres = set()
pdirs = set()
tdirs = set()
srcs = set()
tgts = set()
codes = set()
lckers = {}
rckers = {}
opdep = []

from config_funcs import *

addPathPrefix('sd', '/sdcard')
addPathPrefix('proj', pre('sd') / 'projects')
addPathPrefix('FLAGS', '/data/data/com.termux/files/home')
addPathPrefix('bkx', pre('FLAGS') / '.bkx')
addPathPrefix('gd', 'GoogleDrive:')

addSrcDir('docs', pre('sd') / 'Documents', False)
addSrcDir('refs', pre('sd') / 'Reference', False)
addSrcDir('fdbd', pdir('docs') / 'Finance.db', False)
addSrcDir('backups', pre('sd') / 'backups', False)
addSrcDir('home', pre('FLAGS'), False)

from dirlist import getdl
from functools import partial

dl = getdl(pre('proj'))
for d in dl:
    addSrcDir(d.name, d, True)
    addDep('git_index', d.name)
    addDep('zips', d.name)
    addDep('proj', d.name)
    
addSrcDir('zips', pre('sd') / 'zips', False)

from gitops import gitck1, gitck2, gitremoteck

srcs.add('git_index')
lckers['git_index'] = partial(gitck1,'git_index')

addSrcDir('git', pre('proj') / '.git', False)
lckers['git'] = partial(gitck2, 'git')

tgts.add('bitbucket')
rckers['bitbucket'] = partial(gitremoteck, 'bitbucket')

addSrcDir('proj', pre('proj'), False)


addTgtDir('home', pre('FLAGS'))
addTgtDir('bin', tdir('home') / 'bin')
addTgtDir('sh', tdir('home') / 'bin/sh')
addTgtDir('pl', tdir('home') / 'bin/pl')
#addTgtDir('hnim', tdir('home') / 'nim')
addTgtDir('py', tdir('home') / 'bin/py')
addTgtDir('hgo', tdir('home') / 'go')
addTgtDir('backups', pre('sd') / 'backups')
addTgtDir('fdb', pre('proj') / 'fdb')
addTgtDir('zips', pre('sd') / 'zips')
addTgtDir('blogds', pre('sd') / 'DroidScript/blog')
addTgtDir('termux-backup', pre('sd') / 'backups' / 'termux-backup')

worktree = pre('sd') / 'projects'

npl1 = ('home', 'bash')
op1 = LocalCopy(
    npl1, npl1, {
        'files': [
            '.termux/*', '.bash*', '.swi*', '.profile', '.clang-format',
            'rsyncd.conf'
        ]
    })
addArc(op1)

npl1 = ('bin', 'bash')
op1 = LocalCopy(npl1, npl1, {'files': ['termux-*'], 'exec': True})
addArc(op1)

npl1 = ('sh', 'bash')
op1 = LocalCopy(npl1, npl1, {'files': ['*.sh', '*.env'], 'exec': True})
addArc(op1)

npl1 = ('py', 'python')
op1 = LocalCopy(npl1, npl1, {'files': ['*.py'], 'exec': True})
addArc(op1)

npl1 = ('hgo', 'go')
op1 = LocalCopy(npl1, npl1, {'files': ['**/*.*']})
addArc(op1)

npl1 = ('pl', 'prolog')
op1 = LocalCopy(npl1, npl1, {'files': ['*.pl'], 'exec': True})
addArc(op1)

#npl1 = ('hnim', 'nim')
#op1 = LocalCopy(npl1, npl1, {'files': ['**/*.*'], 'exec': True})
#addArc(op1)

npl1 = ('fdb', 'fdbd')
npl2 = ('fdb', 'docs')
op1 = LocalCopy(npl1, npl2, {'files': ['Finance.db']})
addArc(op1)

npl1 = ('blogds', 'blog')
npl2 = ('blogds', 'blog')
op1 = LocalCopy(npl1, npl2, {'files': ['*.*']})
addArc(op1)

npl1 = ('termux-backup', 'home')
op1 = LocalCopy(npl1, npl1, {'files': ['**/*.*']})
addArc(op1)

#npl1 = ('backups', 'fdbd')
#npl2 = ('backups', 'docs')
#op1 = Scopy(npl1, npl2, {'files': ['Finance.db']})
#addArc(op1)

if 'NOGIT' not in os.environ:
    npl1 = ('git', 'git_index')
    op1 = GitOps(npl1, None, {
        'wt': worktree,
        'add': True,
        'commit': True
    })
    addArc(op1)

    npl1 = ('bitbucket', 'git')
    op1 = GitOps(npl1, None, {
        'wt': worktree,
        'rmt': 'bitbucket',
        'pull': True,
        'push': True
    })
    addArc(op1)

for si in codes:
    npl1 = ('zips', si)
    op1 = Mkzip(npl1, npl1, {'zipfile': si + '.zip'})
    addArc(op1)

for si in ('docs', 'refs', 'proj', 'zips'):
    p1 = pdir(si).relative_to(pre('sd'))
    addTgtDir('gd_' + si, pre('gd') / p1)
    npl1 = ('gd_' + si, si)
    #op1 = CSRestore(npl1, None, {})
    #addArc(op1)
    op1 = CSCopy(npl1, None, {'delete': False})
    addArc(op1)
    
from fmd5h import fmd5hd
from edge import dep
from opbase import OpBaseEncoder

config_dict = {}
config_dict['paths'] = paths
config_dict['pres'] = pres
config_dict['pdirs'] = pdirs
config_dict['tdirs'] = tdirs
config_dict['srcs'] = srcs
config_dict['tgts'] = tgts
config_dict['codes'] = codes

config_dict['dep'] = dep
config_dict['opdep'] = opdep
config_dict['worktree'] = worktree

config_dict['fmd5hd'] = fmd5hd


def round2ms(ns):
    return int(str(ns + 500000)[:-6]) / 1E3


def trunc2ms(ns):
    return int(str(ns)[:-6]) / 1E3


def save_config():
    with open('config.json', 'w') as fh:
        json.dump(config_dict, fh, indent=2, cls=OpBaseEncoder)


if __name__ == '__main__':
    save_config()
    for k in config_dict:
        print(len(config_dict[k]), k)
