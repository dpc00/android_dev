function ib() {
    let ft = app.ReadFile(app.GetPath() + "/blog2.csv");
    let lna = ft.split("\n");
    for (i = 0; i < lna.length; i++) {
        let f = lna[i].split(",");
        let tp = f[1].split(":");
        if (Number(tp[0]) < 10) tp[0] = "0" + Number(tp[0]);
        f[1] = tp.join(":");
        let ts = f[0] + " " + f[1];
        let res = sql(
            "INSERT INTO currentc (ts, cash, fs, dx) VALUES (?,?,?,?)",
            [new Date(ts).toISOString(), f[2], f[3], f[4]]
        );
    }
    app.Exit();
}

