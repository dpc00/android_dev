function lts() {
    let res = sql("SELECT ts FROM currentc ORDER BY ts DESC");
    return res.rows.item(uc).ts;
}

