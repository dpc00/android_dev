
import os
import shutil

import utils

def cpf2(source, target):
    try:
        rv = shutil.copy2(source, target)
        return (None, rv)
    except Exception as e:
        utils.errlog(e)
        return (e, None)

def copyFile(source, target):
    (t_dn, _) = os.path.split(target)
    tmp = os.path.join(t_dn, utils.makename1(8) + '.tmp')
    try:
        sz = os.lstat(source).st_size
        shutil.copy2(source, tmp)
        os.replace(tmp, target)
        return (None, sz)
    except Exception as e:
        utils.errlog(e)
        return (e, None)


if __name__ == "__main__":
    import copy_flash
    copy_flash.fcopy1()
