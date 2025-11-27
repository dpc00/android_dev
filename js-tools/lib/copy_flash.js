/// <ref path="typings/main.d.ts"/>

var dirutils = require("dirutils");
var Dos4 = require("dos4");
var fcs = require("fcstats");
var fs = require("fs");
var json = require("json");
var path = require("path");
var util = require("util");
var utils = require("utils");

var clog = {};
var cfn = utils.expES("%FLASH0%\\Projects\\tools\\clog_flash_CODE0.json");

function setEnv(k, v) {
  var cfn = utils.expES("%FLASH0%\\Projects\\tools\\plaunch_flash_CODE0.json");
  var splobj = json.readConfig(cfn);
  splobj.env[k] = v;
  process.env[k] = v;
  json.writePlaunchJSON(splobj, cfn);
}
module.exports.setEnv = setEnv;

function makename1(n) {
  function ascii(s) {
    return s.charCodeAt(0);
  }

  function chr(m) {
    return String.fromCharCode(m);
  }
  var s = "";
  for (var i = 0; i < n; i++) {
    s += chr(ascii("A") + Math.floor(Math.random() * 26));
  }
  return s;
}
module.exports.makename1 = makename1;

function makename2() {
  var d = new Date();
  return "CODE\\" + d.getDay();
}
module.exports.makename2 = makename2;

function establish() {
  if (
    typeof process.env.FLASH0 == "undefined" ||
    typeof process.env.FLASH1 == "undefined"
  )
    return;
  var src = utils.expES("%FLASH0%\\");
  var dest;
  if (process.env.CLONE_DIR) dest = utils.expES(process.env.CLONE_DIR);
  else {
    dest = utils.expES("%FLASH1%\\" + makename1(8));
    var ev = dest.replace(process.env.FLASH1, "%FLASH1%");
    setEnv("CLONE_DIR", ev);
    var cplb = require("cpl_bat");
    cplb.run();
  }
  return [src, dest];
}
module.exports.establish = establish;

function fixedD(num, len) {
  var s = num.toString();
  if (s.length < len) {
    for (; s.length < len; ) s = " " + s;
  }
  return s;
}

function getClog() {
  clog = json.readConfig(cfn);
}

function writeClog() {
  try {
    json.writeConfig(clog, cfn);
  } catch (e) {
    utils.log(e.message);
  } finally {
    var cbf = setTimeout(writeClog, 30000);
    cbf.unref();
  }
}

function addDMListeners() {
  var ee = dirutils.dmEE1;
  ee.on("dcopy", function (p1, p2) {
    fcs.print();
  });
  ee.on("ddel", function (p2) {
    var v = p2.replace(process.env.CLONE_DIR, "%FLASH0%");
    if (typeof clog[v] != "undefined") delete clog[v];
    v = path.dirname(v);
    if (v.endsWith("%FLASH0%")) v += "\\";
    if (typeof clog[v] == "undefined") clog[v] = 0;
    clog[v]++;
    fcs.print();
  });
  ee.on("dskipped", function (p1) {
    fcs.print();
  });
  ee.on("error", function (err) {
    utils.log(err.message);
    fcs.print();
  });
  ee.on("fcopy", function (p1, p2) {
    var v = p1.replace(process.env.FLASH0, "%FLASH0%");
    v = path.dirname(v);
    if (v.endsWith("%FLASH0%")) v += "\\";
    if (typeof clog[v] == "undefined") clog[v] = 0;
    clog[v]++;
    fcs.print();
  });
  ee.on("fdel", function (p2) {
    var v = p2.replace(process.env.CLONE_DIR, "%FLASH0%");
    v = path.dirname(v);
    if (v.endsWith("%FLASH0%")) v += "\\";
    if (typeof clog[v] == "undefined") clog[v] = 0;
    clog[v]++;
    fcs.print();
  });
}
module.exports.addDMListeners = addDMListeners;

function removeDMListeners() {
  var ee = dirutils.dmEE1;
  ee.removeAllListeners();
}
module.exports.removeDMListeners = removeDMListeners;

function dirCopy(d1, d2) {
  getClog();
  fcs.clr();
  addDMListeners();
  return dirutils.dirCopy(d1, d2, []).then(function () {
    removeDMListeners();
    fcs.print();
    json.writeConfig(clog, cfn);
  });
}
module.exports.dirCopy = dirCopy;

function flashSync1(d1, d2) {
  dirutils.dm_excl = {};
  getClog();
  var cbf = setTimeout(writeClog, 10000);
  cbf.unref();
  var psf = setInterval(fcs.print, 1000);
  psf.unref();
  fcs.clr();
  addDMListeners();
  return dirutils.dirMirror(d1, d2).then(function () {
    removeDMListeners();
    clearTimeout(cbf);
    clearInterval(psf);
    json.writeConfig(clog, cfn);
  });
}
module.exports.flashSync1 = flashSync1;

