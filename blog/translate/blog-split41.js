function dtbl() {
    let dex = de();
    if (dex && dirty3) {
    } else {
        if (!dex) {
            sql(dtbl_cs);
            dirty3 = true;
        }
    }
    return dex;
}

