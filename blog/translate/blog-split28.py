__all__ = ['blog-split28']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['tsz'])
Js('use strict')
var.put('tsz', Js(0.045))
pass


# Add lib to the module scope
blog-split28 = var.to_python()