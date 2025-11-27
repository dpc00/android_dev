function loadnums() {
    db.transaction(function (tx) {
        function load(mv) {
            new Promise((resolve, reject) => {
                tx.executeSql(
                    "SELECT num FROM nums WHERE name=?",
                    [mv.name],
                    (t, res) => {
                        resolve(res);
                    },
                    (t, e) => {
                        reject(e);
                    }
                );
            })
                .catch((err) => {
                    alert(err);
                })
                .then((res) => {
                    if (res.rows.length != 1) {
                        alert(mv.name);
                    }
                    mv.num = res.rows.item(0).num;
                    mv.te.SetText(mv.toString());
                });
        }
        load(cashb);
        load(fsb);
        load(dxb);
        load(davg);
        load(dallow);
        load(inec);
        load(dtot);
        load(tleft);
    });
}

