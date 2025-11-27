from threading import RLock

import asyncrun as ar
import config
from edge import Edge, findEdge
from netup import netup
from opbase import OpBase

rl = RLock()


class GitAdd(OpBase):
    def __init__(self, npl1, npl2, opts={}) -> None:
        super().__init__(npl1, npl2, opts)

    def ischanged(self, e: Edge):
        return e.chk_ct() | e.rchk_ct()

    def __call__(self):
        print("GitAdd")
        tc = 0
        fc = 0
        s = ""
        anyd = False
        di, si = self.npl1
        e: Edge = findEdge(di, si)
        if e.chk_ct():
            s += "l"
            anyd = True
        if e.rchk_ct():
            s += "r"
            anyd = True
        if not anyd:
            return (tc, fc)
        with rl:
            rc, txt1, txt2 = ar.run4("git add -A . -v", cwd=config.src(si))
        if rc == 0:
            tc += 1
        else:
            fc += 1
        if fc == 0:
            e.clr()
            e.rclr()
        return (tc, fc)


class GitCommit(OpBase):
    def __init__(self, npl1, npl2, opts={}) -> None:
        super().__init__(npl1, npl2, opts)

    def ischanged(self, e: Edge):
        return e.chk_ct() | e.rchk_ct()

    def __call__(self):
        print("GitCommit")
        tc = 0
        fc = 0
        s = ""
        anyd = False
        di, si = self.npl1
        e: Edge = findEdge(di, si)
        if e.chk_ct():
            s += "l"
            anyd = True
        if e.rchk_ct():
            s += "r"
            anyd = True
        if not anyd:
            return (tc, fc)
        with rl:
            rc, txt1, txt2 = ar.run4("git commit -a -m pybak -v", cwd=self.opts["wt"])
        if rc in (0, 1):
            tc += 1
        else:
            print("git commit rc:", rc)
            fc += 1
        if fc == 0:
            e.clr()
            e.rclr()
        return (tc, fc)


class GitPush(OpBase):
    def __init__(self, npl1, npl2, opts={}) -> None:
        super().__init__(npl1, npl2, opts)

    def ischanged(self, e: Edge):
        return e.chk_ct() | e.rchk_ct()

    def __call__(self):
        rmt = self.opts.get("rmt")
        print("GitPush", rmt)
        tc = 0
        fc = 0
        s = ""
        anyd = False
        di, si = self.npl1
        e: Edge = findEdge(di, si)
        if e.chk_ct():
            s += "l"
            anyd = True
        if e.rchk_ct():
            s += "r"
            anyd = True
        if not anyd:
            return (tc, fc)
        if rmt == "local" or (netup()):
            with rl:
                rc, txt1, txt2 = ar.run4(
                    "git push " + rmt + " master", cwd=self.opts["wt"]
                )
            if rc == 0:
                tc += 1
            else:
                fc += 1
        if fc == 0:
            e.clr()
            e.rclr()
        return (tc, fc)
