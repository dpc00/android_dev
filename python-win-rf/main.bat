cd \projects\python-win-rf
del temp.log
del temp.raw
ngspice -b -o temp.log -r temp.raw main.cir