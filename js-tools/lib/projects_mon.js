/// <ref path="typings/main/jake/index.d.ts"/>

var cf = require("copy_flash");
var ch = require("chokidar");
var dirutils = require("dirutils");
var diskutils = require("diskutils");
var fcs = require("fcstats");
var fs = require("fs");
var path = require("path");
var utils = require("utils");

var copying = false;
var pd = utils.expES("%FLASH0%\\");

var rdy = false;
var rfc3 = true;
var starttime = Date.now();

var wdirs = [
  // pd + 'Node\\node_modules',
  pd + ".bat",
  pd + ".jedit",
  pd + "GitRepos",
  pd + "Programs\\DirSyncPro-1.51",
  pd + "Programs\\GoogleChromePortable",
  pd + "Programs\\jEdit 5.3.0",
  pd + "Programs\\RocketDockPortable",
  pd + "Programs\\SublimeText",
  pd + "Programs\\Unison-2.40.102\\.unison",
  pd + "Programs\\VSCode\\.vscode",
  pd + "Programs\\WinDirStatPortable\\Data\\settings",
  pd + "Projects",
];

function secs() {
  var curtime = Date.now();
  return (curtime - starttime) / 1000.0;
}

var watcher = ch.watch(wdirs[0], {
  persistent: false,
  ignored: [/clog_flash_CODE0.json/, /.lock/],
  cwd: null,
});

wdirs.slice(1).forEach(function (wd) {
  watcher.add(wd);
});

watcher.on("all", function (ev, fp1, stats) {
  if (rdy) utils.log(secs(), ev, utils.chop(fp1));
  if (fp1.endsWith(".lock")) return;
  var fp2 = path.dirname(fp1);
  var fp3 = fp2.replace(process.env.FLASH0, "%FLASH0%");
  log(fp3);
});

watcher.on("ready", function () {
  preMess();
  rdy = true;
});

watcher.on("error", function (ev) {
  utils.log(secs(), ev);
});

setInterval(f0, 1000);

var secs2 = 0;

function f0() {
  if (!copying) {
    secs2++;
    if (secs2 >= 4) {
      setTimeout(f1, 0);
      secs2 = 0;
    }
  } else secs2 = 0;
}

function f1() {
  var b1 = rfc3;
  var b2 = chkLog();
  var b3 = !copying;
  if (b1 && b2 && b3) {
    copying = true;
    setImmediate(f2);
  }
}

var dirs = {};

var statsinited = false;

function initStats() {
  if (!statsinited) {
    var psf = setInterval(fcs.print, 1000);
    psf.unref();

    fcs.clr();
    cf.addDMListeners();
    statsinited = true;
  }
}

function f2() {
  var sda = cf.establish();

  initStats();

  var p1 = Promise.resolve();

  var tdirs = Object.assign({}, dirs);

  for (var k in tdirs) {
    delete dirs[k];
  }

  Object.keys(tdirs).forEach(function (k) {
    var sfp = utils.expES(k);
    var dfp = dirutils.dPath(sda[0], sda[1], sfp);
    var k2 = k;
    p1 = p1.then(function () {
      return dirutils.dirSync(sfp, dfp).then(function () {
        utils.writedata("\r\n");
      });
    });
  });
  return p1.then(function () {
    // cf.removeDMListeners();
    // clearInterval(psf);
    copying = false;
  });
}

function chkLog() {
  return Object.keys(dirs).length > 0;
}

function log(gp) {
  if (typeof dirs[gp] == "undefined") {
    dirs[gp] = true;
  }
}

function pause() {
  utils.writedata("press any key...");
  var buf = process.stdin.read(1);
  return Promise.resolve();
}

function preMess() {
  var n = (function () {
    var w = watcher.getWatched();
    var i = 0;
    for (var k in w) {
      i++;
    }
    return i;
  })();
  utils.log(n + " dirs.");
  utils.log(secs() + " sec to ready.");
}
