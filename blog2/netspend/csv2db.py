# populates database from csv files

import csv
import datetime
import sqlite3

import fngen

fngen.clear()
fngen.init()

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute("""
    delete from transactions;
""")

sources = [
    "SSA-EarlyRetirement",
    "SSA-SSI",
    "CODHS-OAP",
    "CODHS-FS",
    "Human-Cash",
    "Other-Unknown",
]
assets = ["Direct Express", "Netspend", "Colorado Quest", "Cash", "Unknown"]


def getopt(rw, opts):
    user_choice = 0
    print(rw)

    print("Available options:")
    for i, item in enumerate(opts):
        print(f"{i + 1}) {item}")

    while not (1 <= user_choice <= len(opts)):
        user_choice = int(input("Please enter your choice: "))
        print(f"{user_choice} selected")
        if not (1 <= user_choice <= len(opts)):
            print("Invalid choice. Please select from the available options.")

    print(f"You selected: {user_choice} {opts[user_choice - 1]}")
    return user_choice


def do_one(csv_path):
    print(csv_path)
    with open(csv_path, "rt") as f:
        st = csv.reader(f)

        it = st
        # it.sort(key=lambda i: i['section'])

        # {'Withdrawals and Debits', 'Deposits and Credits'}

        income = 0
        expense = 0

        for rw in it:
            if float(rw[2]) > 0:
                income += float(rw[2])
            elif float(rw[2]) < 0:
                expense -= float(rw[2])
            cursor.execute(
                """
                insert into transactions (day, asset, description, amount)
                values (?,?,?,?);
            """,
                (
                    datetime.date.fromisoformat(rw[0]),
                    2,
                    rw[1].lstrip("'").rstrip("'"),
                    float(rw[2]),
                ),
            )
        conn.commit()

        print(f"income: {income:,>.2f}")
        print(f"expense: {expense:,>.2f}")

        f.close()


for fn in fngen.fns:
    do_one(f"{fn}.csv")


conn.close()
