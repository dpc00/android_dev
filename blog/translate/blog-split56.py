__all__ = ['blog-split56']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['proxynums'])
@Js
def PyJsHoisted_proxynums_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['bal_handler'])
    var.put('cashb', var.get('Proxy').create(var.get('cashb'), var.get('set_handler')))
    var.put('fsb', var.get('Proxy').create(var.get('fsb'), var.get('set_handler')))
    var.put('dxb', var.get('Proxy').create(var.get('dxb'), var.get('set_handler')))
    var.put('davg', var.get('Proxy').create(var.get('davg'), var.get('set_handler')))
    var.put('dallow', var.get('Proxy').create(var.get('dallow'), var.get('set_handler')))
    var.put('maxdl', var.get('Proxy').create(var.get('maxdl'), var.get('set_handler')))
    @Js
    def PyJs_bal_handler_0_(e, this, arguments, var=var):
        var = Scope({'e':e, 'this':this, 'arguments':arguments, 'bal_handler':PyJs_bal_handler_0_}, var)
        var.registers(['e'])
        var.get('davg_dtot_calc')()
        var.get('dallow_calc')()
        var.get('tleft_calc')()
    PyJs_bal_handler_0_._set_name('bal_handler')
    var.put('bal_handler', PyJs_bal_handler_0_)
    var.get('et').callprop('addEventListener', (var.get('cashb').get('name')+Js('-changed')), var.get('bal_handler'))
    var.get('et').callprop('addEventListener', (var.get('dxb').get('name')+Js('-changed')), var.get('bal_handler'))
    var.get('et').callprop('addEventListener', (var.get('fsb').get('name')+Js('-changed')), var.get('bal_handler'))
    var.get('et').callprop('addEventListener', Js('update'), var.get('bal_handler'))
    @Js
    def PyJs_anonymous_1_(e, this, arguments, var=var):
        var = Scope({'e':e, 'this':this, 'arguments':arguments}, var)
        var.registers(['e'])
        var.get('inec_calc')()
    PyJs_anonymous_1_._set_name('anonymous')
    var.get('et').callprop('addEventListener', (var.get('dallow').get('name')+Js('-changed')), PyJs_anonymous_1_)
    @Js
    def PyJs_anonymous_2_(e, this, arguments, var=var):
        var = Scope({'e':e, 'this':this, 'arguments':arguments}, var)
        var.registers(['e'])
        var.get('tleft_calc')()
        var.get('inec_calc')()
    PyJs_anonymous_2_._set_name('anonymous')
    var.get('et').callprop('addEventListener', (var.get('davg').get('name')+Js('-changed')), PyJs_anonymous_2_)
    @Js
    def PyJs_anonymous_3_(e, this, arguments, var=var):
        var = Scope({'e':e, 'this':this, 'arguments':arguments}, var)
        var.registers(['e'])
        var.get('dallow_calc')()
        var.get('inec_calc')()
    PyJs_anonymous_3_._set_name('anonymous')
    var.get('et').callprop('addEventListener', (var.get('maxdl').get('name')+Js('-changed')), PyJs_anonymous_3_)
    var.get('setInterval')(var.get('maxdl_calc'), Js(2000.0))
    var.get('bal_handler')()
PyJsHoisted_proxynums_.func_name = 'proxynums'
var.put('proxynums', PyJsHoisted_proxynums_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split56 = var.to_python()