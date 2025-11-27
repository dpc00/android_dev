function inec_calc() {
    let res1 = davg.num - dallow.num;
    inec.te.SetText(ncs(res1 * maxdl.num));
    inec.save();
}

