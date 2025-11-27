__all__ = ['blog-split33']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['d2t'])
@Js
def PyJsHoisted_d2t_(dv, this, arguments, var=var):
    var = Scope({'dv':dv, 'this':this, 'arguments':arguments}, var)
    var.registers(['h', 'dv', 'd', 'm'])
    var.put('d', var.get('Math').callprop('floor', var.get('dv')))
    var.put('h', var.get('Math').callprop('floor', ((var.get('dv')*Js(24.0))%Js(24.0))))
    var.put('m', var.get('Math').callprop('round', ((var.get('dv')*(Js(24.0)*Js(60.0)))%Js(60.0))))
    return (((((var.get('d')+Js('d,'))+var.get('h'))+Js('h,'))+var.get('m'))+Js('m'))
PyJsHoisted_d2t_.func_name = 'd2t'
var.put('d2t', PyJsHoisted_d2t_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split33 = var.to_python()