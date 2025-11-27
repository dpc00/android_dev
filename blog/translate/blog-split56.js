function proxynums() {
    cashb = new Proxy(cashb, set_handler);
    fsb = new Proxy(fsb, set_handler);
    dxb = new Proxy(dxb, set_handler);
    davg = new Proxy(davg, set_handler);
    dallow = new Proxy(dallow, set_handler);
    maxdl = new Proxy(maxdl, set_handler);
    let bal_handler = (e) => {
        davg_dtot_calc();
        dallow_calc();
        tleft_calc();
    };
    et.addEventListener(cashb.name + "-changed", bal_handler);
    et.addEventListener(dxb.name + "-changed", bal_handler);
    et.addEventListener(fsb.name + "-changed", bal_handler);
    et.addEventListener("update", bal_handler);
    et.addEventListener(dallow.name + "-changed", (e) => {
        inec_calc();
    });
    et.addEventListener(davg.name + "-changed", (e) => {
        tleft_calc();
        inec_calc();
    });
    et.addEventListener(maxdl.name + "-changed", (e) => {
        dallow_calc();
        inec_calc();
    });
    setInterval(maxdl_calc, 2000);
    bal_handler();
}

