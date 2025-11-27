__all__ = ['blog-split45']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['ietbl'])
@Js
def PyJsHoisted_ietbl_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['iex'])
    var.put('iex', var.get('iee')())
    if (var.get('iex') and var.get('dirty2')):
        pass
    else:
        if var.get('iex').neg():
            var.get('sql')(var.get('ietbl_cs'))
            var.put('dirty2', Js(True))
    return var.get('iex')
PyJsHoisted_ietbl_.func_name = 'ietbl'
var.put('ietbl', PyJsHoisted_ietbl_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split45 = var.to_python()