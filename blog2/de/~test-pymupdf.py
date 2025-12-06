# appears to try to make csv files from pdfs, doesn't find the data well though
# tuning this might work but appears that it would be extremely harf

import datetime as dt
import json
import os
import sys
from pprint import pprint

import pymupdf

import fngen

fngen.clear()
fngen.init(".csv2")


def abort1(rc):
    sys.exit(rc)


while fngen.hasnext():
    fn = fngen.next()
    print(f"{fn}.pdf")

    doc = pymupdf.open(f"{fn}.pdf")

    for page in doc:
        tabs = page.find_tables(
            strategy="text"
        )  # locate and extract any tables on page
        print(f"{len(tabs.tables)} found on {page}")  # display number of found tables

        for tt in tabs.tables:  # at least one table found?
            pprint(tt.extract())  # print content of first table
    continue

    tn = 1
    tt = []
    for j, tbl in enumerate(tables):
        # if tn == 1:
        #     tn = 0
        #     continue
        for rw in tbl.df[0]:
            rt = rw.split("\n")
            print(rt)
            continue
            if (
                rt[0]
                in [
                    "Total Fees",
                    "Total Other Fees",
                    "Total Reversed Fees",
                    "Total Returned Item Fees",
                    "Total Overdraft Fees",
                    "Total Deposits and Credits",
                    "Total Withdrawals and Debits",
                ]
                or rt == ["Date Posted", "Description", "Amount"]
                or rt == ["This Month", "YTD"]
                or rt == ["Date ", "Description", "Amount", "Posted"]
            ):
                print(f"skipping row: {rt}")
                continue
            else:
                # rt.sort()
                if rt[2][0] == "$":
                    try:
                        rt[2] = rt[2].replace(",", "")
                        rt[2] = float(rt[2][1:])
                    except Exception as e:
                        print(f"bad number in {fn}.pdf: {rt[2]}")
                        print(rt)
                        raise e
                try:
                    rt[0] = dt.date.strptime(rt[0], "%m/%d/%Y")
                except Exception as e:
                    print(f"bad date in {fn}.pdf: {rt[0]}")
                    print(f"rt: {rt}")
                    if len(rt) > 3:
                        tdt = rt[0] + rt[3]
                        try:
                            rt[0] = dt.date.strptime(tdt, "%m/%d/%Y")
                            rt.pop()
                            print(f"fix1 worked: {rt}")
                        except Exception as e:
                            try:
                                rt[1] = dt.date.strptime(rt[1], "%m/%d/%Y")
                                tmp = rt.pop(1)
                                rt.insert(0, tmp)
                                print(f"fix2 worked: {rt}")
                            except Exception as e:
                                print(f"neither fix worked: {tdt}")
                                raise e
                    else:
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
                if "," in rt[1]:
                    rt[1] = rt[1].replace(",", " ")
            tt.append(rt)
        tts = ""
        for s in tt:
            tts += str(s[0]) + ","
            tts += "'" + s[1] + "'" + ","
            tts += str(s[2])
            tts += "\n"

    with open(f"{fn}.csv2", "wt") as f:
        f.write(tts)
    print("-" * 10)
    print(tts)
