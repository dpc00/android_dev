import ctypes
import ctypes.wintypes as wintypes

def copy_file(src, dst):
    rc = ctypes.windll.kernel32.CopyFileW(src, dst, False)
    if rc==0:
        gle = ctypes.windll.kernel32.GetLastError()
        if gle!=0:
            we = WindowsError(gle, ctypes.FormatError(gle))
            we.src = src
            we.dst = dst
            raise we
    return rc