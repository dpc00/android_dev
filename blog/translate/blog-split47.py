__all__ = ['blog-split47']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['loadnums'])
@Js
def PyJsHoisted_loadnums_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    @Js
    def PyJs_anonymous_0_(tx, this, arguments, var=var):
        var = Scope({'tx':tx, 'this':this, 'arguments':arguments}, var)
        var.registers(['load', 'tx'])
        @Js
        def PyJsHoisted_load_(mv, this, arguments, var=var):
            var = Scope({'mv':mv, 'this':this, 'arguments':arguments}, var)
            var.registers(['mv'])
            @Js
            def PyJs_anonymous_1_(res, this, arguments, var=var):
                var = Scope({'res':res, 'this':this, 'arguments':arguments}, var)
                var.registers(['res'])
                if (var.get('res').get('rows').get('length')!=Js(1.0)):
                    var.get('alert')(var.get('mv').get('name'))
                var.get('mv').put('num', var.get('res').get('rows').callprop('item', Js(0.0)).get('num'))
                var.get('mv').get('te').callprop('SetText', var.get('mv').callprop('toString'))
            PyJs_anonymous_1_._set_name('anonymous')
            @Js
            def PyJs_anonymous_2_(err, this, arguments, var=var):
                var = Scope({'err':err, 'this':this, 'arguments':arguments}, var)
                var.registers(['err'])
                var.get('alert')(var.get('err'))
            PyJs_anonymous_2_._set_name('anonymous')
            @Js
            def PyJs_anonymous_3_(resolve, reject, this, arguments, var=var):
                var = Scope({'resolve':resolve, 'reject':reject, 'this':this, 'arguments':arguments}, var)
                var.registers(['resolve', 'reject'])
                @Js
                def PyJs_anonymous_4_(t, res, this, arguments, var=var):
                    var = Scope({'t':t, 'res':res, 'this':this, 'arguments':arguments}, var)
                    var.registers(['res', 't'])
                    var.get('resolve')(var.get('res'))
                PyJs_anonymous_4_._set_name('anonymous')
                @Js
                def PyJs_anonymous_5_(t, e, this, arguments, var=var):
                    var = Scope({'t':t, 'e':e, 'this':this, 'arguments':arguments}, var)
                    var.registers(['t', 'e'])
                    var.get('reject')(var.get('e'))
                PyJs_anonymous_5_._set_name('anonymous')
                var.get('tx').callprop('executeSql', Js('SELECT num FROM nums WHERE name=?'), Js([var.get('mv').get('name')]), PyJs_anonymous_4_, PyJs_anonymous_5_)
            PyJs_anonymous_3_._set_name('anonymous')
            var.get('Promise').create(PyJs_anonymous_3_).callprop('catch', PyJs_anonymous_2_).callprop('then', PyJs_anonymous_1_)
        PyJsHoisted_load_.func_name = 'load'
        var.put('load', PyJsHoisted_load_)
        pass
        var.get('load')(var.get('cashb'))
        var.get('load')(var.get('fsb'))
        var.get('load')(var.get('dxb'))
        var.get('load')(var.get('davg'))
        var.get('load')(var.get('dallow'))
        var.get('load')(var.get('inec'))
        var.get('load')(var.get('dtot'))
        var.get('load')(var.get('tleft'))
    PyJs_anonymous_0_._set_name('anonymous')
    var.get('db').callprop('transaction', PyJs_anonymous_0_)
PyJsHoisted_loadnums_.func_name = 'loadnums'
var.put('loadnums', PyJsHoisted_loadnums_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split47 = var.to_python()