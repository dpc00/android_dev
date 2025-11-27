__all__ = ['blog-split26']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['tesz'])
Js('use strict')
var.put('tesz', Js(0.066))
pass


# Add lib to the module scope
blog-split26 = var.to_python()