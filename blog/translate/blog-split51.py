__all__ = ['blog-split51']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['me'])
@Js
def PyJsHoisted_me_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get('tblexists')(Js('monthly'))
PyJsHoisted_me_.func_name = 'me'
var.put('me', PyJsHoisted_me_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split51 = var.to_python()