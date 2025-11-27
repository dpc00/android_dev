import atexit
import functools
import json
import os
import re
import sqlite3
from subprocess import Popen, PIPE
import utils

loaded = False
usedb = False

drives = None

@functools.total_ordering
class Drive():
    __slots__ = ['_db', 'capacity', 'driveletter', 'filesystem', 'freespace', 'label', 'serialnumber', 'rt']
    def __init__(self):
        from Dir import Dir
#         self._db = None
        self.capacity = None
        self.driveletter = None
        self.filesystem = None
        self.freespace = None
        self.label = None
        self.serialnumber = None
        self.rt = Dir(self, '')
    def __lt__(self, other):
        return self.label < other.label
    def __eq__(self, other):
        return self.label == other.label
    def __hash__(self):
        try:
            return self.serialnumber
        except AttributeError as e:
            utils.errlog(e)
    def __str__(self):
        ps = 'Disk'
        try:
            ps += ' ' + self.label
            ps += ' (' + self.driveletter + ':)'
            ps += ' ' + '{:0>8X}'.format(self.serialnumber & 0xFFFFFFFF)
        except AttributeError as e:
            utils.errlog(e)
        return ps
    @property
    def contents(self):
        utils.errlog(Exception('sought contents from Drive object'))
        return None
    @property
    def path(self):  # Drive
        rv = self.driveletter
        if len(rv) == 1:
            rv += ':'
        return rv
    def dbFN(self):
        from Dir import fromPath
        # dsn1 = int('667AB765', 16) # CODE0
        # dbdrive = driveFromSN(dsn1)
        dbd = self.path + os.path.sep + '.sync'
        fn = dbd + os.path.sep + '{:0>8X}.sqlite'.format(self.serialnumber)
        # TODO: !!!!
        # fromPath(dbd).create()
        return fn
    def createTable(self):
        c1 = self.db
        c2 = c1.cursor()
        # cmd = 'DROP TABLE IF EXISTS ENTRY'
        # c2.execute(cmd)
        cmd = '''
            CREATE TABLE IF NOT EXISTS `Entry` (
                `PD`        TEXT,
                `Name`      TEXT,
                `MTime`     REAL,
                `Size`      REAL,
                `Digest`    TEXT,
                `ID`        TEXT,
                PRIMARY KEY(`PD`, `Name`)
            );'''
        c2.execute(cmd)
        c1.commit()
        c2.close()
#     @property
#     def db(self):
#         if self._db is None:
#             self._db = sqlite3.connect(self.dbFN())
#             if self._db is not None:
#                 c2 = self._db.cursor()
#                 c2.execute('PRAGMA journal_mode=MEMORY')
#                 rv = c2.fetchone()
#                 if rv[0] != 'memory':
#                     utils.errlog('error setting journal_mode: ' + repr(rv))
#                 self.createTable()
#                 def f1():
#                     if self._db is not None:
#                         self._db.commit()
#                         self._db.close()
#                 atexit.register(f1)
#         return self._db
    
def driveletterFromVL(vl):
    global drives
    for d1 in drives.values():
        try:
            if d1.label.lower() == vl.lower():
                return d1.driveletter + ':'
        except AttributeError as e:
            utils.errlog(e)
    return None

def driveFromSN(sn):  # by driveletter
    global drives
    for d1 in drives.values():
        try:
            if d1.serialnumber == sn:
                return d1
        except AttributeError as e:
            utils.errlog(e)
    return None
def driveFromVL(vl):  # by label
    global drives
    for d1 in drives.values():
        try:
            if d1.label.lower() == vl.lower():
                return d1
        except AttributeError as e:
            utils.errlog(e)
    return None

def driveFromDL(dl):  # by label
    global drives
    for d1 in drives.values():
        try:
            if d1.driveletter.lower() == dl.lower():
                return d1
        except AttributeError as e:
            utils.errlog(e)
    return None

