#!/data/data/com.termux/files/usr/bin/env python
from glob import glob

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PrologLexer

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
