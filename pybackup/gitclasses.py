import asyncrun as ar
import config
import gitops as go
import ldsv as ls
from sd import SD


class GitCmdFailure(Exception):
    pass


def gitcmd(cmd, wt):
    with go.rl:
        rc, txt = ar.run1(cmd, cwd=wt)
    if rc != 0:
        raise GitCmdFailure("gitcmd rc: " + str(rc) + cmd)
    return txt.rstrip()


class Local_Git_Mixin:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    @property
    def isremote(self):
        return False

    @property
    def SDh(self):
        if hasattr(self, "tag"):
            with ls.dl:
                if self.tag in config.LDhd:
                    return config.LDhd[self.tag]
        return 0

    @SDh.setter
    def SDh(self, val):
        if hasattr(self, "tag"):
            with ls.dl:
                config.LDhd[self.tag] = val
                ls.sev.put("ldhd")


class Remote_Git_Mixin:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    @property
    def isremote(self):
        return True

    @property
    def SDh(self):
        if hasattr(self, "tag") and self.tag in config.RDhd:
            return config.RDhd[self.tag]
        return 0

    @SDh.setter
    def SDh(self, val):
        if hasattr(self, "tag"):
            with ls.dl:
                config.RDhd[self.tag] = val
                ls.sev.put("rdhd")


class GitWT(SD, Local_Git_Mixin):
    def __init__(self, *args, **kwargs) -> None:
        for k, v2 in kwargs.items():
            setattr(self, k, v2)
        super().__init__(*args, **kwargs)

    def sdhck(self):
        print(type(self), 'sdhck')
        Dh1 = self.sdh_f()
        cmd = "git status --porcelain --untracked-files=all"
        rv = gitcmd(cmd, self)
        rv = rv.split("\n")
        rv = len([ln for ln in rv if len(ln) > 1 and ln[1] != " "])
        Dh2 = rv
        if rv == 0:
            self.sdhset(Dh2)
        elif Dh2 != Dh1:
            # print(rv)
            pass
        return (Dh2, rv > 0 and Dh2 != Dh1)


class GitIndex(SD, Local_Git_Mixin):
    def __init__(self, *args, **kwargs) -> None:
        for k, v2 in kwargs.items():
            setattr(self, k, v2)
        super().__init__(*args, **kwargs)

    def sdhck(self):
        print(type(self), 'sdhck')
        Dh1 = self.sdh_f()
        cmd = "git status --porcelain --untracked-files=all"
        rv = gitcmd(cmd, self)
        rv = rv.split("\n")
        rv = len([ln for ln in rv if len(ln) > 1 and ln[0] != " "])
        Dh2 = rv
        if rv == 0:
            self.sdhset(Dh2)
        elif Dh2 != Dh1:
            # print(rv)
            pass
        return (Dh2, rv > 0 and Dh2 != Dh1)


class GitRepo(SD, Local_Git_Mixin):
    def __init__(self, *args, **kwargs) -> None:
        for k, v2 in kwargs.items():
            setattr(self, k, v2)
        super().__init__(*args, **kwargs)

    def sdhck(self):
        print(type(self), 'sdhck')
        return self.gitck2()

    def gitck2(self):
        Dh1 = self.sdh_f()
        if Dh1 is None:
            Dh1 = 0
        rv = 0
        for rmt in self.rmts:
            cmd = "git rev-list --count origin/master..master"
            rv += int(gitcmd(cmd, self))
        Dh2 = rv
        if Dh2 == 0:
            self.sdhset(Dh2)
        return (Dh2, rv > 0 and Dh2 != Dh1)


class GitRemote(SD, Remote_Git_Mixin):
    def __init__(self, *args, **kwargs) -> None:
        for k, v2 in kwargs.items():
            setattr(self, k, v2)
        super().__init__(*args, **kwargs)

    def sdhck(self):
        print(type(self), 'sdhck')
        return self.gitremoteck()

    def tdhck(self):
        print(type(self), 'tdhck')
        return self.gitremoteck()

    def gitremoteck(self):
        Dh1 = self.sdh_f()
        Dh2 = None
        # print(Di, 'status here')
        cmd = ""
        try:
            cmd = "git branch master -u origin/master"
            gitcmd(cmd, self)
            cmd = "git remote update " + self.rmt
            gitcmd(cmd, self)
            cmd = "git rev-parse @"
            lcomm = gitcmd(cmd, self)
            cmd = "git rev-parse @{u}"
            rcomm = gitcmd(cmd, self)
            cmd = "git merge-base @ @{u}"
            bcomm = gitcmd(cmd, self)
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
        except GitCmdFailure as e:
            print(e)
        if Dh2 is not None:
            if Dh2 == 1:
                self.sdhset(Dh2)
            return (Dh2, Dh2 > 1 and Dh2 != Dh1)
        return (Dh1, True)
