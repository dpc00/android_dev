import asyncio
import datetime
import pickle
from dataclasses import dataclass, field
from os import walk

import asyncrun as ar
from config import *

rto1 = 0
rto2 = 0

ldlls = {}
rdlls = {}
ldlls_xt = {}
rdlls_xt = {}

ldlls_dirty = False
rdlls_dirty = False

ldllsf = pre('USER') / 'ldlls.pp'
rdllsf = pre('USER') / 'rdlls.pp'


def loadldlls():
    global ldlls, ldlls_xt
    try:
        ldlls = {}
        ldlls_xt = {}
        with open(ldllsf, "rb") as fh:
            td = pickle.load(fh)
            ldlls = td['ldlls']
            ldlls_xt = td['ldlls_xt']
    except Exception as e:
        print(e)
        ldlls_dirty=True
        pass


def loadrdlls():
    global rdlls, rdlls_xt
    try:
        rdlls = {}
        rdlls_xt = {}
        with open(rdllsf, "rb") as fh:
            td = pickle.load(fh)
            rdlls = td['rdlls']
            rdlls_xt = td['rdlls_xt']
    except Exception as e:
        print(e)
        rdlls_dirty=True
        pass


def saveldlls():
    global ldlls_dirty
    # print('-saveldlls')
    if ldlls_dirty:
        with open(ldllsf, "wb") as fh:
            td = {"ldlls": ldlls, "ldlls_xt": ldlls_xt}
            pickle.dump(td, fh)
        ldlls_dirty = False


def saverdlls():
    global rdlls_dirty
    # print('-saverdlls')
    if rdlls_dirty:
        with open(rdllsf, "wb") as fh:
            td = {"rdlls": rdlls, "rdlls_xt": rdlls_xt}
            pickle.dump(td, fh)
        rdlls_dirty = False


@dataclass
class DE:
    nm: Path
    sz: int
    mt: float
    md5: bytes
    _hc: int = field(default=None)

    def __hash__(self):
        from bhash import bhash
        if self._hc is None:
            self._hc = bhash((self.nm, self.sz, self.mt, self.md5))
        return self._hc

    def __eq__(self, other):
        return (str(self.nm), self.sz, self.mt,
                self.md5) == (str(other.nm), other.sz, other.mt, other.md5)

    def __lt__(self, other):
        return (str(self.nm), self.sz, self.mt, self.md5) < (str(
            other.nm), other.sz, other.mt, other.md5)


def getfl(p):
    # print(str(p))
    fl = []
    try:
        if p.is_file():
            fl.append(p)
            return fl
        for pth, dirs, files in walk(p, topdown=True):
            if str(pth).endswith('.git') or '.temp' in str(pth):
                dirs = []
                files = []
            if '.git' in dirs:
                dirs.remove('.git')
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')
            for f in files:
                fl.append(Path(pth, f))
        return fl
    except Exception as e:
        print(e)
        return None


def getdl(p):
    # print(str(p))
    dl = []
    try:
        for pth, dirs, files in walk(p, topdown=True):
            if str(pth).endswith('.git'):
                dirs = []
            if '.git' in dirs:
                dirs.remove('.git')
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')
            for d in dirs.copy():
                if str(d).startswith('.temp'):
                    pass
                else:
                    dl.append(Path(pth, d))
                    dirs.remove(d)
        return dl
    except Exception as e:
        print(e)
        return None


async def getdll0():
    from config import pre
    td = pre('gd')
    # print('getdll0')
    cmd = 'rclone lsjson "' + str(td) + '" --recursive --files-only --hash'
    # print(cmd)
    rc = await ar.run1(cmd)
    if rc == 0:
        l1 = json.loads(ar.txt)

        def es(it):
            it1 = Path(it['Path'])
            it2 = it['Size']
            it3 = it['ModTime'][:-1] + '-00:00'
            it3 = datetime.datetime.fromisoformat(it3).timestamp()
            try:
                it4 = bytes.fromhex(it['Hashes']['MD5'])
            except KeyError as ke:
                print(ke, it1)
                it4 = bytes()
            return DE(it1, it2, it3, it4)

        st = list(map(es, l1))
        st.sort()
        print(len(st), "de's")
        return st
    return None


def sepdlls(dlls):
    from config import tdirs, tdir, pre
    from fnmatch import fnmatch
    from bisect import bisect_left
    import time
    global rdlls_dirty
    for di in tdirs:
        if di.startswith('gd_'):
            rdlls[di] = []
            rdlls_xt[di] = time.time()
            rdlls_dirty = True
            rd = tdir(di).relative_to(pre('gd'))
            tds = str(rd) + '/'
            i = bisect_left(dlls, DE(tds, 0, 0, b''))
            # print(tds, i)
            if i == len(dlls):
                continue
            de = dlls[i]
            if not fnmatch(de.nm, tds + '*'):
                print('error')
                print(rd, tds, i, de.nm)
                # TODO: apply panic procedure
                continue
            while fnmatch(de.nm, tds + '*'):
                de2 = DE(de.nm, de.sz, de.mt, de.md5)
                # TODO: use Path
                de2.nm = de2.nm.relative_to(rd)
                # print(de2[0])
                # if de2 in csdlls[di]:
                # csdlls[di].remove(de2)
                rdlls[di].append(de2)
                i += 1
                if i == len(dlls):
                    break
                de = dlls[i]
    print(len(rdlls), 'csdlls')


