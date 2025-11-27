__all__ = ['blog-split34']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['dallow_calc'])
@Js
def PyJsHoisted_dallow_calc_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['da'])
    var.put('da', ((var.get('cashb').get('num')+var.get('dxb').get('num'))/var.get('maxdl').get('num')))
    var.get('dallow').get('te').callprop('SetText', var.get('ncs')(var.get('da')))
    var.get('dallow').callprop('save')
PyJsHoisted_dallow_calc_.func_name = 'dallow_calc'
var.put('dallow_calc', PyJsHoisted_dallow_calc_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split34 = var.to_python()