__all__ = ['blog-split53']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['nc'])
@Js
def PyJsHoisted_nc_(d, this, arguments, var=var):
    var = Scope({'d':d, 'this':this, 'arguments':arguments}, var)
    var.registers(['d'])
    return (var.get('Math').callprop('round', (var.get('d')*Js(100.0)))/Js(100.0))
PyJsHoisted_nc_.func_name = 'nc'
var.put('nc', PyJsHoisted_nc_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split53 = var.to_python()