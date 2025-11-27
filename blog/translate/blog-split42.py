__all__ = ['blog-split42']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['fixtbl'])
@Js
def PyJsHoisted_fixtbl_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['i', 'sqlt1', 'res', 'row'])
    var.put('sqlt1', Js('CREATE TABLE IF NOT EXISTS tmpc (ts TIMESTAMP PRIMARY KEY NOT NULL,cash REAL,fs REAL,dx REAL)'))
    var.get('sql')(var.get('sqlt1'))
    var.get('sql')(Js('DELETE FROM tmpc'))
    var.put('res', var.get('sql')(Js('select * from currentc order by ts')))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get('res').get('rows').get('length')):
        var.put('row', var.get('res').get('rows').callprop('item', var.get('i')))
        var.get('sql')(Js('insert into tmpc (ts,cash,fs,dx) values (?,?,?,?)'), Js([var.get('Date').create(var.get('row').get('ts')).callprop('toISOString'), var.get('row').get('cash'), var.get('row').get('fs'), var.get('row').get('dx')]))
        # update
        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    var.get('app').callprop('Exit')
PyJsHoisted_fixtbl_.func_name = 'fixtbl'
var.put('fixtbl', PyJsHoisted_fixtbl_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split42 = var.to_python()