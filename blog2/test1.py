import csv
import sqlite3

conn = sqlite3.connect("finance.db")
db = conn.cursor()

db.execute("""
    select day, description, avg(amount) from transactions
    where amount<0 
    group by strftime("%Y-%m", day)
""")

rows1 = db.fetchall()

curbal = 0

with open(
    "daily.csv",
    "wt",
    newline="",
) as f:
    writer = csv.writer(f, quoting=csv.QUOTE_STRINGS)
    writer.writerows(rows1)
