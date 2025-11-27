__all__ = ['blog-split60']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['sql'])
@Js
def PyJsHoisted_sql_(stmnt, dat, this, arguments, var=var):
    var = Scope({'stmnt':stmnt, 'dat':dat, 'this':this, 'arguments':arguments}, var)
    var.registers(['dat', 'stmnt'])
    if (var.get('db')==var.get(u"null")):
        var.put('db', var.get('app').callprop('OpenDatabase', var.get('dbfn')))
        var.get('db').callprop('ExecuteSql', Js('PRAGMA synchronous = OFF'))
    @Js
    def PyJs_anonymous_0_(err, this, arguments, var=var):
        var = Scope({'err':err, 'this':this, 'arguments':arguments}, var)
        var.registers(['err'])
        var.get('app').callprop('Alert', ((((var.get('err')+Js(','))+var.get('stmnt'))+Js(','))+var.get('dat')))
    PyJs_anonymous_0_._set_name('anonymous')
    @Js
    def PyJs_anonymous_1_(res, err, this, arguments, var=var):
        var = Scope({'res':res, 'err':err, 'this':this, 'arguments':arguments}, var)
        var.registers(['err', 'res'])
        var.get('db').callprop('ExecuteSql', var.get('stmnt'), var.get('dat'), var.get('res'), var.get('err'))
    PyJs_anonymous_1_._set_name('anonymous')
    return var.get('Promise').create(PyJs_anonymous_1_).callprop('catch', PyJs_anonymous_0_)
PyJsHoisted_sql_.func_name = 'sql'
var.put('sql', PyJsHoisted_sql_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split60 = var.to_python()