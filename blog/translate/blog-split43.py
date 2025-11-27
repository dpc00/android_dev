__all__ = ['blog-split43']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['ib'])
@Js
def PyJsHoisted_ib_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['ft', 'res', 'tp', 'ts', 'lna', 'f'])
    var.put('ft', var.get('app').callprop('ReadFile', (var.get('app').callprop('GetPath')+Js('/blog2.csv'))))
    var.put('lna', var.get('ft').callprop('split', Js('\n')))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get('lna').get('length')):
        var.put('f', var.get('lna').get(var.get('i')).callprop('split', Js(',')))
        var.put('tp', var.get('f').get('1').callprop('split', Js(':')))
        if (var.get('Number')(var.get('tp').get('0'))<Js(10.0)):
            var.get('tp').put('0', (Js('0')+var.get('Number')(var.get('tp').get('0'))))
        var.get('f').put('1', var.get('tp').callprop('join', Js(':')))
        var.put('ts', ((var.get('f').get('0')+Js(' '))+var.get('f').get('1')))
        var.put('res', var.get('sql')(Js('INSERT INTO currentc (ts, cash, fs, dx) VALUES (?,?,?,?)'), Js([var.get('Date').create(var.get('ts')).callprop('toISOString'), var.get('f').get('2'), var.get('f').get('3'), var.get('f').get('4')])))
        # update
        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    var.get('app').callprop('Exit')
PyJsHoisted_ib_.func_name = 'ib'
var.put('ib', PyJsHoisted_ib_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split43 = var.to_python()