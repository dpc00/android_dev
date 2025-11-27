function SaveNumber(name, num) {
    sql("UPDATE nums SET (num,ts)=(?,?) WHERE name=?", [
        num,
        new Date().toISOString(),
        name,
    ]);
}

