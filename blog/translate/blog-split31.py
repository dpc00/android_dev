__all__ = ['blog-split31']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['uspop'])
Js('use strict')
var.put('uspop', Js(324459463.0))
pass


# Add lib to the module scope
blog-split31 = var.to_python()