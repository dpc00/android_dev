__all__ = ['blog-split49']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['lts'])
@Js
def PyJsHoisted_lts_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['res'])
    var.put('res', var.get('sql')(Js('SELECT ts FROM currentc ORDER BY ts DESC')))
    return var.get('res').get('rows').callprop('item', var.get('uc')).get('ts')
PyJsHoisted_lts_.func_name = 'lts'
var.put('lts', PyJsHoisted_lts_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split49 = var.to_python()