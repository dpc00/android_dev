# populates database from json files

import datetime
import json
import sqlite3

import fngen

fngen.clear()
fngen.init()

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute(
    """
	DROP TABLE income;
	"""
)

cursor.execute(
    """
	DROP TABLE expense;
	"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS income ( 
	time                 DATETIME     ,
	source_id            INT     ,
	asset_id             INT     ,
	value                NUMERIC(6,2) 
 );
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS expense (
	time                 DATETIME     ,
	asset_id             INT     ,
	'type'               TEXT     ,
	value                NUMERIC(6,2)
 );
"""
)

conn.commit()


# json_path = r'netspend-statement-feb-2020.json'
# json_path = r'netspend-statement-mar-2020.json'
# json_path = r'netspend-statement-apr-2020.json'
# json_path = r'netspend-statement-sep-2025.json'


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
    s = s.replace("Credit: ", "")
    s = s.replace("Debit: ", "")
    return s


def do_one(json_path):
    with open(json_path, "rt") as f:
        st = json.load(f)

    print(sorted(st.keys()))
    print("========")

    it = st["accounts"][0]
    # it.sort(key=lambda i: i['section'])

    # {'Withdrawals and Debits', 'Deposits and Credits'}

    income = 0
    expense = 0

    for i in it["transactions"]:
        if i["credit_amount"] != None:
            income += i["credit_amount"]
            cursor.execute(
                """
				INSERT INTO income (time, source_id, asset_id, value) 
				VALUES (?,?,?,?)
				""",
                [
                    datetime.date.fromisoformat(i["date"])
                    if i["date"] is not None
                    else None,
                    5,
                    2,
                    i["credit_amount"],
                ],
            )
            # conn.commit()
        elif i["debit_amount"] != None:
            expense += i["debit_amount"]
            cursor.execute(
                """
				INSERT INTO expense (time, asset_id, "type", value)
				VALUES (?, ?, ?, ?)
				""",
                [
                    datetime.date.fromisoformat(i["date"])
                    if i["date"] is not None
                    else None,
                    2,
                    clean_desc(i),
                    i["debit_amount"],
                ],
            )
            # conn.commit()
        else:
            print("no amt", i)
    conn.commit()

    print(f"income: {income:,>.2f}")
    print(f"expense: {expense:,>.2f}")

    for i in [
        it["summaries"],
        it["beginning_balance"],
        it["ending_balance"],
        st["beginning_balance"],
        st["ending_balance"],
    ]:
        print(i)


for fn in fngen.fns:
    do_one(f"{fn}.json")
