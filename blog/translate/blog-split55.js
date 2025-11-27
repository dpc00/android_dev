function OnStart() {
    db = app.OpenDatabase(dbfn);
    cashb = new Mvar("Cash", "");
    fsb = new Mvar("FS", "");
    dxb = new Mvar("DX", "");
    cashb.isbal = true;
    fsb.isbal = true;
    dxb.isbal = true;
    davg = new Mvar("DAvgExp", "readonly,nokeyboard");
    davg.te.SetTextColor("turquoise");
    dallow = new Mvar("DAllow", "readonly,nokeyboard");
    dallow.te.SetTextColor("fuchsia");
    inec = new Mvar("INec", "readonly,nokeyboard");
    inec.te.SetTextColor("green");
    dtot = new Mvar("DTotExp", "readonly,nokeyboard");
    dtot.te.SetTextColor("blue");
    tleft = new Mvar("TLeft", "readonly,nokeyboard");
    tleft.te.SetTextColor("red");
    maxdl = new Mvar("MaxDL", "readonly,nokeyboard");
    proxynums();
    loadnums();
    let b1 = app.CreateButton("Update", 0.5, bsz);
    b1.SetOnTouch(() => {
        slow(() => {
            cashb.save();
            fsb.save();
            dxb.save();
            davg.save();
            dallow.save();
            inec.save();
            dtot.save();
            tleft.save();
            maxdl.save();
            update_ietbl();
            et.dispatchEvent(new Event("update"));
        });
    });
    let b2 = app.CreateButton("Exit", 0.5, bsz);
    b2ot = () => {
        if (db != null) {
            db.Close();
            db = null;
        }
        app.Exit();
    };
    b2.SetOnTouch(b2ot);
    window.onclose = b2ot;
    rcb = app.CreateCheckBox("Regen i/e tables");
    set_color(rcb);
    let ttl1 = app.CreateText("Balance Log");
    ttl1.SetTextSize(26);
    let lyo1 = app.CreateLayout("linear", "vertical, center");
    lyo1.AddChild(cashb.lo);
    lyo1.AddChild(dxb.lo);
    lyo1.AddChild(fsb.lo);
    set_color(lyo1);
    let lyo2 = app.CreateLayout("linear", "vertical,center");
    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }
    los = [dallow.lo, inec.lo, tleft.lo, davg.lo, dtot.lo];
    shuffleArray(los);
    for (var i = 0; i < los.length; i++) {
        lyo2.AddChild(los[i]);
    }
    set_color(lyo2);
    let lyo0 = app.CreateLayout("linear", "vertical, center");
    lyo0.AddChild(ttl1);
    lyo0.AddChild(lyo1);
    lyo0.AddChild(lyo2);
    lyo0.AddChild(b1);
    lyo0.AddChild(b2);
    lyo0.AddChild(rcb);
    set_color(lyo0);
    lyo0.SetSize(1, 2);
    app.AddLayout(lyo0);
}

