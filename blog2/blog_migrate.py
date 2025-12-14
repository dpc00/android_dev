import sqlite3

dbstarted = False


def dbstart():
    global conn, cursor, dbstarted
    if not dbstarted:
        conn = sqlite3.connect("finance.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        dbstarted = True


def f1():
    global conn, cursor
    dbstart()
    cursor.execute("""
        drop table if exists blog2
    """)
    cursor.execute("""
        create table blog2
        (
            time TIMESTAMP,
            asset_id INTEGER,
            source_receipt INTEGER, 
            type INTEGER,
            amount REAL,
            balance REAL
         );
    """)
    # conn.commit()
    c1 = cursor.execute("""
        select * from blog order by time;
    """)
    acc = {}
    rws = c1.fetchall()
    for r in rws:
        aid = r["asset_id"]
        bal = r["balance"]
        tm = r["time"]
        if aid not in acc:
            acc[aid] = bal
        amt = bal - acc[aid]
        ty = 0 if amt > 0 else 1 if amt < 0 else None
        cursor.execute(
            """
            insert into blog2 (time, asset_id, type, amount, balance)
            values (?,?,?,?,?);
        """,
            [tm, aid, ty, amt, bal],
        )
        acc[aid] = bal
    # conn.commit()
    cursor.execute("""
        drop table if exists blog_bak;
    """)
    conn.commit()


if __name__ == "__main__":
    f1()
