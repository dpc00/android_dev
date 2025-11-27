function tleft_calc() {
    let tf = cashb.num + dxb.num;
    let tl = tf / davg.num;
    let tmp = ncs(tl);
    tleft.te.SetText(tmp);
    tleft.save();
}

