__all__ = ['blog-split41']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['dtbl'])
@Js
def PyJsHoisted_dtbl_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['dex'])
    var.put('dex', var.get('de')())
    if (var.get('dex') and var.get('dirty3')):
        pass
    else:
        if var.get('dex').neg():
            var.get('sql')(var.get('dtbl_cs'))
            var.put('dirty3', Js(True))
    return var.get('dex')
PyJsHoisted_dtbl_.func_name = 'dtbl'
var.put('dtbl', PyJsHoisted_dtbl_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split41 = var.to_python()