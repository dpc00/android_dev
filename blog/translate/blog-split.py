__all__ = ['blog-split']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['ncs', 'fixtbl', 'dtbl', 'iee', 'dtbl_cs', 'mtbl_cs', 'set_handler', 'OnStart', 'cashb', 'rcb', 'tsz', 'd2t', 'dallow_calc', 'slow', 'losz', 'teot', 'set_color', 'davg_dtot_calc', 'mtbl', 'proxynums', 'tleft', 'ietbl_cs', 'inec', 'davg', 'bsz', 'dtot', 'ib', 'et', 'lts', 'dbps', 'maxdl', 'sql', 'txtpa', 'ietbl', 'me', 'update_ietbl', 'b3ot', 'inec_calc', 'txtp', 'dirty2', 'dirty3', 'dallow', 'dirty4', 'SaveNumber', 'loadnums', 'maxdl_calc', 'dbbackup', 'b2ot', 'log_balances', 'dxb', 'de', 'uspop', 'db', 'app', 'dl', 'dbfn', 'Mvar', 'updated', '_classCallCheck', 'uc', 'tblexists', 'nc', 'fsb', 'dbinstall', '_createClass', 'tesz', 'tleft_calc'])
@Js
def PyJsHoisted__classCallCheck_(instance, Constructor, this, arguments, var=var):
    var = Scope({'instance':instance, 'Constructor':Constructor, 'this':this, 'arguments':arguments}, var)
    var.registers(['Constructor', 'instance'])
    if var.get('instance').instanceof(var.get('Constructor')).neg():
        PyJsTempException = JsToPyException(var.get('TypeError').create(Js('Cannot call a class as a function')))
        raise PyJsTempException
PyJsHoisted__classCallCheck_.func_name = '_classCallCheck'
var.put('_classCallCheck', PyJsHoisted__classCallCheck_)
@Js
def PyJsHoisted_d2t_(dv, this, arguments, var=var):
    var = Scope({'dv':dv, 'this':this, 'arguments':arguments}, var)
    var.registers(['h', 'dv', 'd', 'm'])
    var.put('d', var.get('Math').callprop('floor', var.get('dv')))
    var.put('h', var.get('Math').callprop('floor', ((var.get('dv')*Js(24.0))%Js(24.0))))
    var.put('m', var.get('Math').callprop('round', ((var.get('dv')*(Js(24.0)*Js(60.0)))%Js(60.0))))
    return (((((var.get('d')+Js('d,'))+var.get('h'))+Js('h,'))+var.get('m'))+Js('m'))
PyJsHoisted_d2t_.func_name = 'd2t'
var.put('d2t', PyJsHoisted_d2t_)
@Js
def PyJsHoisted_dallow_calc_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['da'])
    var.put('da', ((var.get('cashb').get('num')+var.get('dxb').get('num'))/var.get('maxdl').get('num')))
    var.get('dallow').get('te').callprop('SetText', var.get('ncs')(var.get('da')))
    var.get('dallow').callprop('save')
PyJsHoisted_dallow_calc_.func_name = 'dallow_calc'
var.put('dallow_calc', PyJsHoisted_dallow_calc_)
@Js
def PyJsHoisted_davg_dtot_calc_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['r', 'tmp', 'rc', 'te', 'res', '_tmp'])
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
@Js
def PyJsHoisted_dbbackup_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['d2', 'd1', 'fe1', 'fe2'])
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
        PyJsHolder_65_82758607 = var.own.get('e')
        var.force_own_put('e', PyExceptionToJs(PyJsTempException))
        try:
            var.get('app').callprop('Alert', var.get('e'))
        finally:
            if PyJsHolder_65_82758607 is not None:
                var.own['e'] = PyJsHolder_65_82758607
            else:
                del var.own['e']
            del PyJsHolder_65_82758607
PyJsHoisted_dbbackup_.func_name = 'dbbackup'
var.put('dbbackup', PyJsHoisted_dbbackup_)
@Js
def PyJsHoisted_dbinstall_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['d2', 'd1', 'fe1', 'fe2'])
    try:
        var.put('fe1', var.get('app').callprop('FileExists', var.get('fn1')))
        var.put('fe2', var.get('app').callprop('FileExists', var.get('fn2')))
        if var.get('fe2').neg():
            PyJsTempException = JsToPyException(var.get('Error').create(((Js('backup db ')+var.get('fn2'))+Js(' not found.'))))
            raise PyJsTempException
        if (var.get('fe1').neg() and var.get('fe2')):
            var.get('app').callprop('CopyFile', var.get('fn2'), var.get('fn1'))
            var.put('fe1', var.get('app').callprop('FileExists', var.get('fn1')))
            if var.get('fe1').neg():
                PyJsTempException = JsToPyException(var.get('Error').create(((Js('file ')+var.get('fn2'))+Js(" didn't copy"))))
                raise PyJsTempException
        else:
            if (var.get('fe1') and var.get('fe2')):
                var.put('d1', var.get('app').callprop('GetFileDate', var.get('fn1')))
                var.put('d2', var.get('app').callprop('GetFileDate', var.get('fn2')))
                if (var.get('d2')>var.get('d1')):
                    var.get('app').callprop('CopyFile', var.get('fn2'), var.get('fn1'))
                    var.put('fe1', var.get('app').callprop('FileExists', var.get('fn1')))
                    if var.get('fe1').neg():
                        PyJsTempException = JsToPyException(var.get('Error').create(((Js('file ')+var.get('fn1'))+Js(" didn't copy"))))
                        raise PyJsTempException
            else:
                PyJsTempException = JsToPyException(var.get('Error').create(Js('one or more files missing')))
                raise PyJsTempException
    except PyJsException as PyJsTempException:
        PyJsHolder_65_17811850 = var.own.get('e')
        var.force_own_put('e', PyExceptionToJs(PyJsTempException))
        try:
            var.get('app').callprop('Alert', var.get('e'))
        finally:
            if PyJsHolder_65_17811850 is not None:
                var.own['e'] = PyJsHolder_65_17811850
            else:
                del var.own['e']
            del PyJsHolder_65_17811850
