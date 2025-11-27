function update_ietbl() {
    app.ShowProgressBar("updating tables...");
    let pd = lts();
    let iex = ietbl();
    let wh = "";
    if (iex && !rcb.GetChecked()) {
        wh = " WHERE ts>='" + pd + "'";
    }
    if (dirty2 || rcb.GetChecked()) {
        let ss = "SELECT ts, cash, fs, dx FROM currentc" + wh + " ORDER BY ts";
        let res = sql(ss);
        let rc = res.rows.length;
        let j = 0;
        let i = 1;
        db.transaction(function (tx) {
            for (; i < rc; i++) {
                let pr = res.rows.item(j);
                let cr = res.rows.item(i);
                let bts = pr.ts;
                let ets = cr.ts;
                let cash_diff = nc(cr.cash - pr.cash);
                let fs_diff = nc(cr.fs - pr.fs);
                let dx_diff = nc(cr.dx - pr.dx);
                let cash_recd = cash_diff > 0 ? cash_diff : null;
                let fs_recd = fs_diff > 0 ? fs_diff : null;
                let dx_recd = dx_diff > 0 ? dx_diff : null;
                let cash_spent = cash_diff < 0 ? nc(-cash_diff) : null;
                let fs_spent = fs_diff < 0 ? nc(-fs_diff) : null;
                let dx_spent = dx_diff < 0 ? nc(-dx_diff) : null;
                if (cash_diff != 0 || fs_diff != 0 || dx_diff != 0) {
                    let res2 = tx.executeSql(
                        "INSERT OR REPLACE INTO inc_exp (bts, ets, cash_recd, fs_recd, dx_recd, cash_spent, fs_spent, dx_spent) VALUES (?,?,?,?,?,?,?,?)",
                        [
                            bts,
                            ets,
                            cash_recd,
                            fs_recd,
                            dx_recd,
                            cash_spent,
                            fs_spent,
                            dx_spent,
                        ]
                    );
                    j = i;
                    dirty3 = true;
                }
                uc--;
                app.UpdateProgressBar((i * 80) / rc);
            }
        });
        dirty2 = false;
    }
    app.UpdateProgressBar(80);
    let dex = dtbl();
    wh = "";
    if (dex && !rcb.GetChecked()) {
        wh =
            " WHERE substr(datetime(ets,'localtime'), 1, 10)>='" +
            new Date(pd).toLocaleDateString("fr-CA").substring(0, 10) +
            "'";
        app.ShowPopup(wh);
    }
    if (dirty3 || rcb.GetChecked()) {
        let sst =
            " SELECT substr(datetime(ets,'localtime'), 1, 10) AS ts, SUM(cash_recd) AS cash_recd, SUM(fs_recd) AS fs_recd, SUM(dx_recd) AS dx_recd, SUM(cash_spent) AS cash_spent, SUM(fs_spent) AS fs_spent, SUM(dx_spent) AS dx_spent FROM inc_exp" +
            wh +
            " GROUP BY substr(datetime(ets,'localtime'), 1, 10)";
        sql("INSERT OR REPLACE INTO daily" + sst);
        dirty3 = false;
        dirty4 = true;
    }
    app.UpdateProgressBar(90);
    let mex = mtbl();
    wh = "";
    if (mex && !rcb.GetChecked()) {
        wh =
            " WHERE substr(datetime(ets,'localtime'), 1, 7)>='" +
            new Date(pd).toLocaleDateString("fr-CA").substring(0, 7) +
            "'";
    }
    if (dirty4 || rcb.GetChecked()) {
        let sst =
            " SELECT substr(datetime(ets,'localtime'), 1, 7) AS ts, SUM(cash_recd) AS cash_recd, SUM(fs_recd) AS fs_recd, SUM(dx_recd) AS dx_recd, SUM(cash_spent) AS cash_spent, SUM(fs_spent) AS fs_spent, SUM(dx_spent) AS dx_spent FROM inc_exp" +
            wh +
            " GROUP BY substr(datetime(ets,'localtime'), 1, 7)";
        sql("INSERT OR REPLACE INTO monthly" + sst);
        dirty4 = false;
    }
    app.UpdateProgressBar(100);
    app.HideProgressBar();
    if (rcb.GetChecked()) {
        uc = 0;
        rcb.SetChecked(false);
    }
}

