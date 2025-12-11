from ctypes import Structure
from ctypes import byref
from ctypes import pointer
import ctypes

import ctypes.wintypes as wintypes
import utils

# Windows FILE_ATTRIBUTE constants for interpreting the
# FIND_DATA.dwFileAttributes member
FILE_ATTRIBUTE_READONLY = 1
FILE_ATTRIBUTE_HIDDEN = 2
FILE_ATTRIBUTE_SYSTEM = 4
FILE_ATTRIBUTE_DIRECTORY = 16
FILE_ATTRIBUTE_ARCHIVE = 32
FILE_ATTRIBUTE_DEVICE = 64
FILE_ATTRIBUTE_NORMAL = 128
FILE_ATTRIBUTE_TEMPORARY = 256
FILE_ATTRIBUTE_SPARSE_FILE = 512
FILE_ATTRIBUTE_REPARSE_POINT = 1024
FILE_ATTRIBUTE_COMPRESSED = 2048
FILE_ATTRIBUTE_OFFLINE = 4096
FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 8192
FILE_ATTRIBUTE_ENCRYPTED = 16384
FILE_ATTRIBUTE_INTEGRITY_STREAM = 32768
FILE_ATTRIBUTE_VIRTUAL = 65536
FILE_ATTRIBUTE_NO_SCRUB_DATA = 131072

OPEN_EXISTING = 3
MAX_PATH = 260

# Numer of seconds between 1601-01-01 and 1970-01-01
SECONDS_BETWEEN_EPOCHS = 11644473600
MILLISECONDS_BETWEEN_EPOCHS = 11644473600000
MICROSECONDS_BETWEEN_EPOCHS = 11644473600000000
HUNDREDNANOSECONDS_BETWEEN_EPOCHS = 116444736000000000

INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
INVALID_FILE_ATTRIBUTES = ctypes.c_void_p(-1).value
ERROR_FILE_NOT_FOUND = 2
ERROR_NO_MORE_FILES = 18
IO_REPARSE_TAG_SYMLINK = 0xA000000C
FAT32_GRANULARITY = 20000000

# GetLastError = kernel32.GetLastError


class FILETIME(Structure):
    _fields_ = [("dwLowDateTime", wintypes.DWORD), ("dwHighDateTime", wintypes.DWORD)]


# WIN32_FIND_DATAW
class DE(Structure):
    _fields_ = [
        ("dwFileAttributes", wintypes.DWORD),
        ("ftCreationTime", FILETIME),
        ("ftLastAccessTime", FILETIME),
        ("ftLastWriteTime", FILETIME),
        ("nFileSizeHigh", wintypes.DWORD),
        ("nFileSizeLow", wintypes.DWORD),
        ("dwReserved0", wintypes.DWORD),
        ("dwReserved1", wintypes.DWORD),
        ("cFileName", wintypes.WCHAR * MAX_PATH),
        ("cAlternateFileName", wintypes.WCHAR * 20),
    ]

    # s[0] = td.cFileName
    # s[1] = (td.ftLastWriteTime.dwHighDateTime << 32 | td.ftLastWriteTime.dwLowDateTime) / 10000000 - SECONDS_BETWEEN_EPOCHS
    # s[2] = td.nFileSizeHigh << 32 | td.nFileSizeLow
    # s[3] = td.dwFileAttributes
    # s[4] = td.dwReserved0
    def __init__(self):
        self._mtime = None

    @property
    def name(self):
        return self.cFileName

    @property
    def mtime(self):
        if self._mtime is None:
            self._mtime = (
                (
                    (self.ftLastWriteTime.dwHighDateTime << 32)
                    | (self.ftLastWriteTime.dwLowDateTime & 0xFFFFFFFF)
                )
                - HUNDREDNANOSECONDS_BETWEEN_EPOCHS
            ) / 10000000
        return self._mtime

    @property
    def size(self):
        return (self.nFileSizeHigh << 32) | (self.nFileSizeLow & 0xFFFFFFFF)

    @property
    def attrib(self):
        return self.dwFileAttributes

    @property
    def res0(self):
        return self.dwReserved0

    def isdir(self):
        return not (
            self.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT != 0
            and self.res0 == IO_REPARSE_TAG_SYMLINK
        ) and (self.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY != 0)

    def isfile(self):
        return not (
            self.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT != 0
            and self.res0 == IO_REPARSE_TAG_SYMLINK
        ) and (self.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY == 0)

    def issymlink(self):
        return (
            self.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT != 0
            and self.res0 == IO_REPARSE_TAG_SYMLINK
        )

    def __str__(self):
        return "{:30} {:25} {:12} {:4} {:4}".format(
            self.name, self.mtime, self.size, self.attrib, self.res0
        )

    def __lt__(self, other):
        return (
            self.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY
            > other.attrib & FILE_ATTRIBUTE_DIRECTORY
        ) and (self.name.lower() < other.name.lower())

    # def __eq__(self, other):
    #     return (self.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY == other.attrib & FILE_ATTRIBUTE_DIRECTORY) and (self.name == other.name)


# FindData_Ptr = ctypes.POINTER(DE)


def fileExists(fspec):
    fa = ctypes.windll.kernel32.GetFileAttributesW(fspec)
    if fa == INVALID_FILE_ATTRIBUTES:
        return False
    if (fa & FILE_ATTRIBUTE_REPARSE_POINT != 0) or (fa & FILE_ATTRIBUTE_DIRECTORY != 0):
        return False
    return True


def dirExists(fspec):
    fa = ctypes.windll.kernel32.GetFileAttributesW(fspec)
    if fa == INVALID_FILE_ATTRIBUTES:
        return False
    if (fa & FILE_ATTRIBUTE_REPARSE_POINT != 0) or (fa & FILE_ATTRIBUTE_DIRECTORY == 0):
        return False
    return True


def scan_dir(fspec, isentry=False):
    gle = 0
    if not isentry:
        fspec += "\\*"
    de = DE()
    h = ctypes.windll.kernel32.FindFirstFileW(fspec, byref(de))
    if h == INVALID_HANDLE_VALUE or h == -1:
        gle = ctypes.windll.kernel32.GetLastError()
        if gle != 0:
            we = WindowsError(gle, ctypes.FormatError(gle))
            we.filename = fspec
            raise we
    if h == ERROR_FILE_NOT_FOUND:
        return
    try:
        rc = 1
        while rc != 0:
            yield [
                de.name,
                de.mtime,
                de.size,
                de.attrib,
                de.res0,
                de.isdir(),
                de.isfile(),
            ]
            de._mtime = None
            rc = ctypes.windll.kernel32.FindNextFileW(h, byref(de))
            if rc == 0:
                gle = ctypes.windll.kernel32.GetLastError()
                if gle == ERROR_NO_MORE_FILES or gle == 0:
                    break
                we = WindowsError(gle, ctypes.FormatError(gle))
                we.filename = fspec
                raise we
    finally:
        rc = ctypes.windll.kernel32.FindClose(h)
        if rc == 0:
            utils.log("rc: " + str(rc))
            gle = ctypes.windll.kernel32.GetLastError()
            if gle != 0:
                we = WindowsError(gle, ctypes.FormatError(gle))
                we.filename = fspec
                raise we


if __name__ == "__main__":
    from Drive import getDrives

    getDrives()
    dp = utils.prjDir("py-test")
    utils.log(dp)
    for ses in sorted(list(scan_dir(dp, False))):
        try:
            utils.writedata("\n")
            utils.writedata(str(ses))
        except Exception as e:
            utils.errlog(e)