PyJsHoisted_dbinstall_.func_name = 'dbinstall'
var.put('dbinstall', PyJsHoisted_dbinstall_)
@Js
def PyJsHoisted_dbps_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['fn1', 'fn2'])
    var.put('fn1', (var.get('app').callprop('GetPrivateFolder', Js(''))+Js('/../databases')))
    if (var.get('fn1').get('length')!=Js(0.0)):
        var.put('fn1', Js('/'), '+')
    var.put('fn1', var.get('dbfn'), '+')
    var.put('fn2', Js('/sdcard/projects/blog'))
    if (var.get('fn2').get('length')!=Js(0.0)):
        var.put('fn2', Js('/'), '+')
    var.put('fn2', var.get('dbfn'), '+')
PyJsHoisted_dbps_.func_name = 'dbps'
var.put('dbps', PyJsHoisted_dbps_)
@Js
def PyJsHoisted_de_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get('tblexists')(Js('daily'))
PyJsHoisted_de_.func_name = 'de'
var.put('de', PyJsHoisted_de_)
@Js
def PyJsHoisted_dl_(m, dom, this, arguments, var=var):
    var = Scope({'m':m, 'dom':dom, 'this':this, 'arguments':arguments}, var)
    var.registers(['t1', 't2', 'm', 'em', 'ms', 'mm', 'cd', 'dom', 'mh', 'md', 'days', 'nd'])
    var.put('cd', var.get('Date').create())
    var.put('nd', var.get('Date').create())
    var.put('ms', var.get('Math').callprop('round', ((var.get('dom')*((Js(24.0)*Js(60.0))*Js(60.0)))%Js(60.0))))
    var.put('mm', var.get('Math').callprop('floor', ((var.get('dom')*(Js(24.0)*Js(60.0)))%Js(60.0))))
    var.put('mh', var.get('Math').callprop('floor', ((var.get('dom')*Js(24.0))%Js(24.0))))
    var.get('nd').callprop('setSeconds', var.get('ms'))
    var.get('nd').callprop('setMinutes', var.get('mm'))
    var.get('nd').callprop('setHours', var.get('mh'))
    var.get('nd').callprop('setDate', var.get('Math').callprop('floor', var.get('dom')))
    var.get('nd').callprop('setMonth', var.get('m'))
    var.put('em', PyJsComma(Js(0.0), Js(None)))
    var.put('md', var.get('cd').callprop('getDate'))
    if (var.get('cd')>=var.get('nd')):
        var.get('nd').callprop('setMonth', (var.get('nd').callprop('getMonth')+Js(1.0)))
    var.put('t1', var.get('cd').callprop('getTime'))
    var.put('t2', var.get('nd').callprop('getTime'))
    var.put('days', ((var.get('t2')-var.get('t1'))/Js(86400000.0)))
    return var.get('days')
PyJsHoisted_dl_.func_name = 'dl'
var.put('dl', PyJsHoisted_dl_)
@Js
def PyJsHoisted_dtbl_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['dex'])
    var.put('dex', var.get('de')())
    if (var.get('dex') and var.get('dirty3')):
        pass
    else:
        if var.get('dex').neg():
            var.get('sql')(var.get('dtbl_cs'))
            var.put('dirty3', Js(True))
    return var.get('dex')
PyJsHoisted_dtbl_.func_name = 'dtbl'
var.put('dtbl', PyJsHoisted_dtbl_)
@Js
def PyJsHoisted_fixtbl_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['res', 'row', '_i', 'sqlt1'])
    var.put('sqlt1', Js('CREATE TABLE IF NOT EXISTS tmpc (ts TIMESTAMP PRIMARY KEY NOT NULL,cash REAL,fs REAL,dx REAL)'))
    var.get('sql')(var.get('sqlt1'))
    var.get('sql')(Js('DELETE FROM tmpc'))
    var.put('res', var.get('sql')(Js('select * from currentc order by ts')))
    #for JS loop
    var.put('_i', Js(0.0))
    while (var.get('_i')<var.get('res').get('rows').get('length')):
        var.put('row', var.get('res').get('rows').callprop('item', var.get('_i')))
        var.get('sql')(Js('insert into tmpc (ts,cash,fs,dx) values (?,?,?,?)'), Js([var.get('Date').create(var.get('row').get('ts')).callprop('toISOString'), var.get('row').get('cash'), var.get('row').get('fs'), var.get('row').get('dx')]))
        # update
        (var.put('_i',Js(var.get('_i').to_number())+Js(1))-Js(1))
    var.get('app').callprop('Exit')
PyJsHoisted_fixtbl_.func_name = 'fixtbl'
var.put('fixtbl', PyJsHoisted_fixtbl_)
@Js
def PyJsHoisted_ib_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['tp', 'ts', 'res', 'f', 'lna', 'ft'])
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
@Js
def PyJsHoisted_iee_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get('tblexists')(Js('inc_exp'))
PyJsHoisted_iee_.func_name = 'iee'
var.put('iee', PyJsHoisted_iee_)
@Js
def PyJsHoisted_ietbl_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['iex'])
    var.put('iex', var.get('iee')())
    if (var.get('iex') and var.get('dirty2')):
        pass
    else:
        if var.get('iex').neg():
            var.get('sql')(var.get('ietbl_cs'))
            var.put('dirty2', Js(True))
    return var.get('iex')
