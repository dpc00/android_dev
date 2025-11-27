__all__ = ['blog-split30']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['updated'])
Js('use strict')
var.put('updated', Js(False))
pass


# Add lib to the module scope
blog-split30 = var.to_python()