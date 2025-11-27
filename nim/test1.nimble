# Package

version       = "0.1.0"
author        = "Donald Chitester"
description   = "A new awesome nimble package"
license       = "MIT"
srcDir        = "src"
bin           = @["test1"]

backend       = "c"

# Dependencies

requires "pythonpathlib"
requires "nim >= 1.0.2"

