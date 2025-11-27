function d2t(dv) {
    let d = Math.floor(dv);
    let h = Math.floor((dv * 24) % 24);
    let m = Math.round((dv * (24 * 60)) % 60);
    return d + "d," + h + "h," + m + "m";
}