PyJsHoisted_ietbl_.func_name = 'ietbl'
var.put('ietbl', PyJsHoisted_ietbl_)
@Js
def PyJsHoisted_inec_calc_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['res1'])
    var.put('res1', (var.get('davg').get('num')-var.get('dallow').get('num')))
    var.get('inec').get('te').callprop('SetText', var.get('ncs')((var.get('res1')*var.get('maxdl').get('num'))))
    var.get('inec').callprop('save')
PyJsHoisted_inec_calc_.func_name = 'inec_calc'
var.put('inec_calc', PyJsHoisted_inec_calc_)
@Js
def PyJsHoisted_loadnums_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    @Js
    def PyJs_anonymous_4_(tx, this, arguments, var=var):
        var = Scope({'tx':tx, 'this':this, 'arguments':arguments}, var)
        var.registers(['load', 'tx'])
        @Js
        def PyJsHoisted_load_(mv, this, arguments, var=var):
            var = Scope({'mv':mv, 'this':this, 'arguments':arguments}, var)
            var.registers(['mv'])
            @Js
            def PyJs_anonymous_5_(res, this, arguments, var=var):
                var = Scope({'res':res, 'this':this, 'arguments':arguments}, var)
                var.registers(['res'])
                if (var.get('res').get('rows').get('length')!=Js(1.0)):
                    var.get('alert')(var.get('mv').get('name'))
                var.get('mv').put('num', var.get('res').get('rows').callprop('item', Js(0.0)).get('num'))
                var.get('mv').get('te').callprop('SetText', var.get('mv').callprop('toString'))
            PyJs_anonymous_5_._set_name('anonymous')
            @Js
            def PyJs_anonymous_6_(err, this, arguments, var=var):
                var = Scope({'err':err, 'this':this, 'arguments':arguments}, var)
                var.registers(['err'])
                var.get('alert')(var.get('err'))
            PyJs_anonymous_6_._set_name('anonymous')
            @Js
            def PyJs_anonymous_7_(resolve, reject, this, arguments, var=var):
                var = Scope({'resolve':resolve, 'reject':reject, 'this':this, 'arguments':arguments}, var)
                var.registers(['resolve', 'reject'])
                @Js
                def PyJs_anonymous_8_(t, res, this, arguments, var=var):
                    var = Scope({'t':t, 'res':res, 'this':this, 'arguments':arguments}, var)
                    var.registers(['res', 't'])
                    var.get('resolve')(var.get('res'))
                PyJs_anonymous_8_._set_name('anonymous')
                @Js
                def PyJs_anonymous_9_(t, e, this, arguments, var=var):
                    var = Scope({'t':t, 'e':e, 'this':this, 'arguments':arguments}, var)
                    var.registers(['t', 'e'])
                    var.get('reject')(var.get('e'))
                PyJs_anonymous_9_._set_name('anonymous')
                var.get('tx').callprop('executeSql', Js('SELECT num FROM nums WHERE name=?'), Js([var.get('mv').get('name')]), PyJs_anonymous_8_, PyJs_anonymous_9_)
            PyJs_anonymous_7_._set_name('anonymous')
            var.get('Promise').create(PyJs_anonymous_7_).callprop('catch', PyJs_anonymous_6_).callprop('then', PyJs_anonymous_5_)
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
    PyJs_anonymous_4_._set_name('anonymous')
    var.get('db').callprop('transaction', PyJs_anonymous_4_)
PyJsHoisted_loadnums_.func_name = 'loadnums'
var.put('loadnums', PyJsHoisted_loadnums_)
@Js
def PyJsHoisted_log_balances_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.get('sql')(Js('INSERT INTO currentc (ts, cash, fs, dx) VALUES (?,?,?,?)'), Js([var.get('Date').create().callprop('toISOString'), var.get('cashb').get('num'), var.get('fsb').get('num'), var.get('dxb').get('num')]))
    var.put('dirty2', Js(True))
    (var.put('uc',Js(var.get('uc').to_number())+Js(1))-Js(1))
PyJsHoisted_log_balances_.func_name = 'log_balances'
var.put('log_balances', PyJsHoisted_log_balances_)
@Js
def PyJsHoisted_lts_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['res'])
    var.put('res', var.get('sql')(Js('SELECT ts FROM currentc ORDER BY ts DESC')))
    return var.get('res').get('rows').callprop('item', var.get('uc')).get('ts')
PyJsHoisted_lts_.func_name = 'lts'
var.put('lts', PyJsHoisted_lts_)
@Js
def PyJsHoisted_maxdl_calc_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['dxd', 'cashd'])
    var.put('cashd', var.get('dl')(Js(5.0), Js(28.0)))
    var.put('dxd', var.get('dl')(Js(5.0), Js(3.0)))
    var.get('maxdl').get('te').callprop('SetText', var.get('ncs')(var.get('Math').callprop('max', var.get('cashd'), var.get('dxd'))))
    var.get('maxdl').put('num', var.get('ncs')(var.get('Math').callprop('max', var.get('cashd'), var.get('dxd'))))
PyJsHoisted_maxdl_calc_.func_name = 'maxdl_calc'
var.put('maxdl_calc', PyJsHoisted_maxdl_calc_)
@Js
def PyJsHoisted_me_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get('tblexists')(Js('monthly'))
PyJsHoisted_me_.func_name = 'me'
var.put('me', PyJsHoisted_me_)
@Js
def PyJsHoisted_mtbl_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['mex'])
    var.put('mex', var.get('me')())
    if (var.get('mex') and var.get('dirty4')):
        pass
    else:
        if var.get('mex').neg():
            var.get('sql')(var.get('mtbl_cs'))
            var.put('dirty4', Js(True))
    return var.get('mex')
