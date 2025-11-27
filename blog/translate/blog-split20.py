__all__ = ['blog-split20']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['losz'])
Js('use strict')
var.put('losz', Js(0.075))
pass


# Add lib to the module scope
blog-split20 = var.to_python()