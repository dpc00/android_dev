__all__ = ['blog-split29']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['uc'])
Js('use strict')
var.put('uc', Js(0.0))
pass


# Add lib to the module scope
blog-split29 = var.to_python()