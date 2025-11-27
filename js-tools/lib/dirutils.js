var diskutils = require("diskutils");
var Dos4 = require("dos4");
var EventEmitter = require("events");
var fcs = require("fcstats");
var fs = require("fs");
var path = require("path");
var util = require("util");
var utils = require("utils");

/* copyFile
	var fc = copyFile('\\all.bat', 'all.bat');
	fc.then(function(err) {
		if(err) utils.log(err.message);
 		else utils.log('file copied.');
	});
*/

var ev = require("events");

var dmEE1 = new EventEmitter();
module.exports.dmEE1 = dmEE1;

var dm_excl = {};

module.exports.dm_excl = dm_excl;

function dirsContainingType(sp, exs, norecurse, exc_dirs) {
  var bfp = [];

  function adde(dp1, fl1) {
    var fnl1 = fl1.map(function (fd1) {
      return path.basename(fd1.fp);
    });
    bfp.push({
      path: dp1,
      include: false,
      files: fnl1,
    });
  }

  function dwf(dp2) {
    var p1 = diskutils.filesList(dp2, exs);
    var p2 = p1.then(function (fl) {
      if (fl.length > 0) {
        adde(dp2, fl);
      }
      showprogress();
    });
    return p2;
  }
  var p1 = dirTreeWalk(sp, dwf, norecurse, exc_dirs);
  p1 = p1.then(function () {
    return bfp;
  });
  return p1;
}
module.exports.dirsContainingType = dirsContainingType;

var dmdel = true;

function delDir(d2) {
  var p1 = diskutils.filesList(d2);
  var p2 = diskutils.dirsList(d2);
  return Promise.all([p1, p2]).then(function (ra) {
    var d2fl = ra[0];
    var d2dl = ra[1];
    var p3 = Promise.resolve();
    d2fl.forEach(function (d2fld) {
      p3 = p3.then(function () {
        return diskutils.delFile(d2fld.fp).then(function () {
          dmEE1.emit("fdel", d2fld.fp);
        });
      });
    });
    d2dl.forEach(function (d2dld) {
      p3 = p3.then(function () {
        return delDir(d2dld.dp);
      });
    });
    return p3.then(function () {
      return diskutils.rmDir(d2).then(function () {
        dmEE1.emit("ddel", d2);
      });
    });
  });
}
module.exports.delDir = delDir;

function llookup(l, fd) {
  for (var i = 0; i < l.length; i++) {
    if (path.basename(fd.fp) == path.basename(l[i].fp)) return l[i];
  }
  return null;
}

function llookup2(l, fd) {
  for (var i = 0; i < l.length; i++) {
    if (path.basename(fd.dp) == path.basename(l[i].dp)) return l[i];
  }
  return null;
}

function delDirs(d1, d2) {
  var p1 = diskutils.dirsList(d1);
  var p2 = diskutils.dirsList(d2);
  return Promise.all([p1, p2]).then(function (rva) {
    var d1dl = rva[0];
    var d2dl = rva[1];
    var toDelete = d2dl.filter(
      // not in source
      function (cdd) {
        var ddd = llookup2(d1dl, cdd);
        return !ddd;
      }
    );
    var p3 = Promise.resolve();
    toDelete.forEach(function (cdd) {
      p3 = p3.then(function () {
        return delDir(cdd.dp);
      });
    });
    return p3;
  });
}
module.exports.delDirs = delDirs;

function delFiles(d1, d2, exs) {
  var p1 = diskutils.filesList(d1, exs);
  var p2 = diskutils.filesList(d2, exs);
  return Promise.all([p1, p2]).then(function (rva) {
    var d1fl = rva[0];
    var d2fl = rva[1];
    var toDelete = d2fl.filter(function (d2fld) {
      var dfd = llookup(d1fl, d2fld);
      return !dfd;
    });
    var p3 = Promise.resolve();
    toDelete.forEach(function (d2fld) {
      p3 = p3.then(function () {
        return diskutils.delFile(d2fld.fp).then(function () {
          dmEE1.emit("fdel", d2fld.fp);
        });
      });
    });
    return p3;
  });
}
module.exports.delFiles = delFiles;

function dPath(d1, d2, p) {
  var r1 = path.relative(d1, p);
  var r2 = path.join(d2, r1);
  return r2;
}
module.exports.dPath = dPath;

// var Sse4Crc32 = require("sse4_crc32");

