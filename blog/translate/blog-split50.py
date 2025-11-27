__all__ = ['blog-split50']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['maxdl_calc'])
@Js
def PyJsHoisted_maxdl_calc_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['dxd', 'cashd'])
    var.put('cashd', var.get('dl')(Js(5.0), Js(28.0)))
    var.put('dxd', var.get('dl')(Js(5.0), Js(3.0)))
    var.get('maxdl').get('te').callprop('SetText', var.get('ncs')(var.get('Math').callprop('max', var.get('cashd'), var.get('dxd'))))
    var.get('maxdl').put('num', var.get('ncs')(var.get('Math').callprop('max', var.get('cashd'), var.get('dxd'))))
PyJsHoisted_maxdl_calc_.func_name = 'maxdl_calc'
var.put('maxdl_calc', PyJsHoisted_maxdl_calc_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split50 = var.to_python()