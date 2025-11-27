import atexit
import ctypes
import ctypes.wintypes as wintypes
import os
import threading
from ctypes import Structure
from ctypes import byref

import utils
from Dir import findPath, Dir, fromPath, NEEDS_SCAN
from File import File

CN_FILE_NAME = 0x00000001
CN_DIR_NAME = 0x00000002
CN_ATTRIBUTES = 0x00000004
CN_SIZE = 0x00000008
CN_LAST_WRITE = 0x00000010
CN_SECURITY = 0x00000100

fncflags = CN_FILE_NAME | CN_DIR_NAME | CN_ATTRIBUTES | CN_SIZE | CN_LAST_WRITE | CN_SECURITY

CNE_ADDED = 0x00000001
CNE_REMOVED = 0x00000002
CNE_MODIFIED = 0x00000003
CNE_RENAMED_OLD_NAME = 0x00000004
CNE_RENAMED_NEW_NAME = 0x00000005

atxt = {CNE_ADDED: 'Added',
        CNE_REMOVED: 'Removed',
        CNE_MODIFIED: 'Modified',
        CNE_RENAMED_OLD_NAME: 'Old Name',
        CNE_RENAMED_NEW_NAME: 'New Name'
        }

INVALID_HANDLE_VALUE = ctypes.c_int(-1).value
INFINITE = ctypes.c_int(-1).value
WAIT_FAILED = ctypes.c_void_p(-1)
TRUE = wintypes.BOOL(True)

FILE_LIST_DIRECTORY = 1
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000

OPEN_EXISTING = 3

FILE_SHARE_READ = 1
FILE_SHARE_WRITE = 2
FILE_SHARE_DELETE = 4

MAX_PATH = 32767

ERROR_NOTIFY_ENUM_DIR = 0x3FE
ERROR_OPERATION_ABORTED = 0x3E3

class FILE_NOTIFY_INFORMATION(Structure):
    _fields_ = [
        ("NextEntryOffset", wintypes.DWORD),
        ("Action", wintypes.DWORD),
        ("FileNameLength", wintypes.DWORD),
        ("FileName", wintypes.WCHAR * MAX_PATH)
    ]

    def __str__(self):
        s = '{:3d} {:8s} {:3d} {:s}'.format(self.NextEntryOffset, atxt[self.Action], self.FileNameLength >> 1,
                                            self.FileName[:self.FileNameLength >> 1])
        return s


blen = wintypes.DWORD(MAX_PATH * 2 + 3 * 4).value

# TODO:  Where's the 4K buffer at???
# TODO: Why the 32K file path name length??

def cns(cd):
    global blen
    bret = wintypes.DWORD(0)
    buffer = FILE_NOTIFY_INFORMATION()
    hdir = ctypes.windll.kernel32.CreateFileW(
        cd.path,
        wintypes.DWORD(FILE_LIST_DIRECTORY).value,
        wintypes.DWORD(FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE).value,
        wintypes.LPVOID(0).value,
        wintypes.DWORD(OPEN_EXISTING).value,
        wintypes.DWORD(FILE_FLAG_BACKUP_SEMANTICS).value,
        wintypes.HANDLE(0).value)

    if hdir != INVALID_HANDLE_VALUE:
        def ch(hdir):
            ctypes.windll.kernel32.CancelIoEx(hdir, None)
        atexit.register(ch, hdir)
        while True:
            rv = ctypes.windll.kernel32.ReadDirectoryChangesW(hdir,
                                                              buffer,
                                                              wintypes.DWORD(blen).value,
                                                              wintypes.BOOL(True).value,
                                                              wintypes.DWORD(fncflags).value,
                                                              byref(bret),
                                                              wintypes.LPVOID(0).value,
                                                              wintypes.LPVOID(0).value
                                                              )
            if rv == 0:
                gle = ctypes.windll.kernel32.GetLastError()
                if gle != 0:
                    if gle == ERROR_OPERATION_ABORTED:
                        ctypes.windll.kernel32.CloseHandle(hdir)
                        break
                    we = WindowsError(gle, ctypes.FormatError(gle))
                    we.filename = cd.path
                    utils.errlog(we)
            if rv != ERROR_NOTIFY_ENUM_DIR:  # overflow
                if bret != 0:
                    p1 = ctypes.cast(byref(buffer, 0), ctypes.POINTER(FILE_NOTIFY_INFORMATION)).contents
                    # utils.log(str(p1))
                    while True:
                        yield (p1.Action, p1.FileName[:p1.FileNameLength >> 1], p1.NextEntryOffset)
                        if p1.NextEntryOffset != 0:
                            p1 = ctypes.cast(byref(p1, p1.NextEntryOffset),
                                             ctypes.POINTER(FILE_NOTIFY_INFORMATION)).contents
                            # utils.log(str(p1))
                        else:
                            break
            # buffer = FILE_NOTIFY_INFORMATION()


def dmonitor(cd):
    def dmt(cd):
        stash = None
        for (a, f, no) in cns(cd):
            try:
                ci = findPath(os.path.join(cd.path, f))
                if isinstance(ci, File):
                    utils.log('File {:12s} {:<66s} {:5}'.format(atxt[a], ci.path, no))
                    ci.update()
                    if a == CNE_RENAMED_OLD_NAME:
                        stash = {
                            'oldci': ci
                        }
                elif isinstance(ci, Dir):
                    utils.log('Dir  {:12s} {:<66s} {:5}'.format(atxt[a], ci.path, no))
                    ci.update()
                    if a == CNE_RENAMED_OLD_NAME:
                        stash = {
                            'oldci': ci
                        }
                else:
                    if a == CNE_RENAMED_NEW_NAME:
                        if stash:
                            utils.log(
                                '???? {:12s} {:<66s} {:5} stash: {}'.format(atxt[a], os.path.join(cd.path, f), no,
                                                                            stash['oldci'].path)
                            )
                        else:
                            utils.log('???? {:12s} {:<66s} {:5} nostash'.format(atxt[a], os.path.join(cd.path, f), no))
                    elif a == CNE_RENAMED_OLD_NAME:
                        utils.log('???? {:12s} {:<66s} {:5}'.format(atxt[a], os.path.join(cd.path, f), no))
                        ci = fromPath(os.path.join(cd.path, f))
                        if ci:
                            stash = {
                                'oldci': ci
                            }
                    elif a == CNE_ADDED:
                        utils.log('???? {:12s} {:<66s} {:5}'.format(atxt[a], os.path.join(cd.path, f), no))
                    elif a == CNE_MODIFIED:
                        utils.log('???? {:12s} {:<66s} {:5}'.format(atxt[a], os.path.join(cd.path, f), no))
                    elif a == CNE_REMOVED:
                        utils.log('???? {:12s} {:<66s} {:5}'.format(atxt[a], os.path.join(cd.path, f), no))

                    fp = os.path.join(cd.path, f)
                    pp = os.path.dirname(fp)
                    ci = findPath(pp)
                    if isinstance(ci, File):
                        pass
                    elif isinstance(ci, Dir):
                        ci.update()
                        ci._flags |= NEEDS_SCAN
                        ci.clearDigest2()
            except KeyError:
                utils.log('file change returned: ' + str(a) + ' ' + f + ' ' + str(no))

    t = threading.Thread(target=dmt, name='monitor of ' + cd.path, args=(cd,), daemon=True)
    t.start()

if __name__ == "__main__":
    pass
