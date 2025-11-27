var dirty2 = false;
var dirty3 = false;
var dirty4 = false;
var db = null;
var updated = false;
var b2ot, b3ot;
var tsz = 0.045;
var tesz = 0.066;
var bsz = 0.125;
var losz = 0.075;
var uc = 0;
var uspop = 324459463;
var mtbl_cs =
  "CREATE TABLE monthly (ts TIMESTAMP PRIMARY KEY,cash_recd REAL,fs_recd REAL,dx_recd REAL,cash_spent REAL,fs_spent REAL,dx_spent REAL)";
var dtbl_cs =
  "CREATE TABLE daily (ts TIMESTAMP PRIMARY KEY,cash_recd REAL,fs_recd REAL,dx_recd REAL,cash_spent REAL,fs_spent REAL,dx_spent REAL)";
var ietbl_cs =
  "CREATE TABLE inc_exp (bts TIMESTAMP NOT NULL,ets TIMESTAMP NOT NULL PRIMARY KEY,cash_recd REAL,fs_recd REAL,dx_recd REAL,cash_spent REAL,fs_spent REAL,dx_spent REAL)";
var cashb, fsb, dxb, dtot, davg, dallow, tleft, inec, mindl;
var lts;
var rcb;
var dbfn = "Finance.db";
var fn1 = app.GetPrivateFolder("") + "/../databases";
var fn2 = "/sdcard/projects/blog";
var bal_handler = {
  set: function (obj, prop, val) {
    obj[prop] = val;
    dallow_mindl_calc();
    tleft_calc();
    return true;
  },
};
var davg_handler = {
  set: function (obj, prop, val) {
    obj[prop] = val;
    tleft_calc();
    inec_calc();
    return true;
  },
};
var dallow_handler = {
  set: function (obj, prop, val) {
    obj[prop] = val;
    inec_calc();
    return true;
  },
};
var mindl_handler = {
  set: function (obj, prop, val) {
    obj[prop] = val;
    inec_calc();
    return true;
  },
};
fn1 += dbfn;
fn2 += dbfn;
app.UpdateProgressBar = function (percent, options) {
  prompt("#", "App.UpdateProgressBar(\f" + percent + "\f" + options);
};
if (fn1.length != 0) fn1 += "/";
if (fn2.length != 0) fn2 += "/";
function nc(d) {
  return Math.round(d * 100) / 100;
}
function ncs(d) {
  return nc(d).toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}
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
function txtp(txt) {
  return txtpa(txt).reduce((a, c) => {
    return a + c;
  }, 0);
}
async function sql(stmnt, dat) {
  if (db == null) {
    db = app.OpenDatabase(dbfn);
    db.ExecuteSql("PRAGMA synchronous = OFF");
  }
  return await new Promise((res, err) => {
    db.ExecuteSql(stmnt, dat, res, err);
  }).catch((err) => {
    app.Alert(err + "," + stmnt + "," + dat);
  });
}
async function inec_calc() {
  let res1 = davg.num - dallow.num;
  inec.te.SetText(ncs(res1 * mindl));
}
async function tleft_calc() {
  let tf = cashb.num + dxb.num;
  let tl = tf / davg.num;
  let tmp = ncs(tl);
  tleft.te.SetText(tmp);
}
async function davg_dtot_calc() {
  let res = await sql(
    "SELECT * FROM daily WHERE 'ts' IS NOT NULL ORDER BY 'ts' ASC;"
  );
  let rc = res.rows.length;
  sc = 14;
  bd = new Date(res.rows.item(rc - sc - 1).ts);
  ed = new Date(res.rows.item(rc - 1).ts);
  dd = (ed.getTime() - bd.getTime()) / (1000 * 60 * 60 * 24);
  var te = 0;
  for (i = rc - sc - 1; i < rc; i++) {
    let r = res.rows.item(i);
    te += r.cash_spent;
    te += r.dx_spent;
    if (i == rc - 1) {
      let tmp = ncs(r.cash_spent + r.dx_spent);
      dtot.te.SetText(tmp);
      dtot.lbl.SetText(r.ts);
    }
  }
  let tmp = ncs(te / dd);
  davg.te.SetText(tmp);
}
function d2t(dv) {
  let d = Math.floor(dv);
  let h = Math.floor((dv * 24) % 24);
  let m = Math.round((dv * (24 * 60)) % 60);
  return d + "d," + h + "h," + m + "m";
}
async function dallow_mindl_calc() {
  let cashd = dl(2, 28);
  let dxd = dl(3, 3);
  mindl = Math.min(cashd, dxd);
  let da = cashb.num / cashd + dxb.num / dxd;
  let tmp = ncs(da);
  dallow.te.SetText(tmp);
  app.ShowPopup(d2t(cashd) + " " + d2t(dxd));
}
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
async function tblexists(nm) {
  let res = await sql(
    "SELECT COUNT() AS cnt FROM sqlite_master WHERE type='table' AND name=?",
    [nm]
  );
  return res.rows.item(0).cnt > 0;
}
async function iee() {
  return await tblexists("inc_exp");
}
async function de() {
  return await tblexists("daily");
}
async function me() {
  return await tblexists("monthly");
}
async function mtbl() {
  let mex = await me();
  if (mex && dirty4) {
  } else {
    if (!mex) {
      await sql(mtbl_cs);
      dirty4 = true;
    }
  }
  return mex;
}
async function dtbl() {
  let dex = await de();
  if (dex && dirty3) {
  } else {
    if (!dex) {
      await sql(dtbl_cs);
      dirty3 = true;
    }
  }
  return dex;
}
async function ietbl() {
  let iex = await iee();
  if (iex && dirty2) {
  } else {
    if (!iex) {
      await sql(ietbl_cs);
      dirty2 = true;
    }
  }
  return iex;
}
async function lts() {
  let res = await sql("SELECT ts FROM currentc ORDER BY ts DESC");
  return res.rows.item(uc).ts;
}
async function update_ietbl() {
  app.ShowProgressBar("updating tables...");
  let pd = await lts();
  let iex = await ietbl();
  let wh = "";
  if (iex && !rcb.GetChecked()) {
    wh = " WHERE ts>='" + pd + "'";
  }
  if (dirty2 || rcb.GetChecked()) {
    let ss = "SELECT ts, cash, fs, dx FROM currentc" + wh + " ORDER BY ts";
    let res = await sql(ss);
    let rc = res.rows.length;
    let j = 0;
    let i = 1;
    db.transaction(async function (tx) {
      for (; i < rc; i++) {
        let pr = res.rows.item(j);
        let cr = res.rows.item(i);
        let bts = pr.ts;
        let ets = cr.ts;
        let cash_diff = nc(cr.cash - pr.cash);
        let fs_diff = nc(cr.fs - pr.fs);
        let dx_diff = nc(cr.dx - pr.dx);
        let cash_recd = cash_diff > 0 ? cash_diff : null;
        let fs_recd = fs_diff > 0 ? fs_diff : null;
        let dx_recd = dx_diff > 0 ? dx_diff : null;
        let cash_spent = cash_diff < 0 ? nc(-cash_diff) : null;
        let fs_spent = fs_diff < 0 ? nc(-fs_diff) : null;
        let dx_spent = dx_diff < 0 ? nc(-dx_diff) : null;
        if (cash_diff != 0 || fs_diff != 0 || dx_diff != 0) {
          let res2 = await tx.executeSql(
            "INSERT OR REPLACE INTO inc_exp (bts, ets, cash_recd, fs_recd, dx_recd, cash_spent, fs_spent, dx_spent) VALUES (?,?,?,?,?,?,?,?)",
            [
              bts,
              ets,
              cash_recd,
              fs_recd,
              dx_recd,
              cash_spent,
              fs_spent,
              dx_spent,
            ]
          );
          j = i;
          dirty3 = true;
        }
        uc--;
        app.UpdateProgressBar((i * 80) / rc);
      }
    });
    dirty2 = false;
  }
  app.UpdateProgressBar(80);
  let dex = await dtbl();
  wh = "";
  if (dex && !rcb.GetChecked()) {
    wh =
      " WHERE substr(datetime(ets,'localtime'), 1, 10)>='" +
      new Date(pd).toLocaleDateString("fr-CA").substring(0, 10) +
      "'";
    app.ShowPopup(wh);
  }
  if (dirty3 || rcb.GetChecked()) {
    let sst =
      " SELECT substr(datetime(ets,'localtime'), 1, 10) AS ts, SUM(cash_recd) AS cash_recd, SUM(fs_recd) AS fs_recd, SUM(dx_recd) AS dx_recd, SUM(cash_spent) AS cash_spent, SUM(fs_spent) AS fs_spent, SUM(dx_spent) AS dx_spent FROM inc_exp" +
      wh +
      " GROUP BY substr(datetime(ets,'localtime'), 1, 10)";
    await sql("INSERT OR REPLACE INTO daily" + sst);
    dirty3 = false;
    dirty4 = true;
  }
  app.UpdateProgressBar(90);
  let mex = await mtbl();
  wh = "";
  if (mex && !rcb.GetChecked()) {
    wh =
      " WHERE substr(datetime(ets,'localtime'), 1, 7)>='" +
      new Date(pd).toLocaleDateString("fr-CA").substring(0, 7) +
      "'";
  }
  if (dirty4 || rcb.GetChecked()) {
    let sst =
      " SELECT substr(datetime(ets,'localtime'), 1, 7) AS ts, SUM(cash_recd) AS cash_recd, SUM(fs_recd) AS fs_recd, SUM(dx_recd) AS dx_recd, SUM(cash_spent) AS cash_spent, SUM(fs_spent) AS fs_spent, SUM(dx_spent) AS dx_spent FROM inc_exp" +
      wh +
      " GROUP BY substr(datetime(ets,'localtime'), 1, 7)";
    await sql("INSERT OR REPLACE INTO monthly" + sst);
    dirty4 = false;
  }
  app.UpdateProgressBar(100);
  app.HideProgressBar();
  if (rcb.GetChecked()) {
    uc = 0;
    rcb.SetChecked(false);
  }
}
async function log_balances() {
  await sql("INSERT INTO currentc (ts, cash, fs, dx) VALUES (?,?,?,?)", [
    new Date().toISOString(),
    cashb.num,
    fsb.num,
    dxb.num,
  ]);
  dirty2 = true;
  uc++;
}
async function SaveNumber(name, num) {
  await sql("UPDATE nums SET (num,ts)=(?,?) WHERE name=?", [
    num,
    new Date().toISOString(),
    name,
  ]);
}
async function loadnums() {
  db.transaction(function (tx) {
    async function load(mv) {
      await new Promise((resolve, reject) => {
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
function teot() {
  let v = this.mvar;
  app.ShowPopup(" v.name: " + v.name);
}
function sc(o) {
  try {
    o.SetBackColor("white");
  } catch (e) {}
  try {
    o.SetTextColor("black");
  } catch (e) {}
}
async function slow(f) {
  app.ShowProgress();
  await f();
  app.HideProgress();
}
function proxynums() {
  cashb = new Proxy(cashb, bal_handler);
  fsb = new Proxy(fsb, bal_handler);
  dxb = new Proxy(dxb, bal_handler);
  davg = new Proxy(davg, davg_handler);
  dallow = new Proxy(dallow, dallow_handler);
  mindl = new Proxy(mindl, mindl_handler);
}
async function OnStart() {
  db = app.OpenDatabase(dbfn);
  cashb = new Mvar("Cash", "");
  fsb = new Mvar("FS", "");
  dxb = new Mvar("DX", "");
  cashb.isbal = true;
  fsb.isbal = true;
  dxb.isbal = true;
  davg = new Mvar("DAvgExp", "readonly,nokeyboard");
  davg.te.SetTextColor("turquoise");
  dallow = new Mvar("DAllow", "readonly,nokeyboard");
  dallow.te.SetTextColor("fuchsia");
  inec = new Mvar("INec", "readonly,nokeyboard");
  inec.te.SetTextColor("green");
  dtot = new Mvar("DTotExp", "readonly,nokeyboard");
  dtot.te.SetTextColor("blue");
  tleft = new Mvar("TLeft", "readonly,nokeyboard");
  tleft.te.SetTextColor("red");
  mindl = new Mvar("MinDL", "readonly,nokeyboard");
  proxynums();
  loadnums();
  // davg_dtot_calc();
  let b1 = app.CreateButton("Update", 0.5, bsz);
  b1.SetOnTouch(async () => {
    await slow(async () => {
      await cashb.save();
      await fsb.save();
      await dxb.save();
      await update_ietbl();
    });
    await b3ot();
  });
  let b3 = app.CreateButton("Recalc", 0.5, bsz);
  b3ot = async () => {
    await davg_dtot_calc();
    await dallow_mindl_calc();
    await tleft_calc();
    await inec_calc();
    await davg.save();
    await dallow.save();
    await inec.save();
    await dtot.save();
    await tleft.save();
  };
  b3.SetOnTouch(b3ot);
  let b2 = app.CreateButton("Exit", 0.5, bsz);
  b2ot = async () => {
    if (db != null) {
      db.Close();
      db = null;
    }
    app.Exit();
  };
  b2.SetOnTouch(b2ot);
  window.onclose = b2ot;
  rcb = app.CreateCheckBox("Regen i/e tables");
  sc(rcb);
  let ttl1 = app.CreateText("Balance Log");
  ttl1.SetTextSize(26);
  let lyo1 = app.CreateLayout("linear", "vertical, center");
  lyo1.AddChild(cashb.lo);
  lyo1.AddChild(dxb.lo);
  lyo1.AddChild(fsb.lo);
  sc(lyo1);
  let lyo2 = app.CreateLayout("linear", "vertical,center");
  function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
  }
  los = [dallow.lo, inec.lo, tleft.lo, davg.lo, dtot.lo];
  shuffleArray(los);
  for (var i = 0; i < los.length; i++) {
    lyo2.AddChild(los[i]);
  }
  sc(lyo2);
  let lyo0 = app.CreateLayout("linear", "vertical, center");
  lyo0.AddChild(ttl1);
  lyo0.AddChild(lyo1);
  lyo0.AddChild(lyo2);
  lyo0.AddChild(b1);
  lyo0.AddChild(b3);
  lyo0.AddChild(b2);
  lyo0.AddChild(rcb);
  sc(lyo0);
  lyo0.SetSize(1, 1);
  app.AddLayout(lyo0);
}
async function ib() {
  let ft = app.ReadFile(app.GetPath() + "/blog2.csv");
  let lna = ft.split("\n");
  for (i = 0; i < lna.length; i++) {
    let f = lna[i].split(",");
    let tp = f[1].split(":");
    if (Number(tp[0]) < 10) tp[0] = "0" + Number(tp[0]);
    f[1] = tp.join(":");
    let ts = f[0] + " " + f[1];
    let res = await sql(
      "INSERT INTO currentc (ts, cash, fs, dx) VALUES (?,?,?,?)",
      [new Date(ts).toISOString(), f[2], f[3], f[4]]
    );
  }
  app.Exit();
}
async function fixtbl() {
  let sqlt1 =
    "CREATE TABLE IF NOT EXISTS tmpc (ts TIMESTAMP PRIMARY KEY NOT NULL,cash REAL,fs REAL,dx REAL)";
  await sql(sqlt1);
  await sql("DELETE FROM tmpc");
  let res = await sql("select * from currentc order by ts");
  for (let i = 0; i < res.rows.length; i++) {
    let row = res.rows.item(i);
    await sql("insert into tmpc (ts,cash,fs,dx) values (?,?,?,?)", [
      new Date(row.ts).toISOString(),
      row.cash,
      row.fs,
      row.dx,
    ]);
  }
  app.Exit();
}
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
class Mvar {
  constructor(n, ne) {
    this.num = 0;
    this.te = app.CreateTextEdit(
      "",
      0.5,
      tesz,
      "singleline" + (ne !== "" ? "," + ne : "")
    );
    this.name = n;
    this.te.SetHint(n);
    this.te.mvar = this;
    this.lbl = app.CreateText(this.name, 0.325, tsz, "right");
    this.lo = app.CreateLayout("linear", "horizontal");
    this.lo.AddChild(this.lbl);
    this.lo.AddChild(this.te);
    this.lo.SetSize(0.8, tesz);
    this.cf = async function () {
      let res2, res3;
      let res1 = this.GetText();
      res2 = txtpa(res1);
      res3 = res2.reduce((a, c) => {
        return a + c;
      }, 0);
      if (res2.length == 0) {
      }
      app.ShowPopup(this.mvar.name + ": " + res1 + " = " + ncs(res3));
    };
    this.te.SetOnTouch(this.cf);
    this.te.SetOnChange(this.cf);
    sc(this.te);
    sc(this.lbl);
    sc(this.lo);
  }
  async save() {
    let txt = this.te.GetText();
    let ia = txtpa(txt);
    let acc = 0;
    for (let ci of ia) {
      acc = nc(acc + ci);
      await this.newbal(acc);
    }
    this.te.SetText(this.toString());
  }
  async newbal(nb) {
    if (this.num !== nb) {
      this.num = nb;
      await this.te.SetText(this.toString());
      await SaveNumber(this.name, this.num);
      if (this.isbal) await log_balances();
    }
  }
  toString() {
    return ncs(this.num);
  }
}
