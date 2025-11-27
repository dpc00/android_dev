class Mvar {
    constructor(n, ne) {
        this.num = 0;
        this.te = app.CreateTextEdit(
            "",
            0.5,
            tesz,
            "singleline" + (ne !== "" ? "," + ne : "")
        );
        this.name = n;
        this.te.SetHint(n);
        this.te.mvar = this;
        this.lbl = app.CreateText(this.name, 0.325, tsz, "right");
        this.lo = app.CreateLayout("linear", "horizontal");
        this.lo.AddChild(this.lbl);
        this.lo.AddChild(this.te);
        this.lo.SetSize(0.8, tesz);
        this.tf = function () {
            let res2, res3;
            let res1 = this.GetText();
            res2 = txtpa(res1);
            res3 = res2.reduce((a, c) => {
                return a + c;
            }, 0);
            if (res2.length == 0) {
            }
            app.ShowPopup(this.mvar.name + ": " + res1 + " = " + ncs(res3));
        };
        this.te.SetOnTouch(this.tf);
        this.cf = this.tf;
        this.te.SetOnChange(this.cf);
        set_color(this.te);
        set_color(this.lbl);
        set_color(this.lo);
    }
    save() {
        let txt = this.te.GetText();
        let ia = txtpa(txt);
        let acc = 0;
        for (let ci of ia) {
            acc = nc(acc + ci);
            this.newbal(acc);
        }
    }
    newbal(nb) {
        if (this.num !== nb) {
            this.num = nb;
            this.te.SetText(this.toString());
            SaveNumber(this.name, this.num);
            if (this.isbal) log_balances();
        }
    }
    toString() {
        return ncs(this.num);
    }
}

