__all__ = ['blog-split58']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['set_color'])
@Js
def PyJsHoisted_set_color_(o, this, arguments, var=var):
    var = Scope({'o':o, 'this':this, 'arguments':arguments}, var)
    var.registers(['o'])
    try:
        var.get('o').callprop('SetBackColor', Js('white'))
    except PyJsException as PyJsTempException:
        PyJsHolder_65_54931369 = var.own.get('e')
        var.force_own_put('e', PyExceptionToJs(PyJsTempException))
        try:
            pass
        finally:
            if PyJsHolder_65_54931369 is not None:
                var.own['e'] = PyJsHolder_65_54931369
            else:
                del var.own['e']
            del PyJsHolder_65_54931369
    try:
        var.get('o').callprop('SetTextColor', Js('black'))
    except PyJsException as PyJsTempException:
        PyJsHolder_65_26629434 = var.own.get('e')
        var.force_own_put('e', PyExceptionToJs(PyJsTempException))
        try:
            pass
        finally:
            if PyJsHolder_65_26629434 is not None:
                var.own['e'] = PyJsHolder_65_26629434
            else:
                del var.own['e']
            del PyJsHolder_65_26629434
PyJsHoisted_set_color_.func_name = 'set_color'
var.put('set_color', PyJsHoisted_set_color_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split58 = var.to_python()