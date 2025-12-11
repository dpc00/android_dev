"""
Created on Jul 27, 2016

@author: libraryuser
"""

from Dir import Dir
from FileCmp import FileCmp


# from File import File
class DirCmp(dict):
    def __init__(self, dir1, dir2):
        super(DirCmp, self).__init__()
        self["dir1"] = dir1
        self["dir2"] = dir2

    def __missing__(self, key):
        if key == "files" or key == "dirs" or key == "match":
            self.scan(False)
            if key in self:
                return self[key]
            else:
                if key == "files" or key == "dirs":
                    return {"copy": [], "delete": [], "match": []}
                else:
                    return False
        else:
            return 0

    def scan(self, recurse=False):
        self["files"] = {"copy": [], "delete": [], "match": []}
        self["dirs"] = {"copy": [], "delete": [], "match": []}
        self["match"] = True

        def hl1(dl1, dl2, icopy, idel, imatch, clazz):
            for run in dl1.keys():
                if run not in dl2:
                    icopy.append(dl1[run])
                else:
                    imatch.append(clazz(dl1[run], dl2[run]))
            for f2 in dl2.keys():
                if f2 not in dl1:
                    idel.append(dl2[f2])
            if len(icopy) > 0 or len(idel) > 0:
                self["match"] = False

        hl1(
            self["dir1"]["files"],
            self["dir2"]["files"],
            self["files"]["copy"],
            self["files"]["delete"],
            self["files"]["match"],
            FileCmp,
        )
        hl1(
            self["dir1"]["dirs"],
            self["dir2"]["dirs"],
            self["dirs"]["copy"],
            self["dirs"]["delete"],
            self["dirs"]["match"],
            DirCmp,
        )

        im = self["files"]["match"]
        ic = self["files"]["copy"]
        for i in range(len(im) - 1, -1, -1):
            df1 = im[i]  # FileCmp
            if not df1["match"]:
                im.pop(i)
                ic.append(df1["file1"])
        if len(self["files"]["copy"]) > 0 or len(self["files"]["delete"]) > 0:
            self["match"] = False

        if recurse:
            im = self["dirs"]["match"]
            ic = self["dirs"]["copy"]
            for i in range(len(im)):
                im[i].scan(recurse)
                self["match"] &= im[i]["match"]


if __name__ == "__main__":
    import utils
    import os

    sda = utils.establish()
    rd = "GitRepos\\tools"
    td1 = os.path.join(sda[0], rd)
    dir1 = Dir.fromPath(td1)

    sda = sda[1:]
    for td2 in sda:
        td3 = os.path.join(td2, rd)
        dir2 = Dir.fromPath(td3)
        dc1 = DirCmp(dir1, dir2)
        dc1.scan(True)
