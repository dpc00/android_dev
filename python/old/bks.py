#!/data/data/com.termux/files/usr/bin/env python

import sh
import os
import pyDatalog
import traceback

my_ls = sh.ls.bake('-AgGlR', '--block-size=1', '--time-style=+%s',
                   '--color=never')

try:
    pdir = os.getenv('pyth')
    print('pdir: ' + pdir)

    tmp1 = os.fsdecode(sh.sha256sum(my_ls(pdir)).stdout)
    print('tmp1: ' + tmp1)
    tmp2 = os.getenv('dh') + '_' + 'pyth'
    print('tmp2: ' + tmp2)
    tmp3 = os.fsdecode(sh.cat(tmp2).stdout)
    print('tmp3: ' + tmp3)

    if (tmp1 != tmp3):
        tmp4 = os.getenv('rtbk') + '5'
        print('tmp4: ' + tmp4)
        sh.touch(tmp4)
        print(os.fsdecode(my_ls(tmp4).stdout))
        tmp5 = os.getenv('ct') + '3'
        print('tmp5: ' + tmp5)
        print(os.fsdecode(my_ls(tmp5).stdout))
except Exception as err:
    print(traceback.format_exc())
