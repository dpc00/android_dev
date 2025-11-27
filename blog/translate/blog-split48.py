__all__ = ['blog-split48']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['log_balances'])
@Js
def PyJsHoisted_log_balances_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.get('sql')(Js('INSERT INTO currentc (ts, cash, fs, dx) VALUES (?,?,?,?)'), Js([var.get('Date').create().callprop('toISOString'), var.get('cashb').get('num'), var.get('fsb').get('num'), var.get('dxb').get('num')]))
    var.put('dirty2', Js(True))
    (var.put('uc',Js(var.get('uc').to_number())+Js(1))-Js(1))
PyJsHoisted_log_balances_.func_name = 'log_balances'
var.put('log_balances', PyJsHoisted_log_balances_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split48 = var.to_python()