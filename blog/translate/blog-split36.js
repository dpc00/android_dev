function dbbackup() {
    try {
        var fe1 = app.FileExists(fn1);
        var fe2 = app.FileExists(fn2);
        if (fe1 && !fe2) {
            app.CopyFile(fn1, fn2);
            var fe2 = app.FileExists(fn2);
            if (!fe2) throw new Error("file " + fn2 + " didn't arrive");
        } else if (fe1 && fe2) {
            var d1 = app.GetFileDate(fn1);
            var d2 = app.GetFileDate(fn2);
            if (d1 > d2) {
                app.CopyFile(fn1, fn2);
                var fe2 = app.FileExists(fn2);
                if (!fe2) throw new Error("file " + fn2 + " is now missing");
                d2 = app.GetFileDate(fn2);
                if (d1 > d2) throw new Errorr("file " + fn2 + " didn't copy");
            }
        }
    } catch (e) {
        app.Alert(e);
    }
}

