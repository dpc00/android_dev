__all__ = ['blog-split04']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['bsz'])
Js('use strict')
var.put('bsz', Js(0.125))
pass


# Add lib to the module scope
blog-split04 = var.to_python()