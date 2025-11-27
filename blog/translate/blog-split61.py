__all__ = ['blog-split61']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['tblexists'])
@Js
def PyJsHoisted_tblexists_(nm, this, arguments, var=var):
    var = Scope({'nm':nm, 'this':this, 'arguments':arguments}, var)
    var.registers(['nm', 'res'])
    var.put('res', var.get('sql')(Js("SELECT COUNT() AS cnt FROM sqlite_master WHERE type='table' AND name=?"), Js([var.get('nm')])))
    return (var.get('res').get('rows').callprop('item', Js(0.0)).get('cnt')>Js(0.0))
PyJsHoisted_tblexists_.func_name = 'tblexists'
var.put('tblexists', PyJsHoisted_tblexists_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split61 = var.to_python()