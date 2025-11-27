__all__ = ['blog-split36']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['dbbackup'])
@Js
def PyJsHoisted_dbbackup_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['fe2', 'fe1', 'd1', 'd2'])
    try:
        var.put('fe1', var.get('app').callprop('FileExists', var.get('fn1')))
        var.put('fe2', var.get('app').callprop('FileExists', var.get('fn2')))
        if (var.get('fe1') and var.get('fe2').neg()):
            var.get('app').callprop('CopyFile', var.get('fn1'), var.get('fn2'))
            var.put('fe2', var.get('app').callprop('FileExists', var.get('fn2')))
            if var.get('fe2').neg():
                PyJsTempException = JsToPyException(var.get('Error').create(((Js('file ')+var.get('fn2'))+Js(" didn't arrive"))))
                raise PyJsTempException
        else:
            if (var.get('fe1') and var.get('fe2')):
                var.put('d1', var.get('app').callprop('GetFileDate', var.get('fn1')))
                var.put('d2', var.get('app').callprop('GetFileDate', var.get('fn2')))
                if (var.get('d1')>var.get('d2')):
                    var.get('app').callprop('CopyFile', var.get('fn1'), var.get('fn2'))
                    var.put('fe2', var.get('app').callprop('FileExists', var.get('fn2')))
                    if var.get('fe2').neg():
                        PyJsTempException = JsToPyException(var.get('Error').create(((Js('file ')+var.get('fn2'))+Js(' is now missing'))))
                        raise PyJsTempException
                    var.put('d2', var.get('app').callprop('GetFileDate', var.get('fn2')))
                    if (var.get('d1')>var.get('d2')):
                        PyJsTempException = JsToPyException(var.get('Errorr').create(((Js('file ')+var.get('fn2'))+Js(" didn't copy"))))
                        raise PyJsTempException
    except PyJsException as PyJsTempException:
        PyJsHolder_65_11266105 = var.own.get('e')
        var.force_own_put('e', PyExceptionToJs(PyJsTempException))
        try:
            var.get('app').callprop('Alert', var.get('e'))
        finally:
            if PyJsHolder_65_11266105 is not None:
                var.own['e'] = PyJsHolder_65_11266105
            else:
                del var.own['e']
            del PyJsHolder_65_11266105
PyJsHoisted_dbbackup_.func_name = 'dbbackup'
var.put('dbbackup', PyJsHoisted_dbbackup_)
Js('use strict')
pass
pass


# Add lib to the module scope
blog-split36 = var.to_python()