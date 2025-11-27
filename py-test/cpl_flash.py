'''
Created on Jul 10, 2016

@author: Phil
'''

import dirutils
import json2
import utils
import Dir

def doFlashDrive(vl):
    cfn = utils.expES('%FLASH0%\\Projects\\py-test\\plaunch_flash_' + vl + '.json')
    splobj = {}
    try:
        splobj = json2.readConfig(cfn)
    except Exception as e:
        utils.errlog(e)
        raise e

    for k in splobj['paths'].copy().keys():
        if not splobj['paths'][k]['include']:
            del splobj['paths'][k]

    ae1 = dirutils.dirsContainingType(
        Dir.findDL(vl) + '\\',
        {".acm",".ax",".bat",".cmd",".com",".cpl",".dll",".drv",".efi",".exe",".js",".jse",".msc",".mui",".ocx",".scr",".sys",".tsp",".vbe",".vbs",".wsf",".wsh"},
        False,
        [Dir.findDL(vl) + '\\' + 'FQZGJQYA']
        )
    def run(k):
        return k['path'].lower()
    ae2 = sorted(ae1, key=run)
    for a in ae2:
        if a['path'][1:2] == ':':
            a['path'] = a['path'][2:]
    for pd in ae2:
        def ni():
            if not pd['path'] in splobj['paths']:
                return pd['include']
            else:
                return splobj['paths'][pd['path']]['include']
        splobj['paths'][pd['path']] = {
            'include': ni()
            # ,'files': pd.files
        }
    json2.writeConfig(splobj, cfn)

def run():
    # doFlashDrive('CODE')
    doFlashDrive('CODE0')

if __name__ == "__main__":
    run()
