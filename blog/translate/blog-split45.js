function ietbl() {
    let iex = iee();
    if (iex && dirty2) {
    } else {
        if (!iex) {
            sql(ietbl_cs);
            dirty2 = true;
        }
    }
    return iex;
}

