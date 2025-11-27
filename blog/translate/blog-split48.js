function log_balances() {
    sql("INSERT INTO currentc (ts, cash, fs, dx) VALUES (?,?,?,?)", [
        new Date().toISOString(),
        cashb.num,
        fsb.num,
        dxb.num,
    ]);
    dirty2 = true;
    uc++;
}

