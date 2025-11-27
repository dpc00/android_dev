from pathlib import Path
from os import makedirs
from hashlib import sha256
from asyncrun import run
from opbase import OpBase

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
    #print('copying ', f1, 'to', f2)
    if f1.is_file():
        f2 = f2.parent
    cmd = 'rclone copy ' + str(f1) + ' ' + str(
        f2) + ' --progress --stats-one-line --update -v'
    # print('cmd:',cmd)
    await run(cmd)


#import shutil
#shutil.copy2(f1, f2)


def chkdiff(f1, f2):
    if f1.exists():
        if not f2.exists():
            print('dst file missing:')
            return True
        if f2.stat().st_size < f1.stat().st_size:
            print('size less:', f2.stat().st_size - f1.stat().st_size)
            return True
        if f2.stat().st_mtime_ns < f1.stat().st_mtime_ns:
            print('time older:',
                  (f2.stat().st_mtime_ns - f1.stat().st_mtime_ns) / 1E9)
            return True
        if sha256sumf(f1) != sha256sumf(f2):
            print('hash diff:', f1, f2)
            return True
    return False


class Scopy(OpBase):
    async def __call__(self):
        from bkenv import pdir, tdir, srcs
        from tstamp import bctck, clr, ts2
        from status import onestatus

        tc = 0
        fc = 0
        di, si = self.npl1[0]
        (N2, N1) = ts2(di, si)
        if bctck(N2, N1):
            print('Scpy')
            sp = pdir[self.npl2[0][1]]
            dp = tdir[self.npl2[0][0]]
            gl = self.opts.get('files', ['**/*'])
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
                            await copy2(fsf, fdf)
                            if 'exec' in self.opts:
                                fdf.chmod(496)
                            tc += 1
                    except Exception as e:
                        print(e)
                        fc += 1
            if fc == 0:
                clr(N2, N1)
                if bctck(N2, N1):
                    print('clr failure!')
            if tc > 0:
                ti = self.npl2[0][0]
                if ti in srcs:
                    onestatus(ti)
        return (tc, fc)
