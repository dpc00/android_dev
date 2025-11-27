function mtbl() {
    let mex = me();
    if (mex && dirty4) {
    } else {
        if (!mex) {
            sql(mtbl_cs);
            dirty4 = true;
        }
    }
    return mex;
}

