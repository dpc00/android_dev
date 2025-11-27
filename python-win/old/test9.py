from pathlib import Path
from os import walk

from config import path, srcs, tagid

si = tagid('js-tools')

p = path(srcs, si)


def getfl(p):
    print(str(p))
    fl = []
    try:
        if p.is_file():
            fl.append(p)
            return fl
        for pth, dirs, files in walk(p, topdown=True):
            for f in files:
                fl.append(Path(pth, f).relative_to(p))
        return fl
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    for si in srcs:
        p = path(srcs, si)
        fl = getfl(p)
        fl = sorted(fl)
        print(fl)
