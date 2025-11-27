import contextlib
import datetime as dt
from math import floor

import asyncrun as ar
import config
from edge import Edge
from netup import netup
from opbase import OpBase


def colored(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


def ar_run(cmd):
    opmsg = []
    statmsg = []
    with config.rclk:
        rc, txt, msglst = ar.run3(cmd)

    def f1():  # for ar_run3
        for m in msglst:
            if "operations" in m["source"]:
                opmsg.append(m)
            elif "stats" in m["source"]:
                statmsg.append(m)

    f1()
    return rc, txt, opmsg, statmsg


def chunk_from(s1, amt):
    s2 = set()
    for it in s1:
        s2.add(it)
        if len(s2) == amt:
            yield s2
            s2 = set()
    if len(s2):
        yield s2


class SFc:
    sc = 0
    fc = 0

    def __init__(self) -> None:
        pass

    def value(self):
        return (self.sc, self.fc)


def ts2st(ts):
    t2 = config.ts_trunc2ms(ts)
    t2 = dt.datetime.fromtimestamp(t2, tz=dt.timezone.utc)
    t2 = t2.isoformat()[:-6]
    return t2


def ftouch(di, si, td, lf, sfc):
    if netup():
        nt = ts2st(lf.i.mt)
        cmd = (
            'rclone touch -t"'
            + nt
            + '" "'
            + str(td / lf.nm)
            + '" --progress --no-create -v --use-json-log'
        )
        # cmd += ' --exclude ".git/**" --exclude "__pycache__/**"'
        print(cmd)
        rc, txt, opmsg, statmsg = ar_run(cmd)
        if rc == 0:
            for m in opmsg:
                # print(json.dumps(m, indent=4))
                if str(lf) == m["object"]:
                    if m["msg"].startswith("Updated modification time"):
                        sfc.sc += 1
            opmsg.clear()
            for m in statmsg:
                # print(json.dumps(m, indent=4))
                sfc.sc += m["stats"]["checks"]
            statmsg.clear()
            return True
        else:
            sfc.fc += 1
            opmsg.clear()
            statmsg.clear()
            print(txt)
    return False


def fsync(di, si, sd, td, sfc):
    if netup():
        # print('copy', sd, td)
        cmd = (
            'rclone copy "'
            + str(sd.parent)
            + '" "'
            + str(td.parent)
            + '" --include "'
            + str(td.name)
            + '" --progress --no-traverse -v --use-json-log'
        )
        # cmd += ' --exclude ".git/**" --exclude "__pycache__/**"'
        print(cmd)
        rc, txt, opmsg, statmsg = ar_run(cmd)
        if rc == 0:
            for m in opmsg:
                # print(json.dumps(m, indent=4))
                if str(td.name) == m["object"]:
                    if m["msg"].startswith("Copied"):
                        sfc.sc += 1
                    elif m["msg"].startswith("Updated modification time"):
                        sfc.sc += 1
            opmsg.clear()
            for m in statmsg:
                # print(json.dumps(m, indent=4))
                sfc.sc += m["stats"]["checks"]
                sfc.sc += m["stats"]["transfers"]
            statmsg.clear()
            return True
        else:
            sfc.fc += 1
            opmsg.clear()
            statmsg.clear()
            print(txt)
    return False


def fsynclm(di, si, sd, td, fl1, sfc):
    return all(fsyncl(di, si, sd, td, fl2, sfc) for fl2 in chunk_from(fl1, 10))


def fsyncl(di, si, sd, td, fl, sfc):
    cmd = 'rclone copy "'
    cmd += str(sd) + '" "'
    cmd += str(td) + '" '
    for fn in fl:
        cmd += '--include "' + str(fn.nm) + '" '
    cmd += "--progress --no-traverse -v --use-json-log"
    # cmd += '--exclude "**/.git/**/*" '
    # cmd += '--exclude "**/__pycache__/**/*" '
    # cmd += '--exclude "**/node_modules/**/*" '
    # cmd += '--log-file="rclone.log" '
    # cmd += "--use-json-log"
    if netup():
        # print("copy", sd, td, list(map(lambda de: str(de.nm), fl)))
        print(cmd)
        rc, txt, opmsg, statmsg = ar_run(cmd)
        if rc == 0:
            for m in opmsg:
                # print(json.dumps(m, indent=4))
                for f in fl:
                    if str(f.nm) == m["object"]:
                        if m["msg"].startswith("Copied"):
                            sfc.sc += 1
                        elif m["msg"].startswith("Updated modification time"):
                            sfc.sc += 1
            opmsg.clear()
            for m in statmsg:
                # print(json.dumps(m, indent=4))
                sfc.sc += m["stats"]["checks"]
                sfc.sc += m["stats"]["transfers"]
            statmsg.clear()
            return True
        else:
            sfc.fc += 1
            opmsg.clear()
            statmsg.clear()
            print(txt)
    return False


def fdel(di, si, sd, td, sfc):
    if netup():
        cmd = 'rclone delete "'
        cmd += str(td.parent)
        cmd += '" --include="' + td.name
        cmd += '" --progress -v --use-json-log'
        print(cmd)
        rc, txt, opmsg, statmsg = ar_run(cmd)
        if rc == 0:
            for m in opmsg:
                # print(json.dumps(m, indent=4))
                if str(td.name) == m["object"] and m["msg"].startswith("Deleted"):
                    sfc.sc += 1
            opmsg.clear()
            for m in statmsg:
                # print(json.dumps(m, indent=4))
                sfc.sc += m["stats"]["checks"]
                sfc.sc += m["stats"]["deletes"]
            statmsg.clear()
            return True
        else:
            sfc.fc += 1
            opmsg.clear()
            statmsg.clear()
            print(txt)
    return False


def fdellm(di, si, td, fl1, sfc):
    return all(fdell(di, si, td, fl2, sfc) for fl2 in chunk_from(fl1, 10))


def fdell(di, si, td, fl, sfc):
    cmd = 'rclone delete "'
    cmd += str(td) + '" '
    for fn in fl:
        cmd += '--include "' + str(fn.nm) + '" '
    cmd += "--progress -v --use-json-log"
    # cmd += '--log-file="rclone.log" '
    # cmd += "--use-json-log"
    if netup():
        # print("delete", td, list(map(lambda de: str(de.nm), fl)))
        print(cmd)
        rc, txt, opmsg, statmsg = ar_run(cmd)
        if rc == 0:
            for m in opmsg:
                # print(json.dumps(m, indent=4))
                for f in fl:
                    if str(f.nm) == m["object"] and m["msg"].startswith("Deleted"):
                        sfc.sc += 1
            opmsg.clear()
            for m in statmsg:
                # print(json.dumps(m, indent=4))
                sfc.sc += m["stats"]["checks"]
                sfc.sc += m["stats"]["deletes"]
            statmsg.clear()
            return True
        else:
            sfc.fc = len(fl)
            opmsg.clear()
            statmsg.clear()
            print(txt)
    return False


class BVars:
    def __init__(self, di, si, sfc) -> None:
        self.si = si
        self.di = di
        self.sd = config.src(si)
        self.td = config.tgt(di)
        self.src_dls = None
        self.dst_dls = None
        self.f2d = None
        self.f2c = None
        self.f2t = None
        self.sfc = sfc
        self.ac2 = 0

    def init2(self):
        self.src_dls = self.sd.Dlld()
        if self.src_dls is None:
            self.sfc.fc += 1
        self.dst_dls = self.td.Dlld()
        if self.src_dls is not None and self.dst_dls is not None:
            config.cull_DEs(self.src_dls)
            config.cull_DEs(self.dst_dls)
            self.f2d, self.f2c = config.dllcmp(self.dst_dls, self.src_dls)
        else:
            config.cull_DEs(self.src_dls)
            self.f2d = set()
            self.f2c = set(self.src_dls)
        self.f2t = set()

    def skip_matching(self):
        # handle slip through mismatched on times or more recent

        for rf in self.f2d.copy():
            for lf in self.f2c.copy():
                # TODO: use Path
                if rf.nm == lf.nm:  # names match
                    if rf.i.sz == lf.i.sz and rf.i.mt == lf.i.mt:  # sz,mt match
                        self.f2d.remove(rf)
                        self.f2c.remove(lf)
                    elif rf.i.sz == lf.i.sz:
                        if round(rf.i.mt) == round(lf.i.mt) or floor(rf.i.mt) == floor(
                            lf.i.mt
                        ):
                            self.f2d.remove(rf)
                            self.f2c.remove(lf)
                            self.f2t.add(lf)

    def do_touching(self):
        # TODO: use Path
        from findde import updateDEs

        cfpl = self.f2t.copy()
        if len(cfpl) == 0:
            return
        # print(cfp)
        for lf in cfpl:
            if ftouch(self.di, self.si, self.td, lf, self.sfc):
                self.ac2 += 1
                with contextlib.suppress(KeyError):
                    self.f2t.remove(lf)
        updateDEs(self.td, [str(de.nm) for de in cfpl])
        print("302 complete")

    def do_copying(self):
        # TODO: use Path

        cfpl = self.f2c.copy()
        if len(cfpl) == 0:
            return
        # print(cfp)
        if fsynclm(self.di, self.si, self.sd, self.td, cfpl, self.sfc):
            from findde import updateDEs

            for lf in cfpl:
                self.ac2 += 1
                with contextlib.suppress(KeyError):
                    self.f2c.remove(lf)

                for rf in self.f2d.copy():
                    if str(rf.nm) == str(lf.nm):
                        with contextlib.suppress(KeyError):
                            self.f2d.remove(rf)
            updateDEs(self.td, [str(de.nm) for de in cfpl])
            print("324 complete")

    def do_deletions(self):
        from findde import updateDEs

        cfpl = self.f2d.copy()
        if fdellm(self.di, self.si, self.td, cfpl, self.sfc):
            for rf in cfpl:  # do deletions
                self.ac2 += 1
                with contextlib.suppress(KeyError):
                    self.f2d.remove(rf)

        updateDEs(self.td, [str(de.nm) for de in cfpl])
        print("337 complete")

    def list_deletions(self):
        cfpl = self.f2d.copy()
        print("potential deletions", cfpl)


class CSCopy(OpBase):
    def __init__(self, npl1, npl2, opts={}) -> None:
        super().__init__(npl1, npl2, opts)
        self.sfc = SFc()

    def ischanged(self, e: Edge):
        return e.chk_ct() or e.rchk_ct()

    def __call__(self):
        from edge import Edge, findEdge
        from status import onestatus

        di, si = self.npl1
        print("CSCopy", si + "->" + di)
        if not netup():
            self.sfc.fc += 1
            return self.sfc.value()
        e: Edge = findEdge(di, si)
        if e.chk_ct():
            bv = BVars(di, si, self.sfc)
            bv.init2()
            if bv.sfc.fc == 0:
                print("raw", len(bv.f2d), "todelete", len(bv.f2c), "tocopy")
                bv.skip_matching()
                print("skip", len(bv.f2d), "todelete", len(bv.f2c), "tocopy")
            # if bv.sfc.fc == 0:
            # bv.do_touching()
            if bv.sfc.fc == 0:
                bv.do_copying()
            if bv.sfc.fc == 0:
                if "delete" in self.opts and self.opts["delete"] and len(bv.f2d):
                    bv.do_deletions()
            if bv.ac2:
                pass
        if self.sfc.fc == 0:
            e.clr()
            e.rclr()
        if self.sfc.sc > 0 and di in config.srcs:
            onestatus(di)
        return self.sfc.value()
