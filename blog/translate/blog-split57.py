__all__ = ['blog-split57']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['SaveNumber'])
@Js
def PyJsHoisted_SaveNumber_(name, num, this, arguments, var=var):
    var = Scope({'name':name, 'num':num, 'this':this, 'arguments':arguments}, var)
    var.registers(['name', 'num'])
    var.get('sql')(Js('UPDATE nums SET (num,ts)=(?,?) WHERE name=?'), Js([var.get('num'), var.get('Date').create().callprop('toISOString'), var.get('name')]))
PyJsHoisted_SaveNumber_.func_name = 'SaveNumber'
var.put('SaveNumber', PyJsHoisted_SaveNumber_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split57 = var.to_python()