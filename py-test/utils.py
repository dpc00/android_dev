'''
Created on Jun 27, 2016

@author: Phil
'''
import datetime
import math
import os
import random
import re
import subprocess
import sys

import json2
from Dos4 import Dos4


# var str = '%LOCALAPPDATA%\\Google\\Chrome\\Application'
def chop(txt):
    limit = 200
    if len(txt) <= limit:
        return txt
    else:
        l = []
        while len(txt) > limit:
            l.append(txt[:limit])
            txt = txt[limit:]
        if len(txt) > 0:
            l.append(txt)
    return '\n    '.join(l)


def expES(s):
    def repfn(mo):
        k = mo.group(0).replace('%', '')
        return os.environ[k]

    return re.sub('%([^%]+)%', repfn, s)


def prjDir(prj):
    s = '%FLASH0%\\Projects'
    if not prj is None and len(prj) > 0:
        s += '\\' + prj;
    return expES(s)


def gitDir(prj):
    return prjDir(prj) + '\\.git'


prjList = [
    'py-test',
    'tools',
    'scala-test',
    'DirSyncApp'
]

# print(expES('%LOCALAPPDATA%\\Google\\Chrome\\Application'))

# print(prjDir(prjList[0]))
# print(gitDir(prjList[0]))

# print(chop('expES(%LOCALAPPDATA%\\Google\\Chrome\\Application)expES(%LOCALAPPDATA%\\Google\\Chrome\\Application)'))

ccol = 0
cln = 0


def writedata(data):
    global ccol, cln
    if len(data) > 0:
        hnl = False
        hret = False
        s = str(data)
        try:
            sys.stdout.write(data)
        except UnicodeEncodeError as e:
            pass
        if s.count('\r') > 0:
            hret = True
        if s.count('\n') > 0:
            hnl = True
        if hret:
            ccol = 0
        else:
            ccol += len(s)
        if hnl:
            cln += 1


# writedata('abcde + 134556')
# writedata('fghij + 4356456')
# writedata('\r')
# writedata('                                                      z')
# writedata('\n')

def writedataindent(data):
    global ccol, cln
    if len(data) > 0:
        sa = re.split('[\n]', str(data))
        # sa = [i for i in sa if len(i) > 0]
        for l in sa:
            print('\t' + l, end='\n')
            cln += 1
            ccol = 0
            # print('',end='\n')


# writedataindent('Now is the time for\r\nall good men to \r\ncome to the aid of \r\ntheir country.')

def eo(s1, s2):
    anl = False
    if not s1 is None:
        writedataindent(s1)
        anl = True
    if not s2 is None:
        writedataindent(s2)
        anl = True
    if anl:
        writedata('\n')


def log(s=''):
    if ccol > 0:
        writedata('\n')
    if isinstance(s, str):
        if len(s):
            writedata(s)
    else:
        writedata(str(s))


def errlog(e, inf=None):
    log(str(e))
    if inf:
        log(inf)
    with open('err.log', 'a') as ef:
        ef.write(str(datetime.datetime.now()) + ' ')
        ub = 36
        lb = 0
        for i in range(ub, lb, -1):
            try:
                ef.write(sys._getframe(i).f_code.co_name)
                if i > lb:
                    ef.write('|')
                else:
                    ef.write(':')
            except:
                pass
        ef.write(str(e))
        if inf:
            ef.write(inf)
        ef.write('\n')


def flog(lbl, e):
    log(str(e))
    with open('ferr.log', 'a') as ef:
        ef.write(lbl)
        ef.write(': ')
        ef.write(str(e))
        ef.write('\n')


# log('this is a log entry.')
def dos2(cmd2, args):
    cmd = ['cmd.exe', '/c']
    if not cmd2 is None:
        cmd = cmd + re.split(' ', cmd2)
    if not args is None:
        cmd = cmd + args
    dc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t1 = dc.stdout.decode()
    t2 = dc.stderr.decode()
    if len(t1) > 0 or len(t2) > 0:
        return [t1, t2]
    else:
        return []


# rva = dos2('dir',['\\','/w'])
# eo(rva[0],rva[1])

def pathfind(s1):
    s2 = s1.lower()
    for pe1 in os.environ['PATH'].split(';'):
        pe2 = pe1.lower()
        if pe2.find(s2) > -1:
            print(pe1)


# pathfind('python')

