__all__ = ['blog-split52']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['mtbl'])
@Js
def PyJsHoisted_mtbl_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['mex'])
    var.put('mex', var.get('me')())
    if (var.get('mex') and var.get('dirty4')):
        pass
    else:
        if var.get('mex').neg():
            var.get('sql')(var.get('mtbl_cs'))
            var.put('dirty4', Js(True))
    return var.get('mex')
PyJsHoisted_mtbl_.func_name = 'mtbl'
var.put('mtbl', PyJsHoisted_mtbl_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split52 = var.to_python()