function fCompare(s, t) {
  return new Promise(function (resolve, reject) {
    var s1 = fs.createReadStream(s.fp);
    var s2 = fs.createReadStream(t.fp);
    s1.on("error", function (err) {
      reject(err);
    });
    s2.on("error", function (err) {
      reject(err);
    });

    var r1, r2;

    s1.on("readable", function () {
      r1 = true;
      if (r2) cfunc();
    });
    s2.on("readable", function () {
      r2 = true;
      if (r1) cfunc();
    });

    function cfunc() {
      var chunk1 = s1.read();
      var chunk2 = s2.read();
      while (chunk1 && chunk2) {
        if (chunk1.length != chunk2.length) {
          s1.close();
          s2.close();
          reject();
          return;
        } else {
          for (var i = 0; i < chunk1.length; i++) {
            var rv = chunk2[i] - chunk1[i];
            if (rv != 0) {
              s1.close();
              s2.close();
              reject();
              return;
            }
          }
        }
        chunk1 = s1.read();
        chunk2 = s2.read();
      }
      s1.close();
      s2.close();
      resolve();
    }
  });
}

var copycrit = [
  function (s, t) {
    // 1
    if (t == null || typeof t == "undefined") return Promise.reject();
    else return Promise.resolve();
  },
  function (s, t) {
    // 2
    // if (t == null || typeof t == 'undefined')
    // 	return Promise.reject();
    // else {
    if (t.mtime.getTime() < s.mtime.getTime()) return Promise.reject();
    else return Promise.resolve();
    // }
  },
  function (s, t) {
    // 4
    // if (t == null || typeof t == 'undefined')
    // 	return Promise.reject();
    // else {
    if (t.mtime.getTime() !== s.mtime.getTime()) return Promise.reject();
    else return Promise.resolve();
    // }
  },
  function (s, t) {
    // 8
    // if (t == null || typeof t == 'undefined')
    // 	return Promise.reject();
    // else {
    if (t.size !== s.size) return Promise.reject();
    else return Promise.resolve();
    // }
  },
  function (s, t) {
    // 16
    // if (t == null || typeof t == 'undefined')
    // 	return Promise.reject();
    // else {
    utils.log(utils.chop("dc: " + s.fp + " - " + t.fp));
    return fCompare(s, t);
    // }
  },
];

var ccrit = 1 | 2;
module.exports.ccrit = ccrit;

function copyFiles(d1, d2, exs, ccrit) {
  var p1 = diskutils.filesList(d1, exs);
  var p2 = diskutils.filesList(d2, exs);
  var fc = 0;
  return Promise.all([p1, p2]).then(function (rva) {
    var d1fl = rva[0];
    var d2fl = rva[1];
    var p3 = Promise.resolve();
    d1fl.forEach(function (d1fld) {
      var d2fld = llookup(d2fl, d1fld);
      var p4 = Promise.resolve();
      for (var k = 0; k < copycrit.length; k++) {
        var bit = 1 << k;
        if (ccrit & bit) {
          var k2 = k;
          p4 = p4.then(function () {
            var k3 = k2;
            return copycrit[k3](d1fld, d2fld);
          });
        }
      }
      p4 = p4.catch(function () {
        var sfp = d1fld.fp;
        var dfp = dPath(d1, d2, sfp);
        return diskutils.copyFile(sfp, dfp).then(function () {
          dmEE1.emit("fcopy", sfp, dfp);
          fc++;
        });
      });
      p3 = p3.then(function () {
        return p4;
      });
    });
    return p3;
  });
}
module.exports.copyFiles = copyFiles;

function mirrorDirs(d1, d2) {
  var p1 = diskutils.dirsList(d1);
  var p2 = diskutils.dirsList(d2);
  return Promise.all([p1, p2]).then(function (rva) {
    var d1dl = rva[0];
    var d2dl = rva[1];
    var p3 = Promise.resolve();
    var toCopy = d1dl;
    toCopy.forEach(function (d1dld) {
      var sdp = d1dld.dp;
      var ddp = dPath(d1, d2, sdp);
      p3 = p3.then(function () {
        return dirMirror(sdp, ddp);
      });
    });
    return p3;
  });
}
module.exports.mirrorDirs = mirrorDirs;

function dirCopy(d1, d2, exs) {
  fcs.clr();
  return diskutils.dirExists(d2).then(function (de) {
    if (!de) mkDirs(d2);
    return copyFiles(d1, d2, exs, 1 | 2).then(function () {
      fcs.fcstats.dcpy++;
      dmEE1.emit("dcopy", d1, d2);
    });
  });
}
module.exports.dirCopy = dirCopy;

