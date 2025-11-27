__all__ = ['blog-split59']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['slow'])
@Js
def PyJsHoisted_slow_(f, this, arguments, var=var):
    var = Scope({'f':f, 'this':this, 'arguments':arguments}, var)
    var.registers(['f'])
    var.get('app').callprop('ShowProgress')
    var.get('f')()
    var.get('app').callprop('HideProgress')
PyJsHoisted_slow_.func_name = 'slow'
var.put('slow', PyJsHoisted_slow_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split59 = var.to_python()