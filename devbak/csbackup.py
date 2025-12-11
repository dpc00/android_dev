from pathlib import Path
from asyncrun import run
import asyncio
from opbase import OpBase

igns = ' --exclude "__pycache__/**" --exclude ".git/**" --delete-excluded '


class Csbackup(OpBase):
    async def __call__(self):
        from tstamp import bctck, clr, ts2
        from bkenv import pdir, svcs, tdir
        from netup import netup
        from status import onestatus

        print("Csbackup")
        tcfc = [0, 0]
        tl = []
        for di, si in self.npl1:
            (N2, N1) = ts2(di, si)
            if bctck(N2, N1):
                sd = pdir[si]
                td = tdir[di + "-" + si]
                if "copy" in self.opts:
                    cmd = "rclone copy "
                else:
                    cmd = "rclone sync "
                cmd += (
                    str(sd) + " " + str(td) + " --progress --stats-one-line --update -v"
                )
                if not sd.is_file():
                    cmd += " " + igns

                async def f1(cmd, sd, td, tcfc, N1, N2):
                    if await netup():
                        print(sd, "->", td)
                        rc = await run(cmd)
                        if rc == 0:
                            clr(N2, N1)
                            if bctck(N2, N1):
                                print("clr failure!")
                            tcfc[0] += 1
                        else:
                            tcfc[1] += 1

                tl.append(asyncio.create_task(f1(cmd, sd, td, tcfc, N1, N2)))
            await asyncio.gather(*tl)
        if tcfc[0] > 0 or tcfc[1] > 0:
            onestatus("rclone_as_src")
        return (tcfc[0], tcfc[1])
