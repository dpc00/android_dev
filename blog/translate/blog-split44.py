__all__ = ['blog-split44']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['iee'])
@Js
def PyJsHoisted_iee_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get('tblexists')(Js('inc_exp'))
PyJsHoisted_iee_.func_name = 'iee'
var.put('iee', PyJsHoisted_iee_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split44 = var.to_python()