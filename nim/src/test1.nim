# This is just an example to get you started. A typical binary package
# uses this file as the main entry point of the application.
import marshal
import os
import tables
import pythonpathlib


var paths: tables.Table[string, string] = initTable[string, string]()

when isMainModule:
    echo("Hello, World!")
    var s: PythonPath = Path("/sdcard/Android/data/com.zeropacketbrowser")
    paths["zeropacketbrowser"] = s.p
    echo(paths)
    echo(existsDir(s.p))
    var n: BiggestInt = 0
    for path in walkDirRec(s.p):
        n += getFileInfo(path).size
    echo(n)
    var s2 = $$paths
    echo(s2)
    echo("end")