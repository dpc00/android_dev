'''
Created on Jul 1, 2016

@author: Phil
'''
import os
import stat

import fcstats
import utils


# fs, path
def lstat(p):
    try:
        rv = os.lstat(p)
        return (None, rv)
    except Exception as e:
        return (e, None)


def checkStats(s):
    return True

def rmDir(p):
    try:
        os.rmdir(p)
        fcstats.fcstats['ddel'] += 1
        return (None, p)
    except Exception as e:
        utils.errlog(e)
        return (e, None)


def delFile(f):
    (err1, stats) = lstat(f)
    if err1:
        utils.errlog(err1)
        return (err1, None)
    else:
        try:
            os.unlink(f)
            fcstats.fcstats['fdel'] += 1
            fcstats.fcstats['bdel'] += stats.st_size
            return (None, stats.st_size)
        except Exception as e:
            utils.errlog(e)
            return (e, None)

def fileExists(fp):
    (err1, stats) = lstat(fp)
    if err1:
        if type(err1) is FileNotFoundError:
            return (None, False)
        else:
            utils.errlog(err1)
            return (err1, None)
    else:
        mode = stats.st_mode
        return (None, stat.S_ISREG(mode) and not stat.S_ISLNK(mode))


def dirExists(fp):
    (err1, stats) = lstat(fp)
    if err1:
        if type(err1) is FileNotFoundError:
            return (None, False)
        else:
            utils.errlog(err1)
            return (err1, None)
    else:
        mode = stats.st_mode
        return (None, stat.S_ISDIR(mode) and not stat.S_ISLNK(mode))


def insert(f, stats, memo):
    mode = stats.st_mode
    if not stat.S_ISLNK(mode):
        if stat.S_ISREG(mode):
            memo['files'][f] = {
                'mtime': stats.st_mtime,
                'size': stats.st_size
            }
        else:
            if stat.S_ISDIR(mode):
                memo['dirs'][f] = {
                    'mtime': stats.st_mtime
                }

rd_cache = {}

def readDir(p):
    if p in rd_cache.keys():
        return (None, rd_cache[p])
    else:
        try:
            rv = os.listdir(p)
            if len(rd_cache) > 130:
                for i in range(len(rd_cache.keys())//2):
                    for k in rd_cache.keys():
                        del rd_cache[k]
                        break
            rd_cache[p] = rv
            return (None, rv)
        except Exception as e:
            utils.errlog(e)
            return (e, None)

rs_cache = {}

def readStats(p):
    if p in rs_cache.keys():
        return (None, rs_cache[p])
    else:
        try:
            rv = os.lstat(p)
            # rv = os.listdir(p)
            if len(rs_cache) > 130:
                for _ in range(len(rs_cache.keys())//2):
                    for k in rs_cache.keys():
                        del rs_cache[k]
                        break
            rs_cache[p] = rv
            return (None, rv)
        except Exception as e:
            utils.errlog(e)
            return (e, None)

def dget(dp):
    (err1, fl) = readDir(dp)
    if err1:
        return (err1, None)
    else:
        memo = {
            'p': dp,
            'files': {},
            'dirs': {}
        }
        for de in fl:
            fdp = os.path.join(dp, de)
            (err2, stats) = readStats(fdp)
            if err2:
                # print(str(err2))
                # return (err2, None)
                # insert(de, None, memo)
                pass
            else:
                insert(de, stats, memo)
        return (None, memo)

def filesList(p, es):
    (err1, dgv) = dget(p)
    if err1:
        return (err1, None)
    else:
        if es is None or len(es) == 0:
            return (None, dgv['files'])
        else:
            files = {}
            for f in dgv['files'].keys():
                if os.path.splitext(f)[1].lower() in es:
                    files[f] = dgv['files'][f]
            return (None, files)

def dirsList(p):
    (err1, dgv) = dget(p)
    if err1:
        return (err1, None)
    else:
        return (None, dgv['dirs'])

def mkDirs(dr, mode):
    dirPath = os.path.normpath(dr)
    if mode is None:
        mode = int('0777')
    try:
        os.makedirs(dirPath, mode, True)
    except Exception as e:
        utils.errlog(e)
        return (e, False)
    return (None, True)

# fl = filesList('e:\\Projects\\tools', {'.js'})
# print(fl)

# dl = dirsList('C:\\')
# print(dl)