__all__ = ['blog-split67']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['Mvar', '_createClass', '_classCallCheck'])
@Js
def PyJsHoisted__classCallCheck_(instance, Constructor, this, arguments, var=var):
    var = Scope({'instance':instance, 'Constructor':Constructor, 'this':this, 'arguments':arguments}, var)
    var.registers(['instance', 'Constructor'])
    if var.get('instance').instanceof(var.get('Constructor')).neg():
        PyJsTempException = JsToPyException(var.get('TypeError').create(Js('Cannot call a class as a function')))
        raise PyJsTempException
PyJsHoisted__classCallCheck_.func_name = '_classCallCheck'
var.put('_classCallCheck', PyJsHoisted__classCallCheck_)
Js('use strict')
@Js
def PyJs_anonymous_0_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['defineProperties'])
    @Js
    def PyJsHoisted_defineProperties_(target, props, this, arguments, var=var):
        var = Scope({'target':target, 'props':props, 'this':this, 'arguments':arguments}, var)
        var.registers(['descriptor', 'i', 'target', 'props'])
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<var.get('props').get('length')):
            var.put('descriptor', var.get('props').get(var.get('i')))
            var.get('descriptor').put('enumerable', (var.get('descriptor').get('enumerable') or Js(False)))
            var.get('descriptor').put('configurable', Js(True))
            if var.get('descriptor').contains(Js('value')):
                var.get('descriptor').put('writable', Js(True))
            var.get('Object').callprop('defineProperty', var.get('target'), var.get('descriptor').get('key'), var.get('descriptor'))
            # update
            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    PyJsHoisted_defineProperties_.func_name = 'defineProperties'
    var.put('defineProperties', PyJsHoisted_defineProperties_)
    pass
    @Js
    def PyJs_anonymous_1_(Constructor, protoProps, staticProps, this, arguments, var=var):
        var = Scope({'Constructor':Constructor, 'protoProps':protoProps, 'staticProps':staticProps, 'this':this, 'arguments':arguments}, var)
        var.registers(['Constructor', 'protoProps', 'staticProps'])
        if var.get('protoProps'):
            var.get('defineProperties')(var.get('Constructor').get('prototype'), var.get('protoProps'))
        if var.get('staticProps'):
            var.get('defineProperties')(var.get('Constructor'), var.get('staticProps'))
        return var.get('Constructor')
    PyJs_anonymous_1_._set_name('anonymous')
    return PyJs_anonymous_1_
