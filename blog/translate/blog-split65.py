__all__ = ['blog-split65']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['txtpa'])
@Js
def PyJsHoisted_txtpa_(txt, this, arguments, var=var):
    var = Scope({'txt':txt, 'this':this, 'arguments':arguments}, var)
    var.registers(['res1', 'txt', 're'])
    var.put('re', JsRegExp('/([+\\-]?\\s*([0-9,]*)([\\.][0-9]*)?)/g'))
    var.put('res1', var.get('txt').callprop('match', var.get('re')))
    if (var.get('res1')==var.get(u"null")):
        var.put('res1', Js([]))
    @Js
    def PyJs_anonymous_0_(n, this, arguments, var=var):
        var = Scope({'n':n, 'this':this, 'arguments':arguments}, var)
        var.registers(['n'])
        return ((var.get('n')!=var.get(u"null")) and var.get('Number').callprop('isFinite', var.get('n')))
    PyJs_anonymous_0_._set_name('anonymous')
    @Js
    def PyJs_anonymous_1_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        var.put('s', var.get('s').callprop('replace', JsRegExp('/\\s+/g'), Js('')))
        var.put('s', var.get('s').callprop('replace', JsRegExp('/,/g'), Js('')))
        return var.get('parseFloat')(var.get('s'))
    PyJs_anonymous_1_._set_name('anonymous')
    return var.get('res1').callprop('map', PyJs_anonymous_1_).callprop('filter', PyJs_anonymous_0_)
PyJsHoisted_txtpa_.func_name = 'txtpa'
var.put('txtpa', PyJsHoisted_txtpa_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split65 = var.to_python()