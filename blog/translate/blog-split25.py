__all__ = ['blog-split25']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['set_handler'])
Js('use strict')
@Js
def PyJs_set_0_(obj, prop, val, this, arguments, var=var):
    var = Scope({'obj':obj, 'prop':prop, 'val':val, 'this':this, 'arguments':arguments, 'set':PyJs_set_0_}, var)
    var.registers(['prop', 'obj', 'val', 'oval'])
    var.put('oval', var.get('obj').get(var.get('prop')))
    var.get('obj').put(var.get('prop'), var.get('val'))
    if ((var.get('val')!=var.get('oval')) and (var.get('prop')==Js('num'))):
        var.get('et').callprop('dispatchEvent', var.get('Event').create((var.get('obj').get('name')+Js('-changed'))))
    return Js(True)
PyJs_set_0_._set_name('set')
var.put('set_handler', Js({'set':PyJs_set_0_}))
pass


# Add lib to the module scope
blog-split25 = var.to_python()