__all__ = ['blog-split08']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['db'])
Js('use strict')
var.put('db', var.get(u"null"))
pass


# Add lib to the module scope
blog-split08 = var.to_python()