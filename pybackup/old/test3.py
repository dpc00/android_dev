import json

try:
    import xmlrpclib  # Python 2
except ImportError:
    import xmlrpc.client as xmlrpclib  # Python 3

pypi = xmlrpclib.ServerProxy("http://pypi.python.org/pypi")

packages = pypi.browse(["Programming Language :: Python :: 3"])

n = 0
pkgs = {}

with open("/sdcard/Documents/pypi-packages.txt", "w") as fh:
    for nm, v in packages:
        rd = pypi.release_data(nm, v)
        if (
            rd is not None
            and "keywords" in rd
            and rd["keywords"] is not None
            and "union-find" in rd["keywords"]
        ):
            if nm in pkgs:
                if v > pkgs[nm]:
                    pkgs[nm] = v
            else:
                pkgs[nm] = v
                fh.write(nm)
                fh.write(" ")
                fh.write(v)
                fh.write("\n")
                json.dump(rd, fh, indent=4)
                fh.write("\n")
                n += 1
                if n >= 250:
                    break
