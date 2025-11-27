__all__ = ['blog-split64']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['txtp'])
@Js
def PyJsHoisted_txtp_(txt, this, arguments, var=var):
    var = Scope({'txt':txt, 'this':this, 'arguments':arguments}, var)
    var.registers(['txt'])
    @Js
    def PyJs_anonymous_0_(a, c, this, arguments, var=var):
        var = Scope({'a':a, 'c':c, 'this':this, 'arguments':arguments}, var)
        var.registers(['a', 'c'])
        return (var.get('a')+var.get('c'))
    PyJs_anonymous_0_._set_name('anonymous')
    return var.get('txtpa')(var.get('txt')).callprop('reduce', PyJs_anonymous_0_, Js(0.0))
PyJsHoisted_txtp_.func_name = 'txtp'
var.put('txtp', PyJsHoisted_txtp_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split64 = var.to_python()