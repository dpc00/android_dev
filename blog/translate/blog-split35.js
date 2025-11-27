function davg_dtot_calc() {
    let res = sql(
        "SELECT * FROM daily WHERE 'ts' IS NOT NULL ORDER BY 'ts' ASC;"
    );
    let rc = res.rows.length;
    sc = 14;
    bd = new Date(res.rows.item(rc - sc - 1).ts);
    ed = new Date(res.rows.item(rc - 1).ts);
    dd = (ed.getTime() - bd.getTime()) / (1000 * 60 * 60 * 24);
    var te = 0;
    for (i = rc - sc - 1; i < rc; i++) {
        let r = res.rows.item(i);
        te += r.cash_spent;
        te += r.dx_spent;
        if (i == rc - 1) {
            let tmp = ncs(r.cash_spent + r.dx_spent);
            dtot.te.SetText(tmp);
            dtot.save();
            dtot.lbl.SetText(r.ts);
        }
    }
    let tmp = ncs(te / dd);
    davg.te.SetText(tmp);
    davg.save();
}