async def getdll1(di):
    from config import tdir
    td = tdir(di)
    # print('getdll1', di, str(td))
    cmd = 'rclone lsjson "' + str(td) + '" --recursive --files-only --hash --fast-list'
    # print(cmd)
    rc = await ar.run1(cmd)
    if rc == 0:
        l1 = json.loads(ar.txt)

        def es(it):
            # TODO: use Path
            it1 = Path(it['Path'])
            it2 = it['Size']
            it3 = it['ModTime'][:-1] + '-00:00'
            it3 = datetime.datetime.fromisoformat(it3).timestamp()
            try:
                it4 = bytes.fromhex(it['Hashes']['MD5'])
            except KeyError as ke:
                print(ke, it1)
                it4 = bytes()
            return DE(it1, it2, it3, it4)

        st = list(map(es, l1))
        st.sort()
        return st
    elif rc == 3:
        return []
    return None


async def getdll2(si):
    from config import pdir
    td = pdir(si)
    # print('getdll2', si, str(td))
    cmd = 'rclone lsjson "' + str(
        td) + '" --recursive --files-only --hash --fast-list'
    if not td.is_file():
        cmd += ' --exclude ".git/**" --exclude "__pycache__/**"'
    # print(cmd)
    rc = await ar.run1(cmd)
    if rc == 0:
        l1 = json.loads(ar.txt)

        def es(it):
            # TODO: use Path
            it1 = Path(it['Path'])
            it2 = it['Size']
            it3 = it['ModTime'][:-7] + '-00:00'
            it3 = datetime.datetime.fromisoformat(it3).timestamp()
            it4 = bytes.fromhex(it['Hashes']['MD5'])
            return DE(it1, it2, it3, it4)

        st = list(map(es, l1))
        st.sort()
        return st
    elif rc == 3:
        return []
    return None


def getdll3(si):
    from fmd5h import fmd5f
    from config import trunc2ms, src
    sd = src(si)
    # print('getdll3', si, str(sd))
    l1 = getfl(sd)

    def es(it):
        # TODO: use Path
        it1 = it.relative_to(sd)
        fs = it.stat()
        it2 = fs.st_size
        it3 = fs.st_mtime_ns
        it3 = trunc2ms(it3)
        it4 = fmd5f(it, it2, it3)
        return DE(it1, it2, it3, it4)

    st = list(map(es, l1))
    st.sort()
    return st


async def getrdlls():
    import time
    if len(rdlls) == 0:
        t1 = time.time()
        rv = await getdll0()
        if rv is not None:
            t2 = time.time()
            sepdlls(rv)
            t3 = time.time()
            print(round(t2 - t1, 3), round(t3 - t2, 3))


async def ldlld(si):
    # print('-ldlld', di)
    import time
    global ldlls_dirty
    if si not in ldlls or ldlls_xt[si] + rto2 <= time.time():
        rv = getdll3(si)
        if rv is not None:
            # print(si, 'ldll obtained')
            ldlls[si] = rv
            ldlls_xt[si] = time.time()
            ldlls_dirty = True
        return rv
    else:
        return ldlls[si]


async def rdlld(di):
    # print('-rdlld', di)
    import time
    global rdlls_dirty
    if di not in rdlls or rdlls_xt[di] + rto1 <= time.time():
        rv = await getdll1(di)
        if rv is not None:
            print(di, 'rdll obtained')
            rdlls[di] = rv
            rdlls_xt[di] = time.time()
            rdlls_dirty = True
        return rv
    else:
        return rdlls[di]

def f1(do, dn):
    do_ht = {}
    dn_ht = {}
    for it in do:
        if it.md5 not in do_ht:
            do_ht[it.md5] = [it]
        else:
            do_ht[it.md5].append(it)
    for it in dn:
        if it.md5 not in dn_ht:
            dn_ht[it.md5] = [it]
        else:
            dn_ht[it.md5].append(it)
    return (do_ht, dn_ht)


def dllcmp(do, dn):
    dns = set(dn)
    dos = set(do)
    tocopy = dns - dos
    todelete = dos - dns
    doh, dnh = f1(do, dn)
    tomove = set()
    for it1 in todelete.copy():
        if it1.md5 in doh:
            for it2 in doh[it1.md5]:
                if it2.nm.name == it1.nm.name and it2.nm.parent != it1.nm.parent:
                    for it3 in tocopy.copy():
                        if it3.nm.name == it1.nm.name and it3.md5 == it1.md5 and it3.nm.parent != it1.nm.parent:
                            tocopy.remove(it3)
                            tomove.add((it3, it1))
                            todelete.remove(it1)
    return todelete, tocopy, tomove


if __name__ == '__main__':
    import time

    t1 = time.time()
    rv = asyncio.run(getdll0())
    sepdlls(rv)
    print(len(rv), len(rdlls))
    t2 = time.time()
    print(t2 - t1)
else:
    loadrdlls()
    loadldlls()
