function fixtbl() {
    let sqlt1 =
        "CREATE TABLE IF NOT EXISTS tmpc (ts TIMESTAMP PRIMARY KEY NOT NULL,cash REAL,fs REAL,dx REAL)";
    sql(sqlt1);
    sql("DELETE FROM tmpc");
    let res = sql("select * from currentc order by ts");
    for (let i = 0; i < res.rows.length; i++) {
        let row = res.rows.item(i);
        sql("insert into tmpc (ts,cash,fs,dx) values (?,?,?,?)", [
            new Date(row.ts).toISOString(),
            row.cash,
            row.fs,
            row.dx,
        ]);
    }
    app.Exit();
}

