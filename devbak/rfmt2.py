#!/data/data/com.termux/files/usr/bin/env python
from pygments.formatters import HtmlFormatter
from pygments.lexers import PrologLexer
from pygments import highlight
from sys import exit
from glob import glob
from gb_env import pdir
from funcs import srun
print("-- rfmt2.py --")

# cmd = 'yapf -i -r -vv ' + pdir['pyth'] + '/*.py'

for fn in glob("/sdcard/projects/prolog/*.pl"):
    with open(fn, "r") as fv:
        code = fv.read()
        with open(fn + ".html", "w") as fv2:
            highlight(code,
                      PrologLexer(),
                      HtmlFormatter(full=True),
                      outfile=fv2)
