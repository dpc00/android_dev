__all__ = ['blog-split16']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['et'])
Js('use strict')
var.put('et', var.get('EventTarget').create())
pass


# Add lib to the module scope
blog-split16 = var.to_python()