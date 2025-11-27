from mkzip import Mkzip
from scopy import Scopy
from gitbackup import Gitbackup
from csbackup import Csbackup
from pathlib import Path

tags = []
names = []
paths = []

tpls = []

pres = {}
pdirs = {}
tdirs = {}
svcs = {}

dep = set()
opdep = {}

srcs = {}
codes = {}

dstts = []
srcts = []

def idin(L, it):
    if it not in L:
        ii = len(L)
        L.append(it)
        return ii
    else:
        return L.index(it)

def nameid(n):
	return idin(names, n)
	
def tagid(t):
	return idin(tags, t)

def pathid(p):
	return idin(paths, p)

def tplid(t):
	return idin(tpls, t)

def pre(s):
	return paths[pres[tagid(s)]]

def pdir(s):
	return paths[pdirs[tagid(s)]]

def tdir(s):
	return paths[tdirs[tagid(s)]]

def src(s):
	return paths[srcs[tagid(s)]]

def code(s):
	return paths[codes[tagid(s)]]

def svc(s):
	return names[svcs[tagid(s)]]

def PathPrefix(tag, frag):
    if not isinstance(frag, Path):
        frag = Path(frag)
    tid = tagid(tag)
    pid = pathid(frag)
    pres[tid] = pid

#---

def SrcDir(tag, path, iscode=False, isremote=False):
    global ni1
    if not isinstance(path, Path):
        path = Path(path)
    tid = tagid(tag)
    pid = pathid(path)
    pdirs[tid] = pid
    srcs[tid] = pid
    if iscode:
        codes[tid] = pid
    if not isremote:
        lpd = pre('sd')
        for svcid in svcs:
            try:
                rd = path.relative_to(lpd)
                td = pres[svcid] / rd
                ntag = tags[svcid] + '-' + tags[tid]
                print('ntag',ntag)
                TgtDir(ntag, td)
            except:
                pass


def TgtDir(tag, path):
    if not isinstance(path, Path):
        path = Path(path)
    tid = tagid(tag)
    pid = pathid(path)
    tdirs[tid] = pid


def CloudService(name, tag):
    tid = tagid(tag)
    nid = nameid(name)
    svcs[tid] = nid
    PathPrefix(tag, name + ':')


def Arc(op):
    global ni1, ni2
    opdep[op.npl1] = op
    for j, i in op.npl1:
        if (j, i) not in dep:
            dep.add((j, i))
        idin(srcts, i)
        idin(dstts, (j, i))

class NPL(list):  # tuple-pair list
    def __init__(self, dt, st):
        super(NPL, self).__init__()
        dit = tuple(tagid(t) for t in dt)
        sit = tuple(tagid(t) for t in st)
        self.dtid = tplid(dit)
        self.stid = tplid(sit)
        for dtagid in tpls[self.dtid]:
            for stagid in tpls[self.stid]:
                self.append(( dtagid,stagid ))

    def __hash__(self):
        return hash((self.dtid, self.stid))

    def __eq__(self, other):
        return self.dtid == other.dtid and self.stid == other.stid

    def __neq__(self, other):
        return self.dtid != other.dtid or self.stid != other.stid


PathPrefix('sd', '/sdcard')
PathPrefix('proj', pre('sd') / 'projects')
PathPrefix('FLAGS', '/data/data/com.termux/files/home')
PathPrefix('bkx', pre('FLAGS') / '.bkx')

CloudService('DropBox', 'db')
CloudService('GoogleDrive', 'gd')
CloudService('OneDrive', 'od')

SrcDir('docs', pre('sd') / 'Documents')
SrcDir('refs', pre('sd') / 'Reference')
SrcDir('fdb', pdir('docs') / 'Finance.db')
SrcDir('zip', pre('sd') / 'backups/projects.zip')
SrcDir('blog', pre('proj') / 'blog', True)
SrcDir('fdbak', pre('proj') / 'fdb', True)
SrcDir('scrdev', pre('proj') / 'bash', True)
SrcDir('bash2', pre('proj') / 'bash2', True)
SrcDir('pro', pre('proj') / 'prolog', True)
SrcDir('js', pre('proj') / 'js', True)
SrcDir('pyth', pre('proj') / 'python', True)
SrcDir('dev_bak', pre('proj') / 'devbak', True)
SrcDir('git', pre('proj') / '.git')
SrcDir('rclone_as_src', pre('FLAGS') / '.config/rclone')
SrcDir('proj', pre('proj'))

