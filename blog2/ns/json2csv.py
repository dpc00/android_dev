import csv
import datetime as dt
import json
import sqlite3

import fngen

fngen.clear()
fngen.init(".csv")

while fngen.hasnext():
    fn = fngen.next()
    print(f"processing {fn}.json")

    with open(f"{fn}.json", "rt") as f:
        st = json.load(f)

    print(sorted(st.keys()))
    print("========")

    it = st["accounts"][0]
    trs = it["transactions"]
    for i, r in enumerate(trs):
        if i < len(trs) - 1:
            j = i + 1
            d1 = trs[i]["description"]
            d2 = trs[j]["description"]
            if "\n" in d1:
                ts = d1.split("\n")
                trs[i]["description"] = ts[0]
                if ts[1] != "CA US":
                    if not trs[j]["description"].startswith("COM"):
                        trs[j]["description"] = ts[1] + " " + trs[j]["description"]
                    elif ts[1].endswith("."):
                        trs[j]["description"] = ts[1] + trs[j]["description"]
                else:
                    trs[i]["description"] = " ".join(ts)

    tt = []
    tts = ""
    for i in it["transactions"]:
        rt = [None, None, None]
        rt[0] = dt.datetime.strptime(i["posted_date"] or i["date"], "%Y-%m-%d")
        if i["credit_amount"] != None:
            rt[2] = i["credit_amount"]
        elif i["debit_amount"] != None:
            rt[2] = i["debit_amount"]
        else:
            print("no amt", i)
        rt[1] = i["description"]
        if rt[1].startswith("Debit: "):
            rt[2] = -rt[2]
            rt[1] = rt[1][7:]
        elif rt[1].startswith("Credit: "):
            rt[1] = rt[1][8:]
        if "," in rt[1]:  # comma in csv field means future disaster
            rt[1] = rt[1].replace(",", " ")
        if "\n" in rt[1]:
            rt[1].replace("\n", " ")
        if "\t" in rt[1]:
            rt[1].replace("\t", " ")
        if "  " in rt[1]:
            rt[1].replace("  ", " ")
        tt.append(rt)
    for s in tt:
        tts += s[0].strftime("%Y-%m-%d") + ","
        tts += "'" + s[1] + "'" + ","
        tts += str(s[2])
        tts += "\n"
    print(f"writing {fn}.csv")
    with open(f"{fn}.csv", "wt") as f:
        f.write(tts)
    print("-" * 10)
    print(tts)
