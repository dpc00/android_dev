from asyncrun import run
from pathlib import Path
from opbase import OpBase

class Mkzip(OpBase):
    async def __call__(self):
        from tstamp import bctck, clr, ts2
        from bkenv import pdir, tdir
        from status import onestatus
        print('Mkzip')
        anyd = False
        tc = 0
        fc = 0
        for di, si in self.npl1:
            (N2, N1) = ts2(di, si)
            if bctck(N2, N1):
                anyd = True
                break
        if anyd:
            di, si = self.npl2[0]
            zf = self.opts.get('zipfile', 'projects.zip')
            tp = tdir[di] / zf
            sd = pdir[si]
            cmd = 'zip -r -q ' + \
                str(tp) + ' ' + \
                str(sd) + '/*'
            print(cmd)
            try:
                await run(cmd, cwd=sd)
                for di, si in self.npl1:
                    (N2, N1) = ts2(di, si)
                    clr(N2, N1)
                    if bctck(N2, N1):
                        print('clr failure!')
                tc += 1
            except Exception as e:
                print(e)
                fc += 1
            if tc > 0:
                onestatus(self.npl1[0][0])
        return (tc, fc)