PyJsHoisted_mtbl_.func_name = 'mtbl'
var.put('mtbl', PyJsHoisted_mtbl_)
@Js
def PyJsHoisted_nc_(d, this, arguments, var=var):
    var = Scope({'d':d, 'this':this, 'arguments':arguments}, var)
    var.registers(['d'])
    return (var.get('Math').callprop('round', (var.get('d')*Js(100.0)))/Js(100.0))
PyJsHoisted_nc_.func_name = 'nc'
var.put('nc', PyJsHoisted_nc_)
@Js
def PyJsHoisted_ncs_(d, this, arguments, var=var):
    var = Scope({'d':d, 'this':this, 'arguments':arguments}, var)
    var.registers(['d'])
    return var.get('nc')(var.get('d')).callprop('toLocaleString', var.get('undefined'), Js({'minimumFractionDigits':Js(2.0),'maximumFractionDigits':Js(2.0)}))
PyJsHoisted_ncs_.func_name = 'ncs'
var.put('ncs', PyJsHoisted_ncs_)
@Js
def PyJsHoisted_OnStart_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['ttl1', 'lyo2', 'b2', 'b1', 'lyo1', 'lyo0', 'shuffleArray', 'i'])
    @Js
    def PyJsHoisted_shuffleArray_(array, this, arguments, var=var):
        var = Scope({'array':array, 'this':this, 'arguments':arguments}, var)
        var.registers(['j', '_ref', 'array', '_i2'])
        #for JS loop
        var.put('_i2', (var.get('array').get('length')-Js(1.0)))
        while (var.get('_i2')>Js(0.0)):
            var.put('j', var.get('Math').callprop('floor', (var.get('Math').callprop('random')*(var.get('_i2')+Js(1.0)))))
            var.put('_ref', Js([var.get('array').get(var.get('j')), var.get('array').get(var.get('_i2'))]))
            var.get('array').put(var.get('_i2'), var.get('_ref').get('0'))
            var.get('array').put(var.get('j'), var.get('_ref').get('1'))
            # update
            (var.put('_i2',Js(var.get('_i2').to_number())-Js(1))+Js(1))
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
    def PyJs_anonymous_10_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers([])
        @Js
        def PyJs_anonymous_11_(this, arguments, var=var):
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
        PyJs_anonymous_11_._set_name('anonymous')
        var.get('slow')(PyJs_anonymous_11_)
    PyJs_anonymous_10_._set_name('anonymous')
    var.get('b1').callprop('SetOnTouch', PyJs_anonymous_10_)
    var.put('b2', var.get('app').callprop('CreateButton', Js('Exit'), Js(0.5), var.get('bsz')))
    @Js
    def PyJs_b2ot_12_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments, 'b2ot':PyJs_b2ot_12_}, var)
        var.registers([])
        if (var.get('db')!=var.get(u"null")):
            var.get('db').callprop('Close')
            var.put('db', var.get(u"null"))
        var.get('app').callprop('Exit')
    PyJs_b2ot_12_._set_name('b2ot')
    var.put('b2ot', PyJs_b2ot_12_)
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
    def PyJs_bal_handler_13_(e, this, arguments, var=var):
        var = Scope({'e':e, 'this':this, 'arguments':arguments, 'bal_handler':PyJs_bal_handler_13_}, var)
        var.registers(['e'])
        var.get('davg_dtot_calc')()
        var.get('dallow_calc')()
        var.get('tleft_calc')()
    PyJs_bal_handler_13_._set_name('bal_handler')
    var.put('bal_handler', PyJs_bal_handler_13_)
    var.get('et').callprop('addEventListener', (var.get('cashb').get('name')+Js('-changed')), var.get('bal_handler'))
    var.get('et').callprop('addEventListener', (var.get('dxb').get('name')+Js('-changed')), var.get('bal_handler'))
    var.get('et').callprop('addEventListener', (var.get('fsb').get('name')+Js('-changed')), var.get('bal_handler'))
    var.get('et').callprop('addEventListener', Js('update'), var.get('bal_handler'))
    @Js
    def PyJs_anonymous_14_(e, this, arguments, var=var):
        var = Scope({'e':e, 'this':this, 'arguments':arguments}, var)
        var.registers(['e'])
        var.get('inec_calc')()
    PyJs_anonymous_14_._set_name('anonymous')
    var.get('et').callprop('addEventListener', (var.get('dallow').get('name')+Js('-changed')), PyJs_anonymous_14_)
    @Js
    def PyJs_anonymous_15_(e, this, arguments, var=var):
        var = Scope({'e':e, 'this':this, 'arguments':arguments}, var)
        var.registers(['e'])
        var.get('tleft_calc')()
        var.get('inec_calc')()
    PyJs_anonymous_15_._set_name('anonymous')
    var.get('et').callprop('addEventListener', (var.get('davg').get('name')+Js('-changed')), PyJs_anonymous_15_)
    @Js
    def PyJs_anonymous_16_(e, this, arguments, var=var):
        var = Scope({'e':e, 'this':this, 'arguments':arguments}, var)
        var.registers(['e'])
        var.get('dallow_calc')()
        var.get('inec_calc')()
    PyJs_anonymous_16_._set_name('anonymous')
    var.get('et').callprop('addEventListener', (var.get('maxdl').get('name')+Js('-changed')), PyJs_anonymous_16_)
    var.get('setInterval')(var.get('maxdl_calc'), Js(2000.0))
    var.get('bal_handler')()
