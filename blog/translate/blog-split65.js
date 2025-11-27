function txtpa(txt) {
    let re = /([+\-]?\s*([0-9,]*)([\.][0-9]*)?)/g;
    let res1 = txt.match(re);
    if (res1 == null) res1 = [];
    return res1
        .map((s) => {
            s = s.replace(/\s+/g, "");
            s = s.replace(/,/g, "");
            return parseFloat(s);
        })
        .filter((n) => {
            return n != null && Number.isFinite(n);
        });
}

