'''
Created on Jun 28, 2016

@author: Phil
'''
import os
import platform

import Dir
import json2
import utils

def run():
    from Drive import getDrives, driveletterFromVL
    getDrives()
    if os.environ['FLASH0'] is None:
        os.environ['FLASH0'] = os.path.dirname(os.path.abspath(__file__))
    # var cfn1 = __dirname + '\\plaunch_flash_' + 'CODE' + '.json';
    cfn2 = utils.expES('%FLASH0%\\Projects\\py-test\\plaunch_flash_CODE0.json')
    cfn3 = utils.expES('%FLASH0%\\Projects\\py-test\\plaunch_hd.json')

    # var splobj1 = json.readConfig(cfn1)
    splobj2 = json2.readConfig(cfn2)
    splobj3 = json2.readConfig(cfn3)

    ae2 = []

    def addplines(ps, pre, ae):
        for k in ps:
            if ps[k]['include']:
                s = pre + k
                if s.find(' ') != -1:
                    ae.append('\"' + s + '\"')
                else:
                    ae.append(s)

    # addplines(splobj1.paths, '%FLASH0%', ae2);

    addplines(splobj2['paths'], '%FLASH0%', ae2)
    addplines(splobj3['paths'], 'C:', ae2)

    crlf = '\n'

    envstr = ''
    pstr = ''
    (a, b) = platform.architecture()

    envstr += r'for /f "usebackq tokens=1,2 skip=1" %%i in (`wmic VOLUME where drivetype^=2 get label^,driveletter`) do (' + crlf
    envstr += r' if "%%j"=="CODE0" set FLASH0=%%i' + crlf
    envstr += r' if "%%j"=="CODE1" set FLASH1=%%i' + crlf
    envstr += r' if "%%j"=="CODE2" set FLASH2=%%i' + crlf
    envstr += r' if "%%j"=="CODE3" set FLASH3=%%i' + crlf
    envstr += r' if "%%j"=="CODE4" set FLASH4=%%i' + crlf
    envstr += r' if "%%j"=="CODE5" set FLASH5=%%i' + crlf
    envstr += r' if "%%j"=="CODE6" set FLASH6=%%i' + crlf
    envstr += r')' + crlf
    envstr += 'if "%FLASH0%"=="" exit' + crlf
    envstr += 'if "%FLASH1%"=="" exit' + crlf
    envstr += 'set ARCH=' + 'x' + a[0:2] + crlf
    # for k in splobj1.env):
    #     envstr += 'set ' + k + '=' + splobj1.env[k] + crlf
    for k in splobj2['env']:
        envstr += 'set ' + k + '=' + str(splobj2['env'][k]) + crlf
    pstr += 'path ' + (';%path%' + crlf + 'path ').join(ae2) + ';%path%' + crlf

    with open(driveletterFromVL('CODE0') + '\\.bat\\plaunch.bat', 'w') as f:
        f.write('@echo off' + crlf + envstr + pstr + crlf + '@echo on' + crlf + '%*' + crlf)

if __name__ == "__main__":
    run()
