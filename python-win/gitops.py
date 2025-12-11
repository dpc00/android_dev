import asyncrun as ar
from bhash import bhash
from netup import netup
from opbase import OpBase


async def gitck1(Si):
    from statushash import ldh_f, ldhset
    from config import worktree

    Dh1 = ldh_f(Si)
    cmd = "git status --porcelain --untracked-files=all"
    rc = await ar.run1(cmd, cwd=worktree)
    if rc == 0:
        rv = ar.txt.rstrip()
        Dh2 = bhash(rv)
        if len(rv) == 0:
            await ldhset(Si, Dh2)
        elif Dh2 != Dh1:
            print(rv)
        return Dh2, len(rv) > 0 and Dh2 != Dh1


async def gitck2(Si):
    from statushash import ldh_f, ldhset
    from config import worktree

    Dh1 = ldh_f(Si)
    if Dh1 is None:
        Dh1 = 0
    cmd = "git rev-list --count bitbucket/master..master"
    rc = await ar.run1(cmd, cwd=worktree)
    if rc == 0:
        rv = ar.txt.rstrip()
        Dh2 = int(rv)
        if Dh2 == 0:
            await ldhset(Si, Dh2)
        return Dh2, Dh2 > Dh1


async def gitremoteck(Di):
    from statushash import rdh_f, rdhset
    from config import worktree

    Dh1 = rdh_f(Di)
    Dh2 = None
    # print(Di, 'status here')
    cmd = "git remote update"
    rc = await ar.run1(cmd, cwd=worktree)
    if rc == 0:
        cmd = "git rev-parse @"
        rc = await ar.run1(cmd, cwd=worktree)
        if rc == 0:
            lcomm = ar.txt.rstrip()
            cmd = "git rev-parse @{u}"
            rc = await ar.run1(cmd, cwd=worktree)
            if rc == 0:
                rcomm = ar.txt.rstrip()
                cmd = "git merge-base @ @{u}"
                rc = await ar.run1(cmd, cwd=worktree)
                if rc == 0:
                    bcomm = ar.txt.rstrip()
                    # print('lcomm', lcomm)
                    # print('rcomm', rcomm)
                    # print('bcomm', bcomm)
                    if lcomm == rcomm:
                        print("up-to-date")
                        Dh2 = 1
                    elif lcomm == bcomm:
                        print("need-to-pull")
                        Dh2 = 3
                    elif rcomm == bcomm:
                        print("need-to-push")
                        Dh2 = 2
                    else:
                        print("diverged")
                        Dh2 = 4
    if Dh2 is not None:
        if Dh2 == 1:
            await rdhset(Di, Dh2)
        return Dh2, Dh2 > 1 and Dh2 != Dh1
    return Dh1, True


class GitOps(OpBase):
    async def __call__(self):
        from edge import findEdge

        print("Gitbackup")
        tc = 0
        fc = 0
        s = ""
        anyd = False
        di, si = self.npl1
        e = findEdge(di, si)
        if e.bctck():
            s += "l"
            anyd = True
        if e.rbctck():
            s += "r"
            anyd = True
        if not anyd:
            return tc, fc
        wt = self.opts["wt"]
        if "add" in self.opts:
            rc = await ar.run2("git add -A .", cwd=wt)
            if rc == 0:
                tc += 1
            else:
                fc += 1
        if "commit" in self.opts:
            rc = await ar.run2("git commit -a -m pybak", cwd=wt)
            if rc == 0 or rc == 1:
                tc += 1
            else:
                print("git commit rc:", rc)
                fc += 1
        if "pull" in self.opts and "r" in s:
            rmt = self.opts.get("rmt")
            if rmt == "local" or (await netup()):
                rc = await ar.run2("git pull " + rmt + " master", cwd=wt)
                if rc == 0:
                    tc += 1
                else:
                    fc += 1
        if "push" in self.opts and "l" in s:
            rmt = self.opts.get("rmt")
            if rmt == "local" or (await netup()):
                rc = await ar.run2("git push " + rmt + " master", cwd=wt)
                if rc == 0:
                    tc += 1
                else:
                    fc += 1
        if fc == 0 and tc > 0:
            di, si = self.npl1
            e = findEdge(di, si)
            if "l" in s:
                e.clr()
            if "r" in s:
                e.rclr()
        return tc, fc
