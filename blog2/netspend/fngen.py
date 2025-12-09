import datetime
import os
import pickle

# import pyperclip
from pprint import pprint

# import json

file_path = "fngen.pickle"

sext = ".csv"

fns = []


def load():
    global fns
    print(f"loading {file_path}...")
    with open(file_path, "rb") as f:
        fns = pickle.load(f)
    return


def init(ext=sext):
    global fns, sext

    sext = ext

    if os.path.exists(file_path):
        load()
        return

    print(f"creating {sext} base file name array {file_path}...")

    sd = datetime.date(2020, 2, 1)
    ed = datetime.date.today()
    ed = datetime.date(ed.year, ed.month - 1, 1)

    def incd(d):
        m = d.month
        if m < 12:
            return datetime.date(d.year, d.month + 1, d.day)
        else:
            return datetime.date(d.year + 1, 1, 1)

    cd = sd

    while cd <= ed:
        fn = f"netspend-statement-{cd.strftime('%b-%Y')}"
        fns.append(fn)
        cd = incd(cd)
    save()


def save():
    global fns
    print(f"saving pdf file name array {file_path}...")
    with open(file_path, "wb") as f:
        pickle.dump(fns, f)
    # pprint(fns)


def next():
    global fns
    ch = False
    while len(fns) > 0 and os.path.exists(f"{fns[0]}{sext}"):
        ch = True
        fns.pop(0)
    # pyperclip.copy(fns[0])
    if ch:
        save()
    return fns[0] if len(fns) > 0 else None


def hasnext():
    next()
    return len(fns) > 0


def clear():
    if os.path.exists(file_path):
        os.remove(file_path)
