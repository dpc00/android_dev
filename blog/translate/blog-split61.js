function tblexists(nm) {
    let res = sql(
        "SELECT COUNT() AS cnt FROM sqlite_master WHERE type='table' AND name=?",
        [nm]
    );
    return res.rows.item(0).cnt > 0;
}

