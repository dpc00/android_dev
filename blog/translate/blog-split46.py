__all__ = ['blog-split46']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['inec_calc'])
@Js
def PyJsHoisted_inec_calc_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['res1'])
    var.put('res1', (var.get('davg').get('num')-var.get('dallow').get('num')))
    var.get('inec').get('te').callprop('SetText', var.get('ncs')((var.get('res1')*var.get('maxdl').get('num'))))
    var.get('inec').callprop('save')
PyJsHoisted_inec_calc_.func_name = 'inec_calc'
var.put('inec_calc', PyJsHoisted_inec_calc_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split46 = var.to_python()