PyJsHoisted_proxynums_.func_name = 'proxynums'
var.put('proxynums', PyJsHoisted_proxynums_)
@Js
def PyJsHoisted_SaveNumber_(name, num, this, arguments, var=var):
    var = Scope({'name':name, 'num':num, 'this':this, 'arguments':arguments}, var)
    var.registers(['num', 'name'])
    var.get('sql')(Js('UPDATE nums SET (num,ts)=(?,?) WHERE name=?'), Js([var.get('num'), var.get('Date').create().callprop('toISOString'), var.get('name')]))
PyJsHoisted_SaveNumber_.func_name = 'SaveNumber'
var.put('SaveNumber', PyJsHoisted_SaveNumber_)
@Js
def PyJsHoisted_set_color_(o, this, arguments, var=var):
    var = Scope({'o':o, 'this':this, 'arguments':arguments}, var)
    var.registers(['o'])
    try:
        var.get('o').callprop('SetBackColor', Js('white'))
    except PyJsException as PyJsTempException:
        PyJsHolder_65_53356893 = var.own.get('e')
        var.force_own_put('e', PyExceptionToJs(PyJsTempException))
        try:
            pass
        finally:
            if PyJsHolder_65_53356893 is not None:
                var.own['e'] = PyJsHolder_65_53356893
            else:
                del var.own['e']
            del PyJsHolder_65_53356893
    try:
        var.get('o').callprop('SetTextColor', Js('black'))
    except PyJsException as PyJsTempException:
        PyJsHolder_65_24623156 = var.own.get('e')
        var.force_own_put('e', PyExceptionToJs(PyJsTempException))
        try:
            pass
        finally:
            if PyJsHolder_65_24623156 is not None:
                var.own['e'] = PyJsHolder_65_24623156
            else:
                del var.own['e']
            del PyJsHolder_65_24623156
PyJsHoisted_set_color_.func_name = 'set_color'
var.put('set_color', PyJsHoisted_set_color_)
@Js
def PyJsHoisted_slow_(f, this, arguments, var=var):
    var = Scope({'f':f, 'this':this, 'arguments':arguments}, var)
    var.registers(['f'])
    var.get('app').callprop('ShowProgress')
    var.get('f')()
    var.get('app').callprop('HideProgress')
PyJsHoisted_slow_.func_name = 'slow'
var.put('slow', PyJsHoisted_slow_)
@Js
def PyJsHoisted_sql_(stmnt, dat, this, arguments, var=var):
    var = Scope({'stmnt':stmnt, 'dat':dat, 'this':this, 'arguments':arguments}, var)
    var.registers(['dat', 'stmnt'])
    if (var.get('db')==var.get(u"null")):
        var.put('db', var.get('app').callprop('OpenDatabase', var.get('dbfn')))
        var.get('db').callprop('ExecuteSql', Js('PRAGMA synchronous = OFF'))
    @Js
    def PyJs_anonymous_17_(err, this, arguments, var=var):
        var = Scope({'err':err, 'this':this, 'arguments':arguments}, var)
        var.registers(['err'])
        var.get('app').callprop('Alert', ((((var.get('err')+Js(','))+var.get('stmnt'))+Js(','))+var.get('dat')))
    PyJs_anonymous_17_._set_name('anonymous')
    @Js
    def PyJs_anonymous_18_(res, err, this, arguments, var=var):
        var = Scope({'res':res, 'err':err, 'this':this, 'arguments':arguments}, var)
        var.registers(['res', 'err'])
        var.get('db').callprop('ExecuteSql', var.get('stmnt'), var.get('dat'), var.get('res'), var.get('err'))
    PyJs_anonymous_18_._set_name('anonymous')
    return var.get('Promise').create(PyJs_anonymous_18_).callprop('catch', PyJs_anonymous_17_)
PyJsHoisted_sql_.func_name = 'sql'
var.put('sql', PyJsHoisted_sql_)
@Js
def PyJsHoisted_tblexists_(nm, this, arguments, var=var):
    var = Scope({'nm':nm, 'this':this, 'arguments':arguments}, var)
    var.registers(['res', 'nm'])
    var.put('res', var.get('sql')(Js("SELECT COUNT() AS cnt FROM sqlite_master WHERE type='table' AND name=?"), Js([var.get('nm')])))
    return (var.get('res').get('rows').callprop('item', Js(0.0)).get('cnt')>Js(0.0))
PyJsHoisted_tblexists_.func_name = 'tblexists'
var.put('tblexists', PyJsHoisted_tblexists_)
@Js
def PyJsHoisted_teot_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['v'])
    var.put('v', var.get(u"this").get('mvar'))
    var.get('app').callprop('ShowPopup', (Js(' v.name: ')+var.get('v').get('name')))
PyJsHoisted_teot_.func_name = 'teot'
var.put('teot', PyJsHoisted_teot_)
@Js
def PyJsHoisted_tleft_calc_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['tl', 'tmp', 'tf'])
    var.put('tf', (var.get('cashb').get('num')+var.get('dxb').get('num')))
    var.put('tl', (var.get('tf')/var.get('davg').get('num')))
    var.put('tmp', var.get('ncs')(var.get('tl')))
    var.get('tleft').get('te').callprop('SetText', var.get('tmp'))
    var.get('tleft').callprop('save')
