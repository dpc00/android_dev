from hashlib import md5

import config


def md5sumf(Fn):
    if Fn.exists():
        # print("-md5sumf", str(Fn))
        ho = md5()
        with open(Fn, "rb") as fh:
            b = fh.read(1 << 15)
            while len(b) > 0:
                ho.update(b)
                b = fh.read(1 << 15)
        return ho.digest()
    return None


def fmd5f(fp, sz, mt, nh=None):
    import config
    from de import FSe

    d1 = v.fmd5hd
    if fp not in d1:  # new
        v.hf_dm += 1
        if nh is None:
            nh = md5sumf(fp)
            # pp('new fse, file md5')
        else:
            # pp('new fse, supplied md5')
            pass
        nfse = FSe(sz, mt, nh)
        d1[fp] = nfse
        v.hf_dirty = True
        return nfse
    else:  # existing
        v.hf_dh += 1
        ofse = d1[fp]
        if ofse.sz != sz or ofse.mt != mt:
            v.hf_stm += 1
            if ofse.sz != sz:
                # pp('size diff:', sz - ofse.sz)
                ofse.sz = sz
                v.hf_dirty = True
            if ofse.mt != mt:
                # pp('mt diff:', mt - ofse.mt)
                ofse.mt = mt
                v.hf_dirty = True
            if nh is not None:
                # pp('md5 furnished:', nh!=ofse.md5)
                ofse.md5 = nh
                v.hf_dirty = True
            else:
                nh = md5sumf(fp)
                # pp('md5 file hashed:', nh!=ofse.md5)
                ofse.md5 = nh
                v.hf_dirty = True
        else:
            v.hf_sth += 1
            if nh is not None:
                # pp('md5 update:', nh!=ofse.md5)
                ofse.md5 = nh
                v.hf_dirty = True
        return ofse
