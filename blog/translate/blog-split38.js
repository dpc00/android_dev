function dbps() {
    var fn1 = app.GetPrivateFolder("") + "/../databases";
    if (fn1.length != 0) fn1 += "/";
    fn1 += dbfn;
    var fn2 = "/sdcard/projects/blog";
    if (fn2.length != 0) fn2 += "/";
    fn2 += dbfn;
}

