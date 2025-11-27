function txtp(txt) {
    return txtpa(txt).reduce((a, c) => {
        return a + c;
    }, 0);
}

