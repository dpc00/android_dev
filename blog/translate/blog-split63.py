__all__ = ['blog-split63']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['tleft_calc'])
@Js
def PyJsHoisted_tleft_calc_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['tl', 'tf', 'tmp'])
    var.put('tf', (var.get('cashb').get('num')+var.get('dxb').get('num')))
    var.put('tl', (var.get('tf')/var.get('davg').get('num')))
    var.put('tmp', var.get('ncs')(var.get('tl')))
    var.get('tleft').get('te').callprop('SetText', var.get('tmp'))
    var.get('tleft').callprop('save')
PyJsHoisted_tleft_calc_.func_name = 'tleft_calc'
var.put('tleft_calc', PyJsHoisted_tleft_calc_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split63 = var.to_python()