def progfind(pn1):
    s1, s2 = os.path.splitext(pn1.lower())
    files = []
    for pe1 in os.environ['PATH'].split(';'):
        if pe1 == '':
            continue
        pe2 = pe1.lower()
        try:
            for name in os.listdir(pe2):
                pn = os.path.join(pe2, name)
                if os.path.isfile(pn):
                    s3, s4 = os.path.splitext(name)
                    if s3 == s1:
                        if s2 == '':
                            for x in ['', '.acm', '.ax', '.bat', '.cmd', '.cpl', '.dll', '.drv', '.efi', '.exe', '.mui',
                                      '.ocx', '.scr', '.sys', '.tsp']:
                                if x == s4:
                                    files.append(pn)
                        else:
                            if s4 == s2:
                                files.append(pn)
        except Exception as e:
            errlog(str(e))
    for pn in files:
        print(pn)
    return files


def setEnv(k, v):
    cfn = expES('%FLASH0%\\Projects\\py-test\\plaunch_flash_CODE0.json')
    splobj = json2.readConfig(cfn)
    splobj['env'][k] = v
    os.environ[k] = v
    json2.writeConfig(splobj, cfn)


def makename1(n):
    s = ''
    while len(s) < n:
        j = math.floor(random.random() * 2)
        if j == 0:
            sc = ord('A')
        else:
            sc = ord('a')
        s += chr(sc + math.floor(random.random() * 26))
    return ''.join(sorted(s, key=lambda s: s.lower()))


def makename2():
    return 'CODE\\' + datetime.date.today().weekday()


def establish():
    if 'FLASH0' in os.environ:
        src = expES('%FLASH0%\\')
        dest = []
        if 'FLASH1' in os.environ:
            dest.append(expES('%FLASH1%\\'))
        if 'FLASH2' in os.environ:
            dest.append(expES('%FLASH2%\\'))
        if 'FLASH3' in os.environ:
            dest.append(expES('%FLASH3%\\'))
        if 'FLASH4' in os.environ:
            dest.append(expES('%FLASH4%\\'))
        if 'FLASH5' in os.environ:
            dest.append(expES('%FLASH5%\\'))
        if 'FLASH6' in os.environ:
            dest.append(expES('%FLASH6%\\'))
        if 'FLASH7' in os.environ:
            dest.append(expES('%FLASH7%\\'))
        if len(dest) > 0:
            rv = [src] + dest
            return rv


def fixedD(num, n):
    s = str(num)
    while len(s) < n:
        s = ' ' + s
    return s


def pProcess(s):
    hasSpaces = False
    s2 = ''
    for c in s:
        if c == '%':
            s2 += '^'
        if c == ' ':
            hasSpaces = True
        s2 += c
    if hasSpaces:
        s2 = '\"' + s2 + '\"'
    return s2


def shortcut(fn, target, params=None, wdir=None, icon=None, iindex=None, desc=None):
    a = ['/c', '\\Programs\\Utils\\Shortcut.exe']
    if not fn is None:
        a += ['/F:' + fn]
    a += ['/A:C']
    if not target is None:
        a += ['/T:' + pProcess(target)]
    if not params is None:
        a += ['/P:' + params]
    if not wdir is None:
        a += ['/W:' + pProcess(wdir)]
    if not icon is None and not iindex is None:
        a += ['/I:' + pProcess(icon) + ',' + str(iindex)]
    if not desc is None:
        a += ['/D:' + desc]
    Dos4({
        'cmd': 'cmd.exe',
        'args': a,
        'echo': True,
        'oprint': True,
        'shell': True
    })

def lnkdir():
    # smd1 = expES("%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs")
    smd2 = expES("%FLASH0%\\.lnk")
    return smd2

def lnk1():
    sfn = lnkdir() + "\\VSCodePortable.lnk"
    tfn = "%FLASH0%\\.bat\\vscodeportable.bat"
    ifn = "%FLASH0%\\PortableApps\\VSCodePortable\\VSCodePortable.exe"
    params = "."
    wdir = "%FLASH0%\\Projects\\py-test"
    shortcut(
        sfn,
        tfn,
        icon=ifn,
        iindex=0,
        wdir=wdir,
        desc="Visual Studio Code Portable",
        params=params
    )

def lnk2():
    sfn = lnkdir() + "\\Eclipse.lnk"
    tfn = "%FLASH0%\\.bat\\eclipse.bat"
    ifn = "%FLASH0%\\Programs\\eclipse\\eclipse.exe"
    # params = ""
    wdir = "%FLASH0%\\Projects"
    shortcut(
        sfn,
        tfn,
        icon=ifn,
        iindex=0,
        wdir=wdir,
        desc="Eclipse Neon"
    )

