from pathlib import Path
from asyncrun import run
from os import chdir
from netup import netup
from opbase import OpBase

class Gitbackup(OpBase):
    async def __call__(self):
        from tstamp import bctck, clr, ts2
        from dhash import dhset
        from status import onestatus
        print('Gitbackup')
        tc = 0
        fc = 0
        anyd = False
        for di, si in self.npl1:
            (N2, N1) = ts2(di, si)
            if bctck(N2, N1):
                anyd = True
                break
        if not anyd:
            return (tc, fc)
        wt = self.opts['wt']
        if 'add' in self.opts:
            try:
                await run('git add -A .', cwd=wt)
                tc += 1
            except Exception as e:
                print(e)
                fc += 1
        if 'commit' in self.opts:
            try:
                await run('git commit -a -m pybak', cwd=wt)
                tc += 1
            except Exception as e:
                print(e)
                fc += 1
        if tc > 0:
            onestatus(self.npl1[0][0])
        if 'push' in self.opts:
            rmt = self.opts.get('rmt')
            if rmt=='local' or (await netup()):
                try:
                    await run('git push ' + rmt + ' master', cwd=wt)
                    dhset('git')
                    tc += 1
                except Exception as e:
                    print(e)
                    fc += 1
        if fc == 0 and tc > 0:
            for di, si in self.npl1:
                (N2, N1) = ts2(di, si)
                clr(N2, N1)
                if bctck(N2, N1):
                    print('clr failure!')
        return (tc, fc)
