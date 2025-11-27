__all__ = ['blog-split62']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['teot'])
@Js
def PyJsHoisted_teot_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['v'])
    var.put('v', var.get(u"this").get('mvar'))
    var.get('app').callprop('ShowPopup', (Js(' v.name: ')+var.get('v').get('name')))
PyJsHoisted_teot_.func_name = 'teot'
var.put('teot', PyJsHoisted_teot_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split62 = var.to_python()