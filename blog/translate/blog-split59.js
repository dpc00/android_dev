function slow(f) {
    app.ShowProgress();
    f();
    app.HideProgress();
}

