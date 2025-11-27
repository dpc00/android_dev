'''
Created on Jun 28, 2016

@author: Phil
'''
import utils, json


def readConfig(fn):
    f = open(fn, 'r')
    rv = json.load(f)
    if rv is not None:
        utils.log(fn + ' loaded.')
        f.close()
        return rv
    else:
        utils.log('error parsing ' + fn)
        f.close()
        return None

def writeConfig(obj, fn):
    obj_s = json.dumps(obj, indent='\t')
    f = open(fn, 'w')
    f.write(obj_s)
    f.close()
    utils.log(fn + ' written.')

# cfn1 = utils.expES('%FLASH0%\\Projects\\tools\\plaunch_flash_CODE0.json')
# cfn2 = utils.expES('%FLASH0%\\Projects\\tools\\plaunch_flash_CODE0.test')

# jso = readConfig(cfn1)

# writeConfig(jso, cfn2)