function dirSync(d1, d2, exs) {
  // if (dm_excl[d1]) {
  // 	dmEE1.emit('dskipped', d1);
  // 	return;
  // }
  // dm_excl[d1] = true;

  return diskutils.dirExists(d2).then(function (de) {
    if (!de) mkDirs(d2);
    utils.log(utils.chop("ds: " + d1 + " starting..."));
    var p1 = copyFiles(d1, d2, exs, 1 | 2 | 4 | 8);
    var p2 = delFiles(d1, d2);
    return Promise.all([p1, p2]).then(function () {
      fcs.fcstats.dcpy++;
      dmEE1.emit("dcopy", d1, d2);
      utils.log(utils.chop("ds: " + d1 + " done."));
    });
  });
}
module.exports.dirSync = dirSync;

function dirMirror(d1, d2) {
  if (dm_excl[d1]) {
    dmEE1.emit("dskipped", d1);
    return;
  }
  dm_excl[d1] = true;

  return diskutils.dirExists(d2).then(function (de) {
    if (!de) mkDirs(d2);
    utils.log(utils.chop("dm: " + d1 + " starting..."));
    var p1 = dirSync(d1, d2, []);
    var p2 = delDirs(d1, d2);
    var p3 = mirrorDirs(d1, d2);
    return Promise.all([p1, p2, p3]).then(function () {
      utils.log(utils.chop("dm: " + d1 + " done."));
    });
  });
}
module.exports.dirMirror = dirMirror;

function touchBats() {
  var exe;

  function setExe() {
    var ps = utils.expES("%FLASH0%\\Programs\\Git\\usr\\bin");
    exe = ps + "\\touch.exe";
    return true;
  }

  if (setExe()) {
    return diskutils
      .filesList(utils.expES("%FLASH0%\\"), [".bat"])
      .then(function (fl) {
        fl = fl.map(function (f) {
          return f.fp;
        });
        return new Dos4({
          cmd: exe,
          args: fl,
          collect: false,
          echo: true,
          print: true,
        });
      });
  } else return Promise.resolve();
}
module.exports.touchBats = touchBats;

var dcnt = 0;

function showprogress() {
  utils.writedata("\r\n" + ++dcnt + " dirs");
}
module.exports.showprogress = showprogress;

function dirTreeWalk(pth, fn, norecurse, exc_dirs) {
  var p3 = Promise.resolve();

  var pth2 = dirMatchCase(pth);
  if (pth !== pth2) utils.log("case conflict:" + pth + " changed to " + pth2);

  function not_exc(pth3) {
    return (
      exc_dirs.filter(function (e) {
        var b1 = pth3.length >= e.length;
        var b2 =
          pth3
            .substring(0, e.length)
            .toLowerCase()
            .localeCompare(e.toLowerCase()) === 0;
        return b1 && b2;
      }).length === 0
    );
  }

  if (!exc_dirs || not_exc(pth2)) {
    if (!norecurse) {
      p3 = p3.then(function () {
        return diskutils.dirsList(pth2).then(function (dirs) {
          var p4 = Promise.resolve();
          dirs.forEach(function (dir) {
            p4 = p4.then(function () {
              return dirTreeWalk(dir.dp, fn, norecurse, exc_dirs);
            });
          });
          return p4;
        });
      });
    }
    p3 = p3.then(function () {
      return fn(pth2);
    });
  }
  return p3;
}
module.exports.dirTreeWalk = dirTreeWalk;

function dirMatchCase(p) {
  var pd = path.dirname(p);
  if (pd !== p) {
    try {
      var v1 = path.basename(p).toLocaleLowerCase();
      var fdd = fs.readdirSync(pd).filter(function (f) {
        var v2 = f.toLocaleLowerCase();
        return v1 == v2;
      });
      return path.join(pd, fdd[0]);
    } catch (e) {
      utils.log("error reading dir in dirMatchCase:" + p);
    }
  }
  return p;
}
module.exports.dirMatchCase = dirMatchCase;

function mkDirs(dir, mode) {
  // from jake
  var dirPath = path.normalize(dir),
    paths = dirPath.split(/\/|\\/),
    currPath = "",
    next;

  if (paths[0] == "" || /^[A-Za-z]+:/.test(paths[0])) {
    currPath = paths.shift() || "/";
    currPath = path.join(currPath, paths.shift());
    //utils.log('basedir');
  }
  try {
    //utils.log('making ' + currPath);
    fs.mkdirSync(currPath, mode || 0755);
  } catch (e) {
    if (e.code != "EEXIST") {
      throw e;
    }
  }
  while ((next = paths.shift())) {
    if (next == "..") {
      currPath = path.join(currPath, next);
      continue;
    }
    currPath = path.join(currPath, next);
    try {
      //utils.log('making ' + currPath);
      fs.mkdirSync(currPath, mode || 0755);
    } catch (e) {
      if (e.code != "EEXIST") {
        throw e;
      }
    }
  }
}
module.exports.mkDirs = mkDirs;
