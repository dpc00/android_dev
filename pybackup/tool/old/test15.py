from ctypes import *
from ctypes.util import find_library

dlln = find_library("rtlsdr")

dll = CDLL(dlln)

# "/data/data/com.termux/files/usr/lib/librtlsdr.so"

print(dll)
print(dll.rtlsdr_get_device_count)
print(dll.rtlsdr_get_device_count())
