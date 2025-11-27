#!/data/data/com.termux/files/usr/bin/env python

from subprocess import run


def srun(cmd, **kwargs):
    print(cmd)
    for k in kwargs:
        print(k, '=', kwargs[k])
    return run(cmd, shell=True).returncode


cmd = 'echo ghello | grep "hell"'
print(cmd)


def func(f2n, ol):
    print(ol)

    def f1():
        return globals()[f2n](**ol)

    return f1


f2 = func('srun', {'cmd': cmd, 'option1': "fdfgg", 'option2': "fyffggfg"})

rc = f2()
print('rc: ' + str(rc))
