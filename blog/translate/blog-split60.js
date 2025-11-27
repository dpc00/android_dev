function sql(stmnt, dat) {
    if (db == null) {
        db = app.OpenDatabase(dbfn);
        db.ExecuteSql("PRAGMA synchronous = OFF");
    }
    return new Promise((res, err) => {
        db.ExecuteSql(stmnt, dat, res, err);
    }).catch((err) => {
        app.Alert(err + "," + stmnt + "," + dat);
    });
}

