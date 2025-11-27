'''
Created on Jul 2, 2016

@author: BPLPatron
'''
import utils
from collections import Counter

pcnt = 0
colw = 13

fcstats = Counter()

fcstats2 = Counter()

def cpy():
    for k in fcstats.keys():
        fcstats2[k] = fcstats[k]

def chk():
    for k in fcstats.keys():
        if fcstats2[k] != fcstats[k]:
            cpy()
            return True
    return False

def clr():
    for k in fcstats.keys():
        fcstats[k] = 0
    cpy()

def rightJ(s, l):
    while len(s) < l:
        s = ' ' + s
    return s

def formatNumber(num):
    return "{:15,}".format(num)

def fixedD(num, l):
    return ('{:' + str(l) + ',}').format(num)

def fixedS(s, l):
    return ('{:>' + str(l) + '}').format(s)

hprinted = False

def printHeader():
    global pcnt
    global colw
    if pcnt % 1 == 0:
        utils.writedata('\r\n')
        utils.writedata('\r\n')
        for k in fcstats.keys():
            utils.writedata(fixedS(k, colw))
        utils.writedata('\r\n')
        for k in fcstats.keys():
            utils.writedata(fixedS('----', colw))
        # utils.writedata('\r\n');
    pcnt += 1

def oprint():
    global colw
    if chk():
        utils.writedata('\r\n')
        for k, v in sorted(fcstats.items()):
            utils.writedata(fixedS(k, colw))
            utils.writedata(': ')
            utils.writedata(fixedD(v, colw))
            utils.writedata('\n')

cpy()
