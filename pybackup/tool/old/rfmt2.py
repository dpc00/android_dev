#!/data/data/com.termux/files/usr/bin/env python
from glob import glob
from sys import exit

# from funcs import srun
# from gb_env import pdir
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

print("-- rfmt2.py --")

# cmd = 'yapf -i -r -vv ' + pdir['pyth'] + '/*.py'

for fn in glob("/sdcard/projects/pybackup/*.py"):
    with open(fn, "r") as fv:
        code = fv.read()
        with open(fn + ".html", "w") as fv2:
            highlight(code, PythonLexer(), HtmlFormatter(full=True), outfile=fv2)
