from mkzip import Mkzip
from scopy import Scopy
from gitbackup import Gitbackup
from csbackup import Csbackup
from pathlib import Path

ni1 = 1
ni2 = 1

codes = {}
dep = set()
dstts = {}
opdep = {}
pdir = {}
pre = {}
snm = {}
srcs = {}
srcts = {}
svcs = {}
tdir = {}


def PathPrefix(tag, frag):
    if not isinstance(frag, Path):
        frag = Path(frag)
    pre[tag] = frag


def SrcDir(tag, path, iscode=False, isremote=False):
    global ni1
    if not isinstance(path, Path):
        path = Path(path)
    pdir[tag] = path
    srcs[tag] = path
    if iscode:
        codes[tag] = path
    if tag not in srcts:
        srcts[tag] = ni1
        ni1 += 1
    if not isremote:
        lpd = pre['sd']
        for svc in svcs:
            try:
                rd = path.relative_to(lpd)
                td = pre[svc] / rd
                TgtDir(svc + '-' + tag, td)
            except:
                pass


def TgtDir(tag, path):
    if not isinstance(path, Path):
        path = Path(path)
    tdir[tag] = path


def CloudService(name, tag):
    svcs[tag] = name
    snm[tag] = name
    PathPrefix(tag, name + ':')


def Arc(op):
    global ni1, ni2
    opdep[op.npl1] = op
    for j, i in op.npl1:
        if (j, i) not in dep:
            dep.add((j, i))
        if i not in srcts:
            srcts[i] = ni1
            ni1 += 1
        if (j, i) not in dstts:
            dstts[j, i] = ni2
            ni2 += 1


class NPL(list):  # node-pair list
    def __init__(self, di, si):
        super(NPL, self).__init__()
        self.di = di
        self.si = si
        for j in di:
            for i in si:
                self.append((j, i))

    def __hash__(self):
        return hash((self.di, self.si))

    def __eq__(self, other):
        return self.di == other.di and self.si == other.si

    def __neq__(self, other):
        return self.di != other.di or self.si != self.si


PathPrefix('sd', '/sdcard')
PathPrefix('proj', pre['sd'] / 'projects')
PathPrefix('FLAGS', '/data/data/com.termux/files/home')
PathPrefix('bkx', pre['FLAGS'] / '.bkx')

CloudService('DropBox', 'db')
CloudService('GoogleDrive', 'gd')
CloudService('OneDrive', 'od')

SrcDir('docs', pre['sd'] / 'Documents')
SrcDir('refs', pre['sd'] / 'Reference')
SrcDir('fdb', pdir['docs'] / 'Finance.db')
SrcDir('zip', pre['sd'] / 'backups/projects.zip')
SrcDir('blog', pre['proj'] / 'blog', True)
SrcDir('fdbak', pre['proj'] / 'fdb', True)
SrcDir('scrdev', pre['proj'] / 'bash', True)
SrcDir('bash2', pre['proj'] / 'bash2', True)
SrcDir('pro', pre['proj'] / 'prolog', True)
SrcDir('js', pre['proj'] / 'js', True)
SrcDir('pyth', pre['proj'] / 'python', True)
SrcDir('dev_bak', pre['proj'] / 'devbak', True)
SrcDir('git', pre['proj'] / '.git')
SrcDir('rclone_as_src', pre['FLAGS'] / '.config/rclone')
SrcDir('proj', pre['proj'])

del srcs['proj']

TgtDir('home', pre['FLAGS'])
TgtDir('bin', tdir['home'] / 'bin')
TgtDir('sh', tdir['home'] / 'bin/sh')
TgtDir('pl', tdir['home'] / 'bin/pl')
TgtDir('py', tdir['home'] / 'bin/py')
TgtDir('backups', pre['sd'] / 'backups')
TgtDir('fdbak', pre['proj'] / 'fdb')
TgtDir('scrdev', pre['proj'] / 'bash')
TgtDir('rclone', tdir['home'] / '.config/rclone')

worktree = pre['sd'] / 'projects'


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

    npl = NPL(('git', ), tuple(codes))
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


    #npl1 = NPL(('zip', ), tuple(codes))
    #npl2 = NPL(('backups', ), ('proj', ))
    #Arc(Mkzip(npl1, npl2, {'zipfile': 'projects.zip'}))

    npl = NPL(('db', 'od', 'gd'), tuple(codes))
    Arc(Csbackup(npl, None, {}))

    npl = NPL(('db', 'od', 'gd'), tuple(['docs','refs']))
    Arc(Csbackup(npl, None, {'copy': True}))

init_ops()

dep.add(('local', 'bitbucket'))
dep.add(('db', 'local'))
dep.add(('gd', 'local'))
dep.add(('od', 'local'))

if __name__ == '__main__':
    for i in opdep:
        print(i, opdep[i])