del srcs[tagid('proj')]

TgtDir('home', pre('FLAGS'))
TgtDir('bin', tdir('home') / 'bin')
TgtDir('sh', tdir('home') / 'bin/sh')
TgtDir('pl', tdir('home') / 'bin/pl')
TgtDir('py', tdir('home') / 'bin/py')
TgtDir('backups', pre('sd') / 'backups')
TgtDir('fdbak', pre('proj') / 'fdb')
TgtDir('scrdev', pre('proj') / 'bash')
TgtDir('rclone', tdir('home') / '.config/rclone')

worktree = pre('sd') / 'projects'


def init_ops():
    npl = NPL(('scrdev', ), ('rclone_as_src', ))
    Arc(Scopy(npl, npl, {'files': ['rclone.conf']}))

    npl = NPL(('rclone', ), ('scrdev', ))
    Arc(Scopy(npl, npl, {'files': ['rclone.conf']}))

    npl = NPL(('home', ), ('scrdev', ))
    Arc(
        Scopy(
            npl, npl, {
                'files': [
                    '.termux/*', '.bash*', '.swi*', '.profile',
                    '.clang-format', 'rsyncd.conf'
                ]
            }))
    #opdep[('etc',), ('scrdev',)] = Scopy(('etc',),('scrdev',),('etc',),('scrdev',),{'files': ['rsyncd.conf', 'rsyncd.secrets']})

    npl = NPL(('bin', ), ('scrdev', ))
    Arc(Scopy(npl, npl, {'files': ['termux-*'], 'exec': True}))

    npl = NPL(('sh', ), ('scrdev', ))
    Arc(Scopy(npl, npl, {'files': ['*.sh', '*.env'], 'exec': True}))

    npl = NPL(('py', ), ('pyth', ))
    Arc(Scopy(npl, npl, {'files': ['*.py'], 'exec': True}))

    npl = NPL(('pl', ), ('pro', ))
    Arc(Scopy(npl, npl, {'files': ['*.pl'], 'exec': True}))

    npl1 = NPL(('fdbak', ), ('fdb', ))
    npl2 = NPL(('fdbak', ), ('docs', ))
    Arc(Scopy(npl1, npl2, {'files': ['Finance.db']}))

    npl1 = NPL(('backups', ), ('fdb', ))
    npl2 = NPL(('backups', ), ('docs', ))
    Arc(Scopy(npl1, npl2, {'files': ['Finance.db']}))

    npl = NPL(('git', ), tuple(tags[t] for t in codes))
    Arc(Gitbackup(npl, None, {'wt': worktree, 'add': True, 'commit': True}))

    npl = NPL(('local', ), ('git', ))
    Arc(Gitbackup(npl, None, {'wt': worktree, 'rmt': 'local', 'push': True}))

    npl = NPL(('bitbucket', ), ('git', ))
    Arc(
        Gitbackup(npl, None, {
            'wt': worktree,
            'rmt': 'bitbucket',
            'push': True
        }))


    #npl1 = NPL(('zip', ), tuple(tags[t] for t in codes))
    #npl2 = NPL(('backups', ), ('proj', ))
    #Arc(Mkzip(npl1, npl2, {'zipfile': 'projects.zip'}))

    npl = NPL(('db', 'od', 'gd'), tuple(tags[t] for t in codes))
    Arc(Csbackup(npl, None, {}))

    npl = NPL(('db', 'od', 'gd'), ('docs','refs'))
    Arc(Csbackup(npl, None, {'copy': True}))

init_ops()

dep.add(tuple(tagid(t) for t in ('local', 'bitbucket')))
dep.add(tuple(tagid(t) for t in ('db', 'local')))
dep.add(tuple(tagid(t) for t in ('gd', 'local')))
dep.add(tuple(tagid(t) for t in ('od', 'local')))

if __name__ == '__main__':
    gc = globals().copy()
    for it in gc:
        print(it, gc[it])
