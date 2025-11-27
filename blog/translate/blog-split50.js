function maxdl_calc() {
    let cashd = dl(5, 28);
    let dxd = dl(5, 3);
    maxdl.te.SetText(ncs(Math.max(cashd, dxd)));
    maxdl.num = ncs(Math.max(cashd, dxd));
}

