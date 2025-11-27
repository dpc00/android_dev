import json

with open("tool/lint-all.json", "r") as fh:
    js = fh.read()

arr = json.loads(js)
arr.sort(key=lambda msg: msg["message-id"])

na = {}
for msg in arr:
    d1 = {"path": msg["path"], "line": msg["line"], "msg": msg["message"]}
    sym = msg["message-id"] + "-" + msg["symbol"]
    if sym in na:
        na[sym].append(d1)
    else:
        na[sym] = [d1]

for sym in na.keys():
    na[sym].sort(key=lambda k: (k["path"], k["line"]))


txt = json.dumps(na, indent=4)

with open("tool/lint-all.jtxt", "w") as fh:
    fh.write(txt)

ot = ""

for sym in na.keys():
    for it in na[sym]:
        ot += f'{sym:32} {it["path"]:18} {it["line"]:4} {it["msg"]}\n'

with open("tool/lint-all.jtxt.rfm", "w") as fh:
    fh.write(ot)
