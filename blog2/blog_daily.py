import sqlite3

dbstarted = False


def dbstart():
    global conn, cursor, dbstarted
    if not dbstarted:
        conn = sqlite3.connect("finance.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        dbstarted = True


dbstart()


def daily():
    c1 = cursor.execute("""
        select asset_id, strftime("%Y-%m-%d", time) as day, round(sum(amount),2) as total from blog
        where amount < 0
        group by strftime("%Y-%m-%d", time);
    """)
    rows = c1.fetchall()
    print("day asset total")
    rc = 0
    rt = 0
    for r in rows:
        print(f"{r['day']} {r['total']}")
        rc += 1
        rt += r["total"]
    print(f"{rc} days {round(rt, 2)} total {round(rt / rc, 2)} avg daily expense")


if __name__ == "__main__":
    daily()