function flashSync2(d1, d2) {
  dirutils.dm_excl = {};
  getClog();
  var cbf = setTimeout(writeClog, 10000);
  cbf.unref();
  var psf = setInterval(fcs.print, 1000);
  psf.unref();
  fcs.clr();
  addDMListeners();

  var tclog = Object.assign({}, clog);

  var p1 = Promise.resolve();

  for (k in tclog) {
    (function (kt) {
      var cp = utils.expES(kt);
      var sfp = cp;
      var dfp = dirutils.dPath(d1, d2, sfp);
      p1 = p1.then(function () {
        return dirutils.dirSync(sfp, dfp);
      });
    })(k);
  }
  return p1.then(function () {
    removeDMListeners();
    clearTimeout(cbf);
    clearInterval(psf);
    json.writeConfig(clog, cfn);
  });
}
module.exports.flashSync2 = flashSync2;

function fcopy1() {
  var sda = establish();
  var src = sda[0];
  var dest = sda[1];
  return flashSync1(src, dest);
}
module.exports.fcopy1 = fcopy1;

function fcopy2() {
  var sda = establish();
  var src = sda[0];
  var dest = sda[1];
  return flashSync2(src, dest);
}
module.exports.fcopy2 = fcopy2;

function fcopy3() {
  var sda = establish();
  var src = sda[0] + "\\Programs\\GoogleChromePortable";
  var dest = sda[1] + "\\Programs\\GoogleChromePortable";
  return flashSync1(src, dest);
}
module.exports.fcopy3 = fcopy3;

var xml2js = require("xml2js");

function dsPro() {
  var sda = establish();
  var src = sda[0];
  var dst = sda[1];

  var dspd = utils.expES("%FLASH0%\\Programs\\DirSyncPro-1.51");

  var dscfn1 = dspd + "\\CODE0-CODE1.dsc";
  var dscfn2 = utils.prjDir("tools") + "\\CODE0-CODE1.dsc";

  var dspe = dspd + "\\DirSyncPro.exe";
  var lfn = dspd + "\\FullFlashBackup.log";

  var bfn = utils.expES("%FLASH0%\\dspro.bat");
  var cmd1 = "call \\plaunch jake.cmd flash-backup:dirsyncpro\r\n";
  var cmd2 =
    "call \\plaunch DirSyncPro.exe " +
    dscfn2.replace(process.env.FLASH0, "%FLASH0%") +
    "\r\n";

  var kcdsc_xml = fs.readFileSync(dscfn1, "ascii");
  if (!kcdsc_xml) return Promise.reject();
  return new Promise(function (resolve, reject) {
    new xml2js.Parser().parseString(kcdsc_xml, function (err, result) {
      if (err) reject(err);
      else resolve(result);
    });
  })
    .then(function (kcdsc_js) {
      kcdsc_js.dirsyncpro.job[0].$.src = src;
      kcdsc_js.dirsyncpro.job[0].$.dst = dst;
      kcdsc_js.dirsyncpro.job[0].$.logfile = lfn;
      // kcdsc_js.dirsyncpro.job[0].$.realtimeSync = "true";
      // kcdsc_js.dirsyncpro.job[0].$.realtimeSyncOnStart = "true";
      var kcdsc_xml = new xml2js.Builder().buildObject(kcdsc_js);
      fs.writeFileSync(dscfn2, kcdsc_xml, {
        encoding: "ascii",
      });
      fs.writeFileSync(bfn, cmd1 + cmd2, {
        encoding: "ascii",
      });
    })
    .catch(function (reason) {
      console.dir(reason);
    });
}
module.exports.dsPro = dsPro;

function sublimeText() {
  var sda = establish();
  var src = sda[0];
  var dst = sda[1];

  var std = utils.expES("%FLASH0%\\Programs\\SublimeText");

  var spfn1 = utils.prjDir("") + "\\tools.sublime-project";

  var bfn = utils.expES("%FLASH0%\\.bat\\sublimetext.bat");
  var cmd1 = "call \\plaunch jake.cmd sublimetext\r\n";
  var cmd2 =
    "call \\plaunch subl.exe --project " +
    spfn1.replace(process.env.FLASH0, "%FLASH0%") +
    "\r\n";

  var sp_json = json.readConfig(spfn1);
  sp_json.folders = [];
  utils.prjList.forEach(function (pn, i) {
    sp_json.folders[i] = {
      path: utils.prjDir(pn),
    };
  });
  json.writeConfig(sp_json, spfn1);

  fs.writeFileSync(bfn, cmd1 + cmd2, {
    encoding: "ascii",
  });
}
module.exports.sublimeText = sublimeText;

/*
var std = utils.expES('%FLASH0%\\Programs\\SublimeText');
console.log(std);
*/
