__all__ = ['blog-split54']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['ncs'])
@Js
def PyJsHoisted_ncs_(d, this, arguments, var=var):
    var = Scope({'d':d, 'this':this, 'arguments':arguments}, var)
    var.registers(['d'])
    return var.get('nc')(var.get('d')).callprop('toLocaleString', var.get('undefined'), Js({'minimumFractionDigits':Js(2.0),'maximumFractionDigits':Js(2.0)}))
PyJsHoisted_ncs_.func_name = 'ncs'
var.put('ncs', PyJsHoisted_ncs_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split54 = var.to_python()