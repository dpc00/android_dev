__all__ = ['blog-split12']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['dirty4'])
Js('use strict')
var.put('dirty4', Js(False))
pass


# Add lib to the module scope
blog-split12 = var.to_python()