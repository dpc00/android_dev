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
            balance REAL
         );
    """)
    # conn.commit()
    cursor.execute("""
            insert into blog2
            select * from blog
            order by time;
    """)
    # conn.commit()
    cursor.execute("""
        drop table if exists blog_bak;
    """)
    cursor.execute("""
        alter table blog rename to blog_bak
    """)
    cursor.execute("""
        alter table blog2 rename to blog;
    """)
    conn.commit()


if __name__ == "__main__":
    f1()
