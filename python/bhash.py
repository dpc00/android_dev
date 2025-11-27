from pathlib import Path, PosixPath
from struct import pack, unpack
from hashlib import blake2b


def bhu(ho, it):
    from dirlist import DE

    def iu(it):
        for itit in it:
            bhu(ho, itit)

    bhuf = {
        bytes: lambda it: ho.update(it),
        int: lambda it: ho.update(pack('i', it)),
        float: lambda it: ho.update(pack('f', it)),
        str: lambda it: ho.update(it.encode()),
        Path: lambda it: ho.update(it.__bytes__()),
        PosixPath: lambda it: ho.update(it.__bytes__()),
        tuple: iu,
        set: iu,
        list: iu,
        DE: lambda it: iu((it.nm, it.sz, it.mt, it.md5))
    }
    try:
        bhuf[type(it)](it)
    except KeyError:
        print(type(it), '??')

# flattened list blake2b with integer result
def bhash(it):
    ho = blake2b(digest_size=4)
    bhu(ho, it)
    rv = unpack('i', ho.digest())
    return rv[0]

