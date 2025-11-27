__all__ = ['blog-split38']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['dbps'])
@Js
def PyJsHoisted_dbps_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['fn2', 'fn1'])
    var.put('fn1', (var.get('app').callprop('GetPrivateFolder', Js(''))+Js('/../databases')))
    if (var.get('fn1').get('length')!=Js(0.0)):
        var.put('fn1', Js('/'), '+')
    var.put('fn1', var.get('dbfn'), '+')
    var.put('fn2', Js('/sdcard/projects/blog'))
    if (var.get('fn2').get('length')!=Js(0.0)):
        var.put('fn2', Js('/'), '+')
    var.put('fn2', var.get('dbfn'), '+')
PyJsHoisted_dbps_.func_name = 'dbps'
var.put('dbps', PyJsHoisted_dbps_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split38 = var.to_python()