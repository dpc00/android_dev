import bisect
import datetime
import os
from pathlib import Path

import asyncrun as ar
import config
from de import DE, FSe

dexs = {
    ".cargo",
    ".cache",
    ".git",
    "node_modules",
    "__pycache__",
    ".ropeproject",
    ".ruff_cache",
    ".mypyproject",
    ".mypy_cache",
    ".vite",
    ".yarnclean",
    "storage",
}


def cull_DEs(des):
    des[:] = [
        de
        for de in des
        if not any(sd for sd in de.nm.parent.parts if sd in config.dexs)
    ]


def cull_files(files, pt):
    files[:] = [
        pt(f)
        for f in files
        if not any(sd for sd in f.parent.parts if sd in config.dexs)
    ]


def cull_dirs(dirs, pt):
    dirs[:] = [pt(d) for d in dirs if not isbaddir(pt(d))]


def isbaddir(dir):
    return dir in config.dexs or dir in dexs


class FileList:
    def __new__(cls, sd, **kwargs):
        cls = RemoteFileList if sd.isremote else LocalFileList
        self = object.__new__(cls)
        return self

    def __init__(self, sd) -> None:
        self.sd = sd
        super().__init__()


class LocalFileList(FileList):
    def __init__(self, sd, **kwargs) -> None:
        super().__init__(sd)

    def getfl_str_fp(self, fp: str):
        from collections import deque

        q = deque()
        q.append(fp)

        while True:
            try:
                fp2 = q.popleft()
                # print(fp2)
                with os.scandir(fp2) as di:
                    for it1 in di:
                        if it1.is_file():
                            yield it1
                        elif not it1.is_symlink() and not isbaddir(it1.name):
                            q.append(it1.path)

            except IndexError:
                break

    def getfl(self):
        return self.getfl_str_fp(str(self.sd))

    def getdll(self):  # local-source
        import config

        config.dl1_cs += 1
        st = []
        for it in self.getfl():
            it1 = Path(it.path).relative_to(self.sd)
            try:
                fs = it.stat()
                it2 = fs.st_size
                it3 = fs.st_mtime_ns
                it3 = config.ns_trunc2ms(it3)
            except FileNotFoundError as exc:
                print(exc)
                it2 = 0
                it3 = 0
            fse = FSe(it2, it3)
            bisect.insort(st, DE(it1, fse), key=lambda de: de.nm)

        return st


class RemoteFileList(FileList):
    def __init__(self, sd, **kwargs) -> None:
        super().__init__(sd, **kwargs)

    def getfl(self, sd):
        import json

        cmd = 'rclone lsjson "' + str(sd) + '" --recursive --files-only '
        rc, txt = ar.run1(cmd)
        if rc == 0:
            return json.loads(txt)
        if rc == 3:
            return []
        return None

    def getdll(self):  # remote-source
        import config

        config.dl2_cs += 1
        # print('getdll1', di, str(td))
        st = []
        for it in self.getfl(self.sd):
            # TODO: use Path
            it1 = Path(it["Path"])
            it2 = it["Size"]
            it3 = it["ModTime"][:-1] + "-00:00"
            it3 = datetime.datetime.fromisoformat(it3).timestamp()
            it3 = config.ts_trunc2ms(it3)
            fse = FSe(it2, it3)
            bisect.insort(st, DE(it1, fse), key=lambda de: de.nm)

        return st


if __name__ == "__main__":
    pass