def lnk3():
    sfn = lnkdir() + "\\Repo.py-test.lnk"
    tfn = "%FLASH0%\\.bat\\gitk.bat"
    ifn = "%FLASH0%\\Programs\\Git\\cmd\\gitk.exe"
    # params = ""
    wdir = "%FLASH0%\\GitRepos\\py-test"
    shortcut(
        sfn,
        tfn,
        icon=ifn,
        iindex=0,
        wdir=wdir,
        desc="Py-Test Repo"
    )

def lnk4():
    sfn = lnkdir() + "\\jEdit.lnk"
    tfn = "%FLASH0%\\.bat\\jedit.bat"
    ifn = "%FLASH0%\\PortableApps\\jEditPortable\\jEditPortable.exe"
    # params = ""
    wdir = "%FLASH0%\\Projects"
    shortcut(
        sfn,
        tfn,
        icon=ifn,
        iindex=0,
        wdir=wdir,
        desc="jEdit"
    )

def lnk5():
    sfn = lnkdir() + "\\PyCharm.lnk"
    tfn = "%FLASH0%\\.bat\\pycharm.bat"
    ifn = "%FLASH0%\\Programs\\PyCharm\\pycharm.exe"
    # params = ""
    wdir = "%FLASH0%\\Projects"
    shortcut(
        sfn,
        tfn,
        icon=ifn,
        iindex=0,
        wdir=wdir,
        desc="PyCharm"
    )

def lnk6():
    sfn = lnkdir() + "\\SublimeText.lnk"
    tfn = "%FLASH0%\\.bat\\sublimetext.bat"
    ifn = "%FLASH0%\\Programs\\SublimeText\\sublime_text.exe"
    # params = ""
    wdir = "%FLASH0%\\Projects"
    shortcut(
        sfn,
        tfn,
        icon=ifn,
        iindex=0,
        wdir=wdir,
        desc="Sublime Text 3"
    )

def lnk7():
    sfn = lnkdir() + "\\ComodoCleaner.lnk"
    tfn = "%FLASH0%\\.bat\\cce.bat"
    ifn = "%FLASH0%\\Programs\\Utils\\CCE\\CCE.exe"
    # params = ""
    wdir = "%FLASH0%\\"
    shortcut(
        sfn,
        tfn,
        icon=ifn,
        iindex=0,
        wdir=wdir,
        desc="Comodo Cleaner"
    )

def lnk9():
    sfn = lnkdir() + "\\ProcessExplorer.lnk"
    tfn = "%FLASH0%\\.bat\\procexp.bat"
    ifn = "%FLASH0%\\Programs\\Utils\\procexp.exe"
    # params = ""
    wdir = "%FLASH0%\\"
    shortcut(
        sfn,
        tfn,
        icon=ifn,
        iindex=0,
        wdir=wdir,
        desc="Process Explorer"
    )

def lnk10():
    sfn = lnkdir() + "\\WinDirStat.lnk"
    tfn = "%FLASH0%\\.bat\\windirstatportable.bat"
    ifn = "%FLASH0%\\Programs\\Utils\\WinDirStatPortable\\WinDirStatPortable.exe"
    # params = ""
    wdir = "%FLASH0%\\"
    shortcut(
        sfn,
        tfn,
        icon=ifn,
        iindex=0,
        wdir=wdir,
        desc="WinDirStat"
    )

def lnk11():
    sfn = lnkdir() + "\\Python.lnk"
    tfn = "%FLASH0%\\.bat\\python.bat"
    ifn = "%FLASH0%\\Programs\\Python36x64\\python.exe"
    # params = ""
    wdir = "%FLASH0%\\Projects\\py-test"
    shortcut(
        sfn,
        tfn,
        icon=ifn,
        iindex=0,
        wdir=wdir,
        desc="Python"
    )

def getSTPackage(pf='Package Control.sublime-package'):
    import urllib.request
    import os
    # import hashlib
    # h = '2915d1851351e5ee549c20394736b442' + '8bc59f460fa1548d1514676163dafc88'
    if not pf.endswith('.sublime-package'):
        pf += '.sublime-package'
    log('Getting Sublime Text package \'' + pf + '\'')
    # ipp = sublime.installed_packages_path()
    
    ipp = expES(r'%FLASH0%\PortableApps\SublimeText3Portable\App\SublimeText3\Data\Installed Packages')
    log(ipp)
    urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) )
    try:
        by = urllib.request.urlopen( 'http://packagecontrol.io/' + pf.replace(' ', '%20')).read()
        # dh = hashlib.sha256(by).hexdigest()
        # if dh != h:
        #   print('Error validating download (got %s instead of %s), please try manual install' % (dh, h))
        # else:
        with open(os.path.join(ipp, pf), 'wb' ) as run:
            run.write(by)
    except Exception as e:
        errlog(e)

if __name__ == "__main__":
    print(establish())
