# makes csv files from netspend pdfs using camelot

import datetime as dt
import json
import os
import sys

import camelot

import fngen

fngen.clear()
fngen.init(".csv")


def abort1(rc):
    sys.exit(rc)


def c2f(ns):
    ns = ns.replace(",", "")
    ns = ns.replace("$", "")
    return float(ns)


while fngen.hasnext():
    fn = fngen.next()
    print(f"processing {fn}.pdf")
    if not os.path.exists(f"{fn}.pdf"):
        open(f"{fn}.csv", "wt")
        continue
    tables = camelot.read_pdf(f"{fn}.pdf", pages="all")
    tn = 1
    tt = []
    tts = ""
    for j, tbl in enumerate(tables):
        if tn == 1:
            tn = 0
            continue
        for rw in tbl.df[0]:
            rt = rw.split("\n")
            match rt[0]:
                case "Total Fees":
                    print(f"skipping row: {rt}")
                    continue
                case "Total Other Fees":
                    print(f"skipping row: {rt}")
                    continue
                case "Total Reversed Fees":
                    print(f"skipping row: {rt}")
                    continue
                case "Total Returned Item Fees":
                    print(f"skipping row: {rt}")
                    continue
                case "Total Overdraft Fees":
                    print(f"skipping row: {rt}")
                    continue
                case "Total Deposits and Credits":
                    income = c2f(rt[1])
                    print(f"skipping row: {rt}")
                    continue
                case "Total Withdrawals and Debits":
                    expense = c2f(rt[1])
                    print(f"skipping row: {rt}")
                    continue
                case "Summary of Fees Charged to Your Card Account":
                    print(f"skipping row: {rt}")
                    continue
            match rt:
                case ["Date Posted", "Description", "Amount"]:
                    print(f"skipping row: {rt}")
                    continue
                case ["This Month", "YTD"]:
                    print(f"skipping row: {rt}")
                    continue
                case ["Date ", "Description", "Amount", "Posted"]:
                    print(f"skipping row: {rt}")
                    continue
            fixing = False
            while True:
                de = set()
                for i in range(0, len(rt)):
                    try:
                        dt.date.strptime(rt[i], "%m/%d/%Y")
                    except ValueError as e:
                        de.add(i)
                if de == {1, 2}:
                    if fixing:
                        print(f"fixed rt:{rt}")
                        fixing = False
                    break
                print(f"odd de: {de} rt: {rt}")
                fixing = True
                if de == {0, 1, 2, 3}:
                    try:
                        dt.date.strptime(rt[0] + rt[3], "%m/%d/%Y")
                        rt[0] += rt[3]
                        rt.pop(3)
                        continue
                    except ValueError as e:
                        raise e
                if de == {0, 1, 2, 3, 4}:
                    try:
                        dt.date.strptime(rt[0] + rt[3], "%m/%d/%Y")
                        rt[0] += rt[3]
                        rt[1] += rt[4]
                        rt.pop(3)
                        rt.pop(3)
                        continue
                    except ValueError as e:
                        raise e
                if de == {0, 2, 3}:
                    rt[0] += rt[3]
                    rt.pop(3)
                    rt[0], rt[1] = rt[1], rt[0]
                    continue
                print(f"unhandled de: {de} rt: {rt}")
                raise ValueError

            rt[0] = dt.date.strptime(rt[0], "%m/%d/%Y")
            try:
                rt[2] = c2f(rt[2])
            except Exception as e:
                print(f"bad number in {fn}.pdf: {rt}")
                raise e
            try:
                if rt[1].startswith("Debit: "):
                    rt[2] = -rt[2]
                    rt[1] = rt[1][7:]
                elif rt[1].startswith("Credit: "):
                    rt[1] = rt[1][8:]
            except Exception as e:
                print(f"bad rt: {rt}")
                print(rt)
                raise e
            if "," in rt[1]:  # comma in csv field means future disaster
                rt[1] = rt[1].replace(",", " ")
            tt.append(rt)
    for s in tt:
        tts += str(s[0]) + ","
        tts += "'" + s[1] + "'" + ","
        tts += str(s[2])
        tts += "\n"

    print(f"writing {fn}.csv")
    with open(f"{fn}.csv", "wt") as f:
        f.write(tts)
    print("-" * 10)
    print(tts)
