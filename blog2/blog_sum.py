import datetime
import locale
import math
import sqlite3

dbstarted = False


def dbstart():
    global conn, cursor, dbstarted
    if not dbstarted:
        conn = sqlite3.connect("finance.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        dbstarted = True


def sum_blog():
    global conn, cursor
    dbstart()
    c1 = cursor.execute("""
        select * from blog
        order by time;
    """)
    bb = {}
    eb = {}
    rws = c1.fetchall()
    inc = {}
    exp = {}
    for r in rws:
        aid = r["asset_id"]
        amt = r["amount"]
        bal = r["balance"]
        if aid not in bb:
            bb[aid] = bal
            eb[aid] = bal
            inc[aid] = 0
            exp[aid] = 0
        if amt > 0:
            inc[aid] += amt
        elif amt < 0:
            exp[aid] += amt
        eb[aid] = bal

    print(f"aid beginning ending   income  expense")
    for aid in bb:
        print(
            f"{aid:>2} {bb[aid]:>8.2f} {eb[aid]:>8.2f} {inc[aid]:>8.2f} {exp[aid]:>8.2f}"
        )
    print(
        f"{'total':>20} {round(sum(inc.values()), 2):>8.2f} {round(sum(exp.values()), 2):>8.2f}"
    )


if __name__ == "__main__":
    sum_blog()
