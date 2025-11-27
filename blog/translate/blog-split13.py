__all__ = ['blog-split13']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['dtbl_cs'])
Js('use strict')
var.put('dtbl_cs', Js('CREATE TABLE daily (ts TIMESTAMP PRIMARY KEY,cash_recd REAL,fs_recd REAL,dx_recd REAL,cash_spent REAL,fs_spent REAL,dx_spent REAL)'))
pass


# Add lib to the module scope
blog-split13 = var.to_python()