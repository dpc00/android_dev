__all__ = ['blog-split09']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['dbfn'])
Js('use strict')
var.put('dbfn', Js('Finance.db'))
pass


# Add lib to the module scope
blog-split09 = var.to_python()