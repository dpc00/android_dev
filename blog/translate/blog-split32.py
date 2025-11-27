__all__ = ['blog-split32']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers([])
Js('use strict')
@Js
def PyJs_anonymous_0_(percent, options, this, arguments, var=var):
    var = Scope({'percent':percent, 'options':options, 'this':this, 'arguments':arguments}, var)
    var.registers(['options', 'percent'])
    var.get('prompt')(Js('#'), (((Js('App.UpdateProgressBar(\x0c')+var.get('percent'))+Js('\x0c'))+var.get('options')))
PyJs_anonymous_0_._set_name('anonymous')
var.get('app').put('UpdateProgressBar', PyJs_anonymous_0_)
pass


# Add lib to the module scope
blog-split32 = var.to_python()