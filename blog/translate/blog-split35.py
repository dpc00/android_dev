__all__ = ['blog-split35']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['davg_dtot_calc'])
@Js
def PyJsHoisted_davg_dtot_calc_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['_tmp', 'rc', 'r', 'res', 'tmp', 'te'])
    var.put('res', var.get('sql')(Js("SELECT * FROM daily WHERE 'ts' IS NOT NULL ORDER BY 'ts' ASC;")))
    var.put('rc', var.get('res').get('rows').get('length'))
    var.put('sc', Js(14.0))
    var.put('bd', var.get('Date').create(var.get('res').get('rows').callprop('item', ((var.get('rc')-var.get('sc'))-Js(1.0))).get('ts')))
    var.put('ed', var.get('Date').create(var.get('res').get('rows').callprop('item', (var.get('rc')-Js(1.0))).get('ts')))
    var.put('dd', ((var.get('ed').callprop('getTime')-var.get('bd').callprop('getTime'))/(((Js(1000.0)*Js(60.0))*Js(60.0))*Js(24.0))))
    var.put('te', Js(0.0))
    #for JS loop
    var.put('i', ((var.get('rc')-var.get('sc'))-Js(1.0)))
    while (var.get('i')<var.get('rc')):
        var.put('r', var.get('res').get('rows').callprop('item', var.get('i')))
        var.put('te', var.get('r').get('cash_spent'), '+')
        var.put('te', var.get('r').get('dx_spent'), '+')
        if (var.get('i')==(var.get('rc')-Js(1.0))):
            var.put('_tmp', var.get('ncs')((var.get('r').get('cash_spent')+var.get('r').get('dx_spent'))))
            var.get('dtot').get('te').callprop('SetText', var.get('_tmp'))
            var.get('dtot').callprop('save')
            var.get('dtot').get('lbl').callprop('SetText', var.get('r').get('ts'))
        # update
        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    var.put('tmp', var.get('ncs')((var.get('te')/var.get('dd'))))
    var.get('davg').get('te').callprop('SetText', var.get('tmp'))
    var.get('davg').callprop('save')
PyJsHoisted_davg_dtot_calc_.func_name = 'davg_dtot_calc'
var.put('davg_dtot_calc', PyJsHoisted_davg_dtot_calc_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split35 = var.to_python()