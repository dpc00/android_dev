# appears to make csv files from json files

import datetime
import json
import sqlite3

import fngen

fngen.clear()
fngen.init(".csv")


def get_date_from_transaction(i):
    if i["posted_date"] is not None:
        return datetime.date.fromisoformat(i["posted_date"])
    elif i["date"] is not None:
        return datetime.date.fromisoformat(i["date"])
    else:
        return None


def clean_desc(i):
    s = i["description"]
    s = s.replace("\n", " ")
    s = s.replace(",", "")
    return s


def do_one(json_path):
    with open(json_path, "rt") as f:
        st = json.load(f)

    it = st["accounts"][0]
    # it.sort(key=lambda i: i['section'])

    income = 0
    expense = 0

    tts = ""

    it["transactions"].sort(key=lambda w: len(it) - w["order"])
    for i in it["transactions"]:
        tl = ["", "", 0]
        if i["debit_amount"] != None:  # should be in credit field
            income += i["debit_amount"]
            tl[0] = get_date_from_transaction(i)
            tl[1] = clean_desc(i)
            tl[2] = i["debit_amount"]
            # conn.commit()
        elif i["credit_amount"] != None:  # should be in debit field
            expense += i["credit_amount"]
            tl[0] = get_date_from_transaction(i)
            tl[1] = clean_desc(i)
            tl[2] = -i["credit_amount"]
            # conn.commit()
        else:
            print("no amt", i)
        tts += str(tl[0]) + ","
        tts += "'" + tl[1] + "',"
        tts += str(tl[2])
        tts += "\n"

    with open(f"{fn}.csv", "wt") as f:
        f.write(tts)
    print(tts)


for fn in fngen.fns:
    do_one(f"{fn}.json")
    print("-" * 10)
