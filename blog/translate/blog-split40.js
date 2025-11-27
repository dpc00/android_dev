function dl(m, dom) {
    let cd = new Date();
    let nd = new Date();
    let ms = Math.round((dom * (24 * 60 * 60)) % 60);
    let mm = Math.floor((dom * (24 * 60)) % 60);
    let mh = Math.floor((dom * 24) % 24);
    nd.setSeconds(ms);
    nd.setMinutes(mm);
    nd.setHours(mh);
    nd.setDate(Math.floor(dom));
    nd.setMonth(m);
    let em;
    let md = cd.getDate();
    if (cd >= nd) {
        nd.setMonth(nd.getMonth() + 1);
    }
    let t1 = cd.getTime();
    let t2 = nd.getTime();
    let days = (t2 - t1) / 86400000;
    return days;
}

