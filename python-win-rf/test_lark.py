import lark

f1 = open("spice_cir.lark")
f2 = open("temp.sp")

ebnf = f1.read(-1)
txt = f2.read(-1)

parser = lark.Lark(ebnf)

t = parser.parse(txt)
open("temp.tree", "w").write(t.pretty())