PyJsHoisted_tleft_calc_.func_name = 'tleft_calc'
var.put('tleft_calc', PyJsHoisted_tleft_calc_)
@Js
def PyJsHoisted_txtp_(txt, this, arguments, var=var):
    var = Scope({'txt':txt, 'this':this, 'arguments':arguments}, var)
    var.registers(['txt'])
    @Js
    def PyJs_anonymous_19_(a, c, this, arguments, var=var):
        var = Scope({'a':a, 'c':c, 'this':this, 'arguments':arguments}, var)
        var.registers(['c', 'a'])
        return (var.get('a')+var.get('c'))
    PyJs_anonymous_19_._set_name('anonymous')
    return var.get('txtpa')(var.get('txt')).callprop('reduce', PyJs_anonymous_19_, Js(0.0))
PyJsHoisted_txtp_.func_name = 'txtp'
var.put('txtp', PyJsHoisted_txtp_)
@Js
def PyJsHoisted_txtpa_(txt, this, arguments, var=var):
    var = Scope({'txt':txt, 'this':this, 'arguments':arguments}, var)
    var.registers(['res1', 're', 'txt'])
    var.put('re', JsRegExp('/([+\\-]?\\s*([0-9,]*)([\\.][0-9]*)?)/g'))
    var.put('res1', var.get('txt').callprop('match', var.get('re')))
    if (var.get('res1')==var.get(u"null")):
        var.put('res1', Js([]))
    @Js
    def PyJs_anonymous_20_(n, this, arguments, var=var):
        var = Scope({'n':n, 'this':this, 'arguments':arguments}, var)
        var.registers(['n'])
        return ((var.get('n')!=var.get(u"null")) and var.get('Number').callprop('isFinite', var.get('n')))
    PyJs_anonymous_20_._set_name('anonymous')
    @Js
    def PyJs_anonymous_21_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        var.put('s', var.get('s').callprop('replace', JsRegExp('/\\s+/g'), Js('')))
        var.put('s', var.get('s').callprop('replace', JsRegExp('/,/g'), Js('')))
        return var.get('parseFloat')(var.get('s'))
    PyJs_anonymous_21_._set_name('anonymous')
    return var.get('res1').callprop('map', PyJs_anonymous_21_).callprop('filter', PyJs_anonymous_20_)
