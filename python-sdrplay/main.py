import ctypes

lib = ctypes.CDLL(r"C:\Program Files\SDRplay\API\x64\sdrplay_api.dll")

print(lib)

f = lib.sdrplay_api_ApiVersion

rv = ctypes.c_float()

if f(ctypes.pointer(rv)) == 0:
    print(rv.value)
else:
    print("error getting sdrplay api version")
    print(rv.value)
