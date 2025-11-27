import esprima
import json

with open("blog.js","r") as fh:
    txt = fh.read()

js_ast = esprima.parseScript(txt)

with open("blog-script.txt", "w") as fh:
    for it in js_ast.body:
        fh.write(str(it)+'\n')
    
