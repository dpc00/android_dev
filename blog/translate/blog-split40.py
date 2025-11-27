__all__ = ['blog-split40']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['dl'])
@Js
def PyJsHoisted_dl_(m, dom, this, arguments, var=var):
    var = Scope({'m':m, 'dom':dom, 'this':this, 'arguments':arguments}, var)
    var.registers(['em', 'ms', 'days', 'nd', 'dom', 't1', 't2', 'md', 'm', 'cd', 'mm', 'mh'])
    var.put('cd', var.get('Date').create())
    var.put('nd', var.get('Date').create())
    var.put('ms', var.get('Math').callprop('round', ((var.get('dom')*((Js(24.0)*Js(60.0))*Js(60.0)))%Js(60.0))))
    var.put('mm', var.get('Math').callprop('floor', ((var.get('dom')*(Js(24.0)*Js(60.0)))%Js(60.0))))
    var.put('mh', var.get('Math').callprop('floor', ((var.get('dom')*Js(24.0))%Js(24.0))))
    var.get('nd').callprop('setSeconds', var.get('ms'))
    var.get('nd').callprop('setMinutes', var.get('mm'))
    var.get('nd').callprop('setHours', var.get('mh'))
    var.get('nd').callprop('setDate', var.get('Math').callprop('floor', var.get('dom')))
    var.get('nd').callprop('setMonth', var.get('m'))
    var.put('em', PyJsComma(Js(0.0), Js(None)))
    var.put('md', var.get('cd').callprop('getDate'))
    if (var.get('cd')>=var.get('nd')):
        var.get('nd').callprop('setMonth', (var.get('nd').callprop('getMonth')+Js(1.0)))
    var.put('t1', var.get('cd').callprop('getTime'))
    var.put('t2', var.get('nd').callprop('getTime'))
    var.put('days', ((var.get('t2')-var.get('t1'))/Js(86400000.0)))
    return var.get('days')
PyJsHoisted_dl_.func_name = 'dl'
var.put('dl', PyJsHoisted_dl_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split40 = var.to_python()