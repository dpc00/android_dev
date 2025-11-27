__all__ = ['blog-split10']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['dirty2'])
Js('use strict')
var.put('dirty2', Js(False))
pass


# Add lib to the module scope
blog-split10 = var.to_python()