PyJs_anonymous_0_._set_name('anonymous')
var.put('_createClass', PyJs_anonymous_0_())
pass
@Js
def PyJs_anonymous_2_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['Mvar'])
    @Js
    def PyJsHoisted_Mvar_(n, ne, this, arguments, var=var):
        var = Scope({'n':n, 'ne':ne, 'this':this, 'arguments':arguments}, var)
        var.registers(['ne', 'n'])
        var.get('_classCallCheck')(var.get(u"this"), var.get('Mvar'))
        var.get(u"this").put('num', Js(0.0))
        var.get(u"this").put('te', var.get('app').callprop('CreateTextEdit', Js(''), Js(0.5), var.get('tesz'), (Js('singleline')+((Js(',')+var.get('ne')) if PyJsStrictNeq(var.get('ne'),Js('')) else Js('')))))
        var.get(u"this").put('name', var.get('n'))
        var.get(u"this").get('te').callprop('SetHint', var.get('n'))
        var.get(u"this").get('te').put('mvar', var.get(u"this"))
        var.get(u"this").put('lbl', var.get('app').callprop('CreateText', var.get(u"this").get('name'), Js(0.325), var.get('tsz'), Js('right')))
        var.get(u"this").put('lo', var.get('app').callprop('CreateLayout', Js('linear'), Js('horizontal')))
        var.get(u"this").get('lo').callprop('AddChild', var.get(u"this").get('lbl'))
        var.get(u"this").get('lo').callprop('AddChild', var.get(u"this").get('te'))
        var.get(u"this").get('lo').callprop('SetSize', Js(0.8), var.get('tesz'))
        @Js
        def PyJs_anonymous_3_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['res1', 'res3', 'res2'])
            var.put('res2', PyJsComma(Js(0.0), Js(None)))
            var.put('res3', PyJsComma(Js(0.0), Js(None)))
            var.put('res1', var.get(u"this").callprop('GetText'))
            var.put('res2', var.get('txtpa')(var.get('res1')))
            @Js
            def PyJs_anonymous_4_(a, c, this, arguments, var=var):
                var = Scope({'a':a, 'c':c, 'this':this, 'arguments':arguments}, var)
                var.registers(['a', 'c'])
                return (var.get('a')+var.get('c'))
            PyJs_anonymous_4_._set_name('anonymous')
            var.put('res3', var.get('res2').callprop('reduce', PyJs_anonymous_4_, Js(0.0)))
            if (var.get('res2').get('length')==Js(0.0)):
                pass
            var.get('app').callprop('ShowPopup', ((((var.get(u"this").get('mvar').get('name')+Js(': '))+var.get('res1'))+Js(' = '))+var.get('ncs')(var.get('res3'))))
        PyJs_anonymous_3_._set_name('anonymous')
        var.get(u"this").put('tf', PyJs_anonymous_3_)
        var.get(u"this").get('te').callprop('SetOnTouch', var.get(u"this").get('tf'))
        var.get(u"this").put('cf', var.get(u"this").get('tf'))
        var.get(u"this").get('te').callprop('SetOnChange', var.get(u"this").get('cf'))
        var.get('set_color')(var.get(u"this").get('te'))
        var.get('set_color')(var.get(u"this").get('lbl'))
        var.get('set_color')(var.get(u"this").get('lo'))
    PyJsHoisted_Mvar_.func_name = 'Mvar'
    var.put('Mvar', PyJsHoisted_Mvar_)
    pass
    @Js
    def PyJs_save_5_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments, 'save':PyJs_save_5_}, var)
        var.registers(['acc', '_iterator', '_didIteratorError', '_iteratorNormalCompletion', '_step', 'ci', '_iteratorError', 'txt', 'ia'])
        var.put('txt', var.get(u"this").get('te').callprop('GetText'))
        var.put('ia', var.get('txtpa')(var.get('txt')))
        var.put('acc', Js(0.0))
        var.put('_iteratorNormalCompletion', Js(True))
        var.put('_didIteratorError', Js(False))
        var.put('_iteratorError', var.get('undefined'))
        try:
            #for JS loop
            var.put('_iterator', var.get('ia').callprop(var.get('Symbol').get('iterator')))
            while var.put('_iteratorNormalCompletion', var.put('_step', var.get('_iterator').callprop('next')).get('done')).neg():
                var.put('ci', var.get('_step').get('value'))
                var.put('acc', var.get('nc')((var.get('acc')+var.get('ci'))))
                var.get(u"this").callprop('newbal', var.get('acc'))
                # update
                var.put('_iteratorNormalCompletion', Js(True))
        except PyJsException as PyJsTempException:
            PyJsHolder_657272_74094564 = var.own.get('err')
            var.force_own_put('err', PyExceptionToJs(PyJsTempException))
            try:
                var.put('_didIteratorError', Js(True))
                var.put('_iteratorError', var.get('err'))
            finally:
                if PyJsHolder_657272_74094564 is not None:
                    var.own['err'] = PyJsHolder_657272_74094564
                else:
                    del var.own['err']
                del PyJsHolder_657272_74094564
        finally:
            try:
                if (var.get('_iteratorNormalCompletion').neg() and var.get('_iterator').get('return')):
                    var.get('_iterator').callprop('return')
            finally:
                if var.get('_didIteratorError'):
                    PyJsTempException = JsToPyException(var.get('_iteratorError'))
                    raise PyJsTempException
    PyJs_save_5_._set_name('save')
    @Js
    def PyJs_newbal_6_(nb, this, arguments, var=var):
        var = Scope({'nb':nb, 'this':this, 'arguments':arguments, 'newbal':PyJs_newbal_6_}, var)
        var.registers(['nb'])
        if PyJsStrictNeq(var.get(u"this").get('num'),var.get('nb')):
            var.get(u"this").put('num', var.get('nb'))
            var.get(u"this").get('te').callprop('SetText', var.get(u"this").callprop('toString'))
            var.get('SaveNumber')(var.get(u"this").get('name'), var.get(u"this").get('num'))
            if var.get(u"this").get('isbal'):
                var.get('log_balances')()
    PyJs_newbal_6_._set_name('newbal')
    @Js
    def PyJs_toString_7_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments, 'toString':PyJs_toString_7_}, var)
        var.registers([])
        return var.get('ncs')(var.get(u"this").get('num'))
    PyJs_toString_7_._set_name('toString')
    var.get('_createClass')(var.get('Mvar'), Js([Js({'key':Js('save'),'value':PyJs_save_5_}), Js({'key':Js('newbal'),'value':PyJs_newbal_6_}), Js({'key':Js('toString'),'value':PyJs_toString_7_})]))
    return var.get('Mvar')
PyJs_anonymous_2_._set_name('anonymous')
var.put('Mvar', PyJs_anonymous_2_())
pass


# Add lib to the module scope
blog-split67 = var.to_python()