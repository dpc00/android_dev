function dbinstall() {
    try {
        var fe1 = app.FileExists(fn1);
        var fe2 = app.FileExists(fn2);
        if (!fe2) throw new Error("backup db " + fn2 + " not found.");
        if (!fe1 && fe2) {
            app.CopyFile(fn2, fn1);
            fe1 = app.FileExists(fn1);
            if (!fe1) throw new Error("file " + fn2 + " didn't copy");
        } else if (fe1 && fe2) {
            var d1 = app.GetFileDate(fn1);
            var d2 = app.GetFileDate(fn2);
            if (d2 > d1) {
                app.CopyFile(fn2, fn1);
                fe1 = app.FileExists(fn1);
                if (!fe1) throw new Error("file " + fn1 + " didn't copy");
            }
        } else {
            throw new Error("one or more files missing");
        }
    } catch (e) {
        app.Alert(e);
    }
}

