__all__ = ['blog-split55']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['OnStart'])
@Js
def PyJsHoisted_OnStart_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['lyo2', 'lyo1', 'shuffleArray', 'lyo0', 'b2', 'b1', 'i', 'ttl1'])
    @Js
    def PyJsHoisted_shuffleArray_(array, this, arguments, var=var):
        var = Scope({'array':array, 'this':this, 'arguments':arguments}, var)
        var.registers(['_i', 'j', 'array', '_ref'])
        #for JS loop
        var.put('_i', (var.get('array').get('length')-Js(1.0)))
        while (var.get('_i')>Js(0.0)):
            var.put('j', var.get('Math').callprop('floor', (var.get('Math').callprop('random')*(var.get('_i')+Js(1.0)))))
            var.put('_ref', Js([var.get('array').get(var.get('j')), var.get('array').get(var.get('_i'))]))
            var.get('array').put(var.get('_i'), var.get('_ref').get('0'))
            var.get('array').put(var.get('j'), var.get('_ref').get('1'))
            # update
            (var.put('_i',Js(var.get('_i').to_number())-Js(1))+Js(1))
    PyJsHoisted_shuffleArray_.func_name = 'shuffleArray'
    var.put('shuffleArray', PyJsHoisted_shuffleArray_)
    var.put('db', var.get('app').callprop('OpenDatabase', var.get('dbfn')))
    var.put('cashb', var.get('Mvar').create(Js('Cash'), Js('')))
    var.put('fsb', var.get('Mvar').create(Js('FS'), Js('')))
    var.put('dxb', var.get('Mvar').create(Js('DX'), Js('')))
    var.get('cashb').put('isbal', Js(True))
    var.get('fsb').put('isbal', Js(True))
    var.get('dxb').put('isbal', Js(True))
    var.put('davg', var.get('Mvar').create(Js('DAvgExp'), Js('readonly,nokeyboard')))
    var.get('davg').get('te').callprop('SetTextColor', Js('turquoise'))
    var.put('dallow', var.get('Mvar').create(Js('DAllow'), Js('readonly,nokeyboard')))
    var.get('dallow').get('te').callprop('SetTextColor', Js('fuchsia'))
    var.put('inec', var.get('Mvar').create(Js('INec'), Js('readonly,nokeyboard')))
    var.get('inec').get('te').callprop('SetTextColor', Js('green'))
    var.put('dtot', var.get('Mvar').create(Js('DTotExp'), Js('readonly,nokeyboard')))
    var.get('dtot').get('te').callprop('SetTextColor', Js('blue'))
    var.put('tleft', var.get('Mvar').create(Js('TLeft'), Js('readonly,nokeyboard')))
    var.get('tleft').get('te').callprop('SetTextColor', Js('red'))
    var.put('maxdl', var.get('Mvar').create(Js('MaxDL'), Js('readonly,nokeyboard')))
    var.get('proxynums')()
    var.get('loadnums')()
    var.put('b1', var.get('app').callprop('CreateButton', Js('Update'), Js(0.5), var.get('bsz')))
    @Js
    def PyJs_anonymous_0_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers([])
        @Js
        def PyJs_anonymous_1_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            var.get('cashb').callprop('save')
            var.get('fsb').callprop('save')
            var.get('dxb').callprop('save')
            var.get('davg').callprop('save')
            var.get('dallow').callprop('save')
            var.get('inec').callprop('save')
            var.get('dtot').callprop('save')
            var.get('tleft').callprop('save')
            var.get('maxdl').callprop('save')
            var.get('update_ietbl')()
            var.get('et').callprop('dispatchEvent', var.get('Event').create(Js('update')))
        PyJs_anonymous_1_._set_name('anonymous')
        var.get('slow')(PyJs_anonymous_1_)
    PyJs_anonymous_0_._set_name('anonymous')
    var.get('b1').callprop('SetOnTouch', PyJs_anonymous_0_)
    var.put('b2', var.get('app').callprop('CreateButton', Js('Exit'), Js(0.5), var.get('bsz')))
    @Js
    def PyJs_b2ot_2_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments, 'b2ot':PyJs_b2ot_2_}, var)
        var.registers([])
        if (var.get('db')!=var.get(u"null")):
            var.get('db').callprop('Close')
            var.put('db', var.get(u"null"))
        var.get('app').callprop('Exit')
    PyJs_b2ot_2_._set_name('b2ot')
    var.put('b2ot', PyJs_b2ot_2_)
    var.get('b2').callprop('SetOnTouch', var.get('b2ot'))
    var.get('window').put('onclose', var.get('b2ot'))
    var.put('rcb', var.get('app').callprop('CreateCheckBox', Js('Regen i/e tables')))
    var.get('set_color')(var.get('rcb'))
    var.put('ttl1', var.get('app').callprop('CreateText', Js('Balance Log')))
    var.get('ttl1').callprop('SetTextSize', Js(26.0))
    var.put('lyo1', var.get('app').callprop('CreateLayout', Js('linear'), Js('vertical, center')))
    var.get('lyo1').callprop('AddChild', var.get('cashb').get('lo'))
    var.get('lyo1').callprop('AddChild', var.get('dxb').get('lo'))
    var.get('lyo1').callprop('AddChild', var.get('fsb').get('lo'))
    var.get('set_color')(var.get('lyo1'))
    var.put('lyo2', var.get('app').callprop('CreateLayout', Js('linear'), Js('vertical,center')))
    pass
    var.put('los', Js([var.get('dallow').get('lo'), var.get('inec').get('lo'), var.get('tleft').get('lo'), var.get('davg').get('lo'), var.get('dtot').get('lo')]))
    var.get('shuffleArray')(var.get('los'))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get('los').get('length')):
        var.get('lyo2').callprop('AddChild', var.get('los').get(var.get('i')))
        # update
        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    var.get('set_color')(var.get('lyo2'))
    var.put('lyo0', var.get('app').callprop('CreateLayout', Js('linear'), Js('vertical, center')))
    var.get('lyo0').callprop('AddChild', var.get('ttl1'))
    var.get('lyo0').callprop('AddChild', var.get('lyo1'))
    var.get('lyo0').callprop('AddChild', var.get('lyo2'))
    var.get('lyo0').callprop('AddChild', var.get('b1'))
    var.get('lyo0').callprop('AddChild', var.get('b2'))
    var.get('lyo0').callprop('AddChild', var.get('rcb'))
    var.get('set_color')(var.get('lyo0'))
    var.get('lyo0').callprop('SetSize', Js(1.0), Js(2.0))
    var.get('app').callprop('AddLayout', var.get('lyo0'))
PyJsHoisted_OnStart_.func_name = 'OnStart'
var.put('OnStart', PyJsHoisted_OnStart_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split55 = var.to_python()