PyJsHoisted_txtpa_.func_name = 'txtpa'
var.put('txtpa', PyJsHoisted_txtpa_)
@Js
def PyJsHoisted_update_ietbl_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['sst', 'wh', '_sst', 'pd', 'dex', 'mex', 'iex'])
    var.get('app').callprop('ShowProgressBar', Js('updating tables...'))
    var.put('pd', var.get('lts')())
    var.put('iex', var.get('ietbl')())
    var.put('wh', Js(''))
    if (var.get('iex') and var.get('rcb').callprop('GetChecked').neg()):
        var.put('wh', ((Js(" WHERE ts>='")+var.get('pd'))+Js("'")))
    if (var.get('dirty2') or var.get('rcb').callprop('GetChecked')):
        @Js
        def PyJs_anonymous_22_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['rc', 'res', 'ss', 'j', 'i'])
            var.put('ss', ((Js('SELECT ts, cash, fs, dx FROM currentc')+var.get('wh'))+Js(' ORDER BY ts')))
            var.put('res', var.get('sql')(var.get('ss')))
            var.put('rc', var.get('res').get('rows').get('length'))
            var.put('j', Js(0.0))
            var.put('i', Js(1.0))
            @Js
            def PyJs_anonymous_23_(tx, this, arguments, var=var):
                var = Scope({'tx':tx, 'this':this, 'arguments':arguments}, var)
                var.registers(['dx_recd', 'dx_diff', 'ets', 'cr', 'cash_recd', 'res2', 'cash_diff', 'dx_spent', 'cash_spent', 'fs_recd', 'fs_spent', 'tx', 'bts', 'fs_diff', 'pr'])
                #for JS loop
                
                while (var.get('i')<var.get('rc')):
                    var.put('pr', var.get('res').get('rows').callprop('item', var.get('j')))
                    var.put('cr', var.get('res').get('rows').callprop('item', var.get('i')))
                    var.put('bts', var.get('pr').get('ts'))
                    var.put('ets', var.get('cr').get('ts'))
                    var.put('cash_diff', var.get('nc')((var.get('cr').get('cash')-var.get('pr').get('cash'))))
                    var.put('fs_diff', var.get('nc')((var.get('cr').get('fs')-var.get('pr').get('fs'))))
                    var.put('dx_diff', var.get('nc')((var.get('cr').get('dx')-var.get('pr').get('dx'))))
                    var.put('cash_recd', (var.get('cash_diff') if (var.get('cash_diff')>Js(0.0)) else var.get(u"null")))
                    var.put('fs_recd', (var.get('fs_diff') if (var.get('fs_diff')>Js(0.0)) else var.get(u"null")))
                    var.put('dx_recd', (var.get('dx_diff') if (var.get('dx_diff')>Js(0.0)) else var.get(u"null")))
                    var.put('cash_spent', (var.get('nc')((-var.get('cash_diff'))) if (var.get('cash_diff')<Js(0.0)) else var.get(u"null")))
                    var.put('fs_spent', (var.get('nc')((-var.get('fs_diff'))) if (var.get('fs_diff')<Js(0.0)) else var.get(u"null")))
                    var.put('dx_spent', (var.get('nc')((-var.get('dx_diff'))) if (var.get('dx_diff')<Js(0.0)) else var.get(u"null")))
                    if (((var.get('cash_diff')!=Js(0.0)) or (var.get('fs_diff')!=Js(0.0))) or (var.get('dx_diff')!=Js(0.0))):
                        var.put('res2', var.get('tx').callprop('executeSql', Js('INSERT OR REPLACE INTO inc_exp (bts, ets, cash_recd, fs_recd, dx_recd, cash_spent, fs_spent, dx_spent) VALUES (?,?,?,?,?,?,?,?)'), Js([var.get('bts'), var.get('ets'), var.get('cash_recd'), var.get('fs_recd'), var.get('dx_recd'), var.get('cash_spent'), var.get('fs_spent'), var.get('dx_spent')])))
                        var.put('j', var.get('i'))
                        var.put('dirty3', Js(True))
                    (var.put('uc',Js(var.get('uc').to_number())-Js(1))+Js(1))
                    var.get('app').callprop('UpdateProgressBar', ((var.get('i')*Js(80.0))/var.get('rc')))
                    # update
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            PyJs_anonymous_23_._set_name('anonymous')
            var.get('db').callprop('transaction', PyJs_anonymous_23_)
            var.put('dirty2', Js(False))
        PyJs_anonymous_22_._set_name('anonymous')
        PyJs_anonymous_22_()
    var.get('app').callprop('UpdateProgressBar', Js(80.0))
    var.put('dex', var.get('dtbl')())
    var.put('wh', Js(''))
    if (var.get('dex') and var.get('rcb').callprop('GetChecked').neg()):
        var.put('wh', ((Js(" WHERE substr(datetime(ets,'localtime'), 1, 10)>='")+var.get('Date').create(var.get('pd')).callprop('toLocaleDateString', Js('fr-CA')).callprop('substring', Js(0.0), Js(10.0)))+Js("'")))
        var.get('app').callprop('ShowPopup', var.get('wh'))
    if (var.get('dirty3') or var.get('rcb').callprop('GetChecked')):
        var.put('sst', ((Js(" SELECT substr(datetime(ets,'localtime'), 1, 10) AS ts, SUM(cash_recd) AS cash_recd, SUM(fs_recd) AS fs_recd, SUM(dx_recd) AS dx_recd, SUM(cash_spent) AS cash_spent, SUM(fs_spent) AS fs_spent, SUM(dx_spent) AS dx_spent FROM inc_exp")+var.get('wh'))+Js(" GROUP BY substr(datetime(ets,'localtime'), 1, 10)")))
        var.get('sql')((Js('INSERT OR REPLACE INTO daily')+var.get('sst')))
        var.put('dirty3', Js(False))
        var.put('dirty4', Js(True))
    var.get('app').callprop('UpdateProgressBar', Js(90.0))
    var.put('mex', var.get('mtbl')())
    var.put('wh', Js(''))
    if (var.get('mex') and var.get('rcb').callprop('GetChecked').neg()):
        var.put('wh', ((Js(" WHERE substr(datetime(ets,'localtime'), 1, 7)>='")+var.get('Date').create(var.get('pd')).callprop('toLocaleDateString', Js('fr-CA')).callprop('substring', Js(0.0), Js(7.0)))+Js("'")))
    if (var.get('dirty4') or var.get('rcb').callprop('GetChecked')):
        var.put('_sst', ((Js(" SELECT substr(datetime(ets,'localtime'), 1, 7) AS ts, SUM(cash_recd) AS cash_recd, SUM(fs_recd) AS fs_recd, SUM(dx_recd) AS dx_recd, SUM(cash_spent) AS cash_spent, SUM(fs_spent) AS fs_spent, SUM(dx_spent) AS dx_spent FROM inc_exp")+var.get('wh'))+Js(" GROUP BY substr(datetime(ets,'localtime'), 1, 7)")))
        var.get('sql')((Js('INSERT OR REPLACE INTO monthly')+var.get('_sst')))
        var.put('dirty4', Js(False))
    var.get('app').callprop('UpdateProgressBar', Js(100.0))
    var.get('app').callprop('HideProgressBar')
    if var.get('rcb').callprop('GetChecked'):
        var.put('uc', Js(0.0))
        var.get('rcb').callprop('SetChecked', Js(False))
PyJsHoisted_update_ietbl_.func_name = 'update_ietbl'
var.put('update_ietbl', PyJsHoisted_update_ietbl_)
Js('use strict')
@Js
def PyJs_anonymous_0_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['defineProperties'])
    @Js
    def PyJsHoisted_defineProperties_(target, props, this, arguments, var=var):
        var = Scope({'target':target, 'props':props, 'this':this, 'arguments':arguments}, var)
        var.registers(['target', 'i', 'descriptor', 'props'])
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
        var.registers(['Constructor', 'staticProps', 'protoProps'])
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
pass
pass
pass
var.put('bsz', Js(0.125))
pass
pass
pass
var.put('db', var.get(u"null"))
var.put('dbfn', Js('Finance.db'))
var.put('dirty2', Js(False))
var.put('dirty3', Js(False))
var.put('dirty4', Js(False))
var.put('dtbl_cs', Js('CREATE TABLE daily (ts TIMESTAMP PRIMARY KEY,cash_recd REAL,fs_recd REAL,dx_recd REAL,cash_spent REAL,fs_spent REAL,dx_spent REAL)'))
pass
pass
var.put('et', var.get('EventTarget').create())
pass
var.put('ietbl_cs', Js('CREATE TABLE inc_exp (bts TIMESTAMP NOT NULL,ets TIMESTAMP NOT NULL PRIMARY KEY,cash_recd REAL,fs_recd REAL,dx_recd REAL,cash_spent REAL,fs_spent REAL,dx_spent REAL)'))
pass
var.put('losz', Js(0.075))
pass
pass
var.put('mtbl_cs', Js('CREATE TABLE monthly (ts TIMESTAMP PRIMARY KEY,cash_recd REAL,fs_recd REAL,dx_recd REAL,cash_spent REAL,fs_spent REAL,dx_spent REAL)'))
pass
@Js
def PyJs_set_2_(obj, prop, val, this, arguments, var=var):
    var = Scope({'obj':obj, 'prop':prop, 'val':val, 'this':this, 'arguments':arguments, 'set':PyJs_set_2_}, var)
    var.registers(['oval', 'prop', 'val', 'obj'])
    var.put('oval', var.get('obj').get(var.get('prop')))
    var.get('obj').put(var.get('prop'), var.get('val'))
    if ((var.get('val')!=var.get('oval')) and (var.get('prop')==Js('num'))):
        var.get('et').callprop('dispatchEvent', var.get('Event').create((var.get('obj').get('name')+Js('-changed'))))
    return Js(True)