def getWMIDrives():
    global drives
    fl = ['capacity', 'driveletter', 'filesystem', 'freespace', 'label', 'serialnumber']
    fin = [True, False, False, True, False, True]
    fo = []
    #              330952704    System Reserved  -2008134104   '
    # F:           4109750272   CODE             -1906067864   '
    def fieldno(fn):
        for i in range(len(fl)):
            if fn == fl[i]:
                return i
    def field(l, fn):
        i = fieldno(fn)
        n1 = fo[i]
        n2 = fo[i + 1]
        ft = l[n1:n2]
        return ft.rstrip().decode('utf-8')

    with Popen('wmic VOLUME get ' + ','.join(fl), shell=True, stdout=PIPE, universal_newlines=False) as proc:
        so = proc.stdout.read()
        lns = re.split(b'[\r\n]+', so);
        
        def findFOs():
            hl = lns[0].decode()
            i = 0
            j = 0
            sw = True
            while i < len(hl):
                if sw:
                    if hl[i] != ' ' and (i == 0 or hl[i - 1] == ' '):
                        fo.append(i)
                        j += 1
                        sw = not sw
                    i += 1
                else:
                    if hl[i] == ' ' and hl[i - 1] != ' ':
                        sw = not sw
                    else:
                        i += 1
            fo.append(len(hl))
        findFOs()
        
        for i in range(1, len(lns)):
            l = lns[i]
            # utils.log(l)
            if len(l) > 0:
                fn = fl[5]
                v = field(l, fn)
                if len(v):
                    if fin[5]:
                        try:
                            v = int(v)
                        except ValueError:
                            # utils.errlog(e)
                            pass
                new = False
                d1 = driveFromSN(v)
                if not d1:
                    d1 = Drive()
                    new = True
                for j in range(len(fl)):
                    fn = fl[j]
                    v = field(l, fn)
                    if len(v):
                        if fin[j]:
                            try:
                                v = int(v)
                                setattr(d1, fn, v)
                            except ValueError:
                                # utils.errlog(e)
                                pass
                        else:
                            setattr(d1, fn, v)
                try:
                    if d1.driveletter is not None:
                        d1.driveletter = d1.driveletter[0]
                        if new:
                            drives[d1.serialnumber] = d1
                        if drives[d1.serialnumber].rt is not None:
                            if drives[d1.serialnumber].rt.pd != d1:
                                raise ValueError('drive root points to wrong Disk')
                except AttributeError:
                    # utils.errlog(e)
                    pass

def initDurus():
    pass
#         global new, restarting, tablesdeleted
#         if DB.conn is None:
#     global conn
#     dbdir = findDL('CODE0') + '\\.sync'
#     dbfn = 'CODE0-CODEN.durus'
#     d1 = fromPath(dbdir)
#     d1.create()
#     f1 = findFile(d1, dbfn) 
#     if not f1.exists():
#         new = True
#         tablesdeleted = True
#     conn = Connection(FileStorage(f1.path))

def getDrives(udb=False):
    global loaded, drives, usedb
    usedb = udb
    if usedb:
        if not loaded:
            drives = {}
            def chkDrives():
                for d1 in drives.values():
                    rt = d1.rt
                    if rt:
                        if rt.pd is not d1:
                            utils.errlog(ValueError('drive root points to wrong Disk'))
                            rt.pd = d1
            def printDrives():
                for d1 in drives.values():
                    ds = ''
                    if hasattr(d1, 'serialnumber'):
                        if d1.serialnumber is not None:
                            ds += '{:08X}  '.format(d1.serialnumber & 0xFFFFFFFF)
                    else:
                        if d1.serialnumber is not None:
                            ds += '{:8}  '.format('')
                    if hasattr(d1, 'driveletter'):
                        if d1.driveletter is not None:
                            ds += '({:1}:)  '.format(d1.driveletter)
                    else:
                        if d1.driveletter is not None:
                            ds += '({})  '.format('no drive letter')
                    if hasattr(d1, 'label'):
                        if d1.label is not None:
                            ds += '{:12}'.format(d1.label)
                    else:
                        if d1.label is not None:
                            ds += '{:12} '.format('')
                    utils.log(ds)
            chkDrives()
            getWMIDrives()
            printDrives()
            loaded = True
    else:
        if drives is None:
            drives = {}
        getWMIDrives()
        loaded = True
    return drives

# def saveDrives():
#     global loaded, drives, contents, usedb
#     from Dir import fromPath, dbHash
#     for d1 in [driveFromVL('CODE0'), driveFromVL('CODE1')]:
#         # utils.log('exporting database ' + sfn1)
#         c1 = d1.db
#         c2 = c1.cursor()
#         # cmd1 = 'DELETE FROM ENTRY'
#         # c2.execute(cmd1)
#         # c1.commit()
#         rt1 = d1.rt
#         cmd2 = "UPDATE Entry SET MTime=?, Size=?, Digest=?, ID=? WHERE PD=? and Name=?"
#         def f1(d2):
#             utils.log('saving ' + str(d2))
#             p1 = dbHash(d2.pd)
#             p2 = d2.name
#             p3 = d2.mtime
#             p4 = d2.size
#             p5 = json.dumps(d2.digest)
#             p6 = dbHash(d2)
#             utils.log()
#             c2.execute(cmd2, (p3, p4, p5, p6, p1, p2))
#             p1 = p6
#             p6 = None
#             for de in d2.contents.files:
#                 p2 = de.name
#                 p3 = de.mtime
#                 p4 = de.size
#                 p5 = de.digest
#                 c2.execute(cmd2, (p3, p4, p5, p6, p1, p2))
#             c1.commit()
#         rt1.dfWalk(f1)
#         c2.close()
