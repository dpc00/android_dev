__all__ = ['blog-split39']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['de'])
@Js
def PyJsHoisted_de_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get('tblexists')(Js('daily'))
PyJsHoisted_de_.func_name = 'de'
var.put('de', PyJsHoisted_de_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split39 = var.to_python()