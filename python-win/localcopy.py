from os import makedirs

from asyncrun import run1
from opbase import OpBase
from hashlib import sha256

global ldlls_dirty


def sha256sums(S1):
    ho = sha256()
    ho.update(S1)
    return ho.hexdigest()


def sha256sumf(Fn):
    if Fn.exists():
        b = Fn.read_bytes()
        ho = sha256()
        ho.update(b)
        return ho.hexdigest()
    return None


async def copy2(f1, f2):
    # print('copying ', f1, 'to', f2)
    if f1.is_file():
        f2 = f2.parent
    cmd = 'copy "' + str(f1) + '" "' + str(f2) + '"'
    print(cmd)
    return await run1(cmd)


# import shutil
# shutil.copy2(f1, f2)


def chkdiff(f1, f2):
    if f1.exists():
        if not f2.exists():
            print("dst file missing:")
            return True
        f1s = f1.stat()
        f2s = f2.stat()
        if f2s.st_size < f1s.st_size:
            print("size less:", f2s.st_size - f1s.st_size)
            return True
        if f2s.st_size > f1s.st_size:
            print("size more:", f2s.st_size - f1s.st_size)
            return True
        if f2s.st_mtime_ns > f1s.st_mtime_ns:
            print("time later:", (f2s.st_mtime_ns - f1s.st_mtime_ns) / 1e9)
            return False
        if sha256sumf(f1) != sha256sumf(f2):
            print("hash diff:", f1, f2)
            return True
    return False


class LocalCopy(OpBase):
    async def __call__(self):
        from config import pdir, tdir
        from edge import findEdge
        from dirlist import ldlls

        global ldlls_dirty
        tc = 0
        fc = 0
        di, si = self.npl1
        e = findEdge(di, si)
        if e.bctck():
            print("LocalCopy")
            sp = pdir(self.npl2[1])
            dp = tdir(self.npl2[0])
            gl = self.opts.get("files", ["**/*"])
            for g in gl:
                fl = sp.glob(g)
                for fsf in fl:
                    rf = fsf.relative_to(sp)
                    fdf = dp / rf
                    pd = fdf.parent
                    try:
                        if not pd.exists():
                            makedirs(pd, exist_ok=True)
                        if chkdiff(fsf, fdf):
                            rv = await copy2(fsf, fdf)
                            if rv == 0:
                                if "exec" in self.opts:
                                    fdf.chmod(496)
                                tc += 1
                            else:
                                fc += 1
                    except Exception as e:
                        print(e)
                        fc += 1
            if fc == 0:
                e.clr()
                if e.bctck():
                    print("clr failure!")
            if tc > 0:
                tv = self.npl2[0]
                if tv in ldlls:
                    del ldlls[tv]
                    ldlls_dirty = True
        return tc, fc