PyJs_set_2_._set_name('set')
var.put('set_handler', Js({'set':PyJs_set_2_}))
var.put('tesz', Js(0.066))
pass
var.put('tsz', Js(0.045))
var.put('uc', Js(0.0))
var.put('updated', Js(False))
var.put('uspop', Js(324459463.0))
@Js
def PyJs_anonymous_3_(percent, options, this, arguments, var=var):
    var = Scope({'percent':percent, 'options':options, 'this':this, 'arguments':arguments}, var)
    var.registers(['percent', 'options'])
    var.get('prompt')(Js('#'), (((Js('App.UpdateProgressBar(\x0c')+var.get('percent'))+Js('\x0c'))+var.get('options')))
PyJs_anonymous_3_._set_name('anonymous')
var.get('app').put('UpdateProgressBar', PyJs_anonymous_3_)
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
@Js
def PyJs_anonymous_24_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['Mvar'])
    @Js
    def PyJsHoisted_Mvar_(n, ne, this, arguments, var=var):
        var = Scope({'n':n, 'ne':ne, 'this':this, 'arguments':arguments}, var)
        var.registers(['n', 'ne'])
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
        def PyJs_anonymous_25_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['res1', 'res3', 'res2'])
            var.put('res2', PyJsComma(Js(0.0), Js(None)))
            var.put('res3', PyJsComma(Js(0.0), Js(None)))
            var.put('res1', var.get(u"this").callprop('GetText'))
            var.put('res2', var.get('txtpa')(var.get('res1')))
            @Js
            def PyJs_anonymous_26_(a, c, this, arguments, var=var):
                var = Scope({'a':a, 'c':c, 'this':this, 'arguments':arguments}, var)
                var.registers(['c', 'a'])
                return (var.get('a')+var.get('c'))
            PyJs_anonymous_26_._set_name('anonymous')
            var.put('res3', var.get('res2').callprop('reduce', PyJs_anonymous_26_, Js(0.0)))
            if (var.get('res2').get('length')==Js(0.0)):
                pass
            var.get('app').callprop('ShowPopup', ((((var.get(u"this").get('mvar').get('name')+Js(': '))+var.get('res1'))+Js(' = '))+var.get('ncs')(var.get('res3'))))
        PyJs_anonymous_25_._set_name('anonymous')
        var.get(u"this").put('tf', PyJs_anonymous_25_)
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
    def PyJs_save_27_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments, 'save':PyJs_save_27_}, var)
        var.registers(['_iteratorError', '_iterator', 'ia', 'acc', '_step', 'txt', 'ci', '_iteratorNormalCompletion', '_didIteratorError'])
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
            PyJsHolder_657272_10740534 = var.own.get('err')
            var.force_own_put('err', PyExceptionToJs(PyJsTempException))
            try:
                var.put('_didIteratorError', Js(True))
                var.put('_iteratorError', var.get('err'))
            finally:
                if PyJsHolder_657272_10740534 is not None:
                    var.own['err'] = PyJsHolder_657272_10740534
                else:
                    del var.own['err']
                del PyJsHolder_657272_10740534
        finally:
            try:
                if (var.get('_iteratorNormalCompletion').neg() and var.get('_iterator').get('return')):
                    var.get('_iterator').callprop('return')
            finally:
                if var.get('_didIteratorError'):
                    PyJsTempException = JsToPyException(var.get('_iteratorError'))
                    raise PyJsTempException
    PyJs_save_27_._set_name('save')
    @Js
    def PyJs_newbal_28_(nb, this, arguments, var=var):
        var = Scope({'nb':nb, 'this':this, 'arguments':arguments, 'newbal':PyJs_newbal_28_}, var)
        var.registers(['nb'])
        if PyJsStrictNeq(var.get(u"this").get('num'),var.get('nb')):
            var.get(u"this").put('num', var.get('nb'))
            var.get(u"this").get('te').callprop('SetText', var.get(u"this").callprop('toString'))
            var.get('SaveNumber')(var.get(u"this").get('name'), var.get(u"this").get('num'))
            if var.get(u"this").get('isbal'):
                var.get('log_balances')()
    PyJs_newbal_28_._set_name('newbal')
    @Js
    def PyJs_toString_29_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments, 'toString':PyJs_toString_29_}, var)
        var.registers([])
        return var.get('ncs')(var.get(u"this").get('num'))
    PyJs_toString_29_._set_name('toString')
    var.get('_createClass')(var.get('Mvar'), Js([Js({'key':Js('save'),'value':PyJs_save_27_}), Js({'key':Js('newbal'),'value':PyJs_newbal_28_}), Js({'key':Js('toString'),'value':PyJs_toString_29_})]))
    return var.get('Mvar')
PyJs_anonymous_24_._set_name('anonymous')
var.put('Mvar', PyJs_anonymous_24_())
pass


# Add lib to the module scope
blog-split = var.to_python()