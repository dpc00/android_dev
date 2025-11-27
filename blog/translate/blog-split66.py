__all__ = ['blog-split66']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['update_ietbl'])
@Js
def PyJsHoisted_update_ietbl_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['mex', 'pd', 'wh', '_sst', 'iex', 'dex', 'sst'])
    var.get('app').callprop('ShowProgressBar', Js('updating tables...'))
    var.put('pd', var.get('lts')())
    var.put('iex', var.get('ietbl')())
    var.put('wh', Js(''))
    if (var.get('iex') and var.get('rcb').callprop('GetChecked').neg()):
        var.put('wh', ((Js(" WHERE ts>='")+var.get('pd'))+Js("'")))
    if (var.get('dirty2') or var.get('rcb').callprop('GetChecked')):
        @Js
        def PyJs_anonymous_0_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['rc', 'res', 'i', 'j', 'ss'])
            var.put('ss', ((Js('SELECT ts, cash, fs, dx FROM currentc')+var.get('wh'))+Js(' ORDER BY ts')))
            var.put('res', var.get('sql')(var.get('ss')))
            var.put('rc', var.get('res').get('rows').get('length'))
            var.put('j', Js(0.0))
            var.put('i', Js(1.0))
            @Js
            def PyJs_anonymous_1_(tx, this, arguments, var=var):
                var = Scope({'tx':tx, 'this':this, 'arguments':arguments}, var)
                var.registers(['ets', 'cash_diff', 'dx_diff', 'cash_recd', 'tx', 'fs_spent', 'cr', 'bts', 'fs_diff', 'dx_spent', 'pr', 'res2', 'cash_spent', 'fs_recd', 'dx_recd'])
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
            PyJs_anonymous_1_._set_name('anonymous')
            var.get('db').callprop('transaction', PyJs_anonymous_1_)
            var.put('dirty2', Js(False))
        PyJs_anonymous_0_._set_name('anonymous')
        PyJs_anonymous_0_()
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
pass
pass


# Add lib to the module scope
blog-split66 = var.to_python()