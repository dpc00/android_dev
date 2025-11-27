var Dos4 = require("dos4");
var fcs = require("fcstats");
var fs = require("fs");
var path = require("path");
var utils = require("utils");

var constants = require("constants");

function lstat(p) {
  var p1 = new Promise(function (resolve, reject) {
    fs.lstat(p, function (err, stats) {
      if (err) {
        // debugger;
        reject(err);
      } else {
        resolve(stats);
      }
    });
  });
  return p1;
}
module.exports.lstat = lstat;

function checkStats(stats) {
  // var bits = {
  // 	'F_OK': constants['F_OK'],
  // 	'R_OK': constants['R_OK'],
  // 	'S_IFCHR': constants['S_IFCHR'],
  // 	'S_IFDIR': constants['S_IFDIR'],
  // 	'S_IFLNK': constants['S_IFLNK'],
  // 	'S_IFMT': constants['S_IFMT'],
  // 	'S_IFREG': constants['S_IFREG'],
  // 	'W_OK': constants['W_OK'],
  // 	'X_OK': constants['X_OK']
  // };

  // for (var k in bits) {
  // 	if ((constants[k] & stats.mode) != 0) {
  // 		utils.writedata(k + '(' + constants[k] + ') ');
  // 	}
  // }
  return (constants.R_OK & stats.mode) != 0;
}

function fixDT(source, target) {
  var p1 = lstat(source);
  var p2 = p1.then(function (stats) {
    var p3 = new Promise(function (resolve, reject) {
      fs.utimes(target, stats.atime, stats.mtime, function (err) {
        if (err) {
          reject(err);
        } else {
          resolve();
        }
      });
    });
    return p3;
  });
  return p2;
}

function cpf1(source, target) {
  return new Dos4({
    cmd: "cmd.exe",
    args: ["/c", "copy", source, target],
    echo: true,
    collect: false,
    print: false,
  });
}

function cpf2(source, target) {
  return new Promise(function (resolve, reject) {
    var s1 = fs.createReadStream(source);
    var s2 = fs.createWriteStream(target);
    s1.on("error", reject);
    s2.on("error", reject);
    s2.on("close", resolve);
    s1.pipe(s2);
  }).then(function () {
    return fixDT(source, target);
  });
}

function rmDir(f) {
  return new Promise(function (resolve, reject) {
    fs.rmdir(f, function (err) {
      if (err) {
        // debugger;
        return reject(err);
      } else {
        fcs.fcstats.ddel++;
        return resolve();
      }
    });
  });
}
module.exports.rmDir = rmDir;

function delFile(f) {
  return lstat(f)
    .then(function (stats) {
      return new Promise(function (resolve, reject) {
        fs.unlink(f, function (err) {
          if (err) {
            reject(err);
          } else {
            resolve();
          }
        });
      }).then(function () {
        fcs.fcstats.fdel++;
        fcs.fcstats.bdel += stats.size;
      });
    })
    .catch(function (reason) {
      if (typeof reason == "string") utils.log(reason);
      else if (typeof reason == "number") utils.log("errcode: " + reason);
      else if (typeof reason == "object") utils.log(reason.message);
    });
}
module.exports.delFile = delFile;

function copyFile(source, target) {
  return lstat(source)
    .then(function (stats) {
      return cpf1(source, target).then(function () {
        fcs.fcstats.fcpy++;
        fcs.fcstats.bcpy += stats.size;
      });
    })
    .catch(function (reason) {
      if (typeof reason == "string") utils.log(reason);
      else if (typeof reason == "number") utils.log("errcode: " + reason);
      else if (typeof reason == "object") utils.log(reason.message);
    });
}
module.exports.copyFile = copyFile;

function type(fn) {
  var fs = require("fs");
  var txt = fs.readFileSync(fn);
  writedata(txt);
}
module.exports.type = type;

function fileExists(fp) {
  return lstat(fp).then(
    function (stats) {
      return stats.isFile() && !stats.isSymbolicLink();
    },
    function (err) {
      if (err.code == "ENOENT") return Promise.resolve(false);
      else {
        return Promise.reject(err);
      }
    }
  );
}
module.exports.fileExists = fileExists;

function dirExists(fp) {
  return lstat(fp).then(
    function (stats) {
      return stats.isDirectory();
    },
    function (err) {
      if (err.code == "ENOENT") return false;
      else {
        return Promise.reject(err);
      }
    }
  );
}
module.exports.dirExists = dirExists;

function readDir(p) {
  return new Promise(function (resolve, reject) {
    fs.readdir(p, function (err, files) {
      if (err) {
        // debugger;
        reject(err);
      } else resolve(files);
    });
  });
}
module.exports.readDir = readDir;

function insert(fp, stats, memo) {
  if (!stats.isSymbolicLink()) {
    if (stats.isFile()) {
      memo.files.push({
        fp: fp,
        mtime: stats.mtime,
        size: stats.size,
      });
    } else {
      if (stats.isDirectory()) {
        memo.dirs.push({
          dp: fp,
          mtime: stats.mtime,
        });
      }
    }
  }
}

function dget(dp) {
  return readDir(dp)
    .then(function (dea) {
      return Promise.all(
        dea.map(function (fde) {
          var fdp = path.join(dp, fde);
          return lstat(fdp)
            .then(function (stats) {
              return {
                p: fdp,
                s: stats,
              };
            })
            .catch(function (reason) {
              if (typeof reason == "string") utils.log(reason);
              else if (typeof reason == "number")
                utils.log("errcode: " + reason);
              else if (typeof reason == "object") utils.log(reason.message);
              return {
                p: fdp,
                s: null,
              };
            });
        })
      );
    })
    .then(function (psa) {
      var memo = {
        p: dp,
        files: [],
        dirs: [],
      };
      psa.forEach(function (ps) {
        if (ps.s != null) insert(ps.p, ps.s, memo);
      });
      return Promise.resolve(memo);
    })
    .catch(function (reason) {
      if (typeof reason == "string") utils.log(reason);
      else if (typeof reason == "number") utils.log("errcode: " + reason);
      else if (typeof reason == "object") utils.log(reason.message);
      var memo = {
        p: dp,
        files: [],
        dirs: [],
      };
      return Promise.resolve(memo);
    });
}
module.exports.dget = dget;

function filesList(p, es) {
  function ematch(fd) {
    return (
      es.filter(function (e) {
        return fd.fp.endsWith(e);
      }).length > 0
    );
  }
  return dget(p).then(function (memo) {
    var pfiles = memo.files;
    if (es && es.length > 0) pfiles = pfiles.filter(ematch);
    return pfiles;
  });
}
module.exports.filesList = filesList;

function dirsList(p) {
  return dget(p).then(function (memo) {
    return memo.dirs;
  });
}
module.exports.dirsList = dirsList;
