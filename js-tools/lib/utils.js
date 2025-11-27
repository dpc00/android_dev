var cproc = require("child_process");
var fs = require("fs");
var json = require("json");
var path = require("path");

function chop(txt) {
  var limit = 79;
  var mt = " ... ";
  if (txt.length > limit) {
    var b1 = 0;
    var e1 = limit / 2 - mt.length / 2;
    var b2 = txt.length - (limit / 2 - mt.length / 2);
    var e2 = txt.length;
    txt = txt.substring(b1, e1) + mt + txt.substring(b2, e2);
  }
  return txt;
}
module.exports.chop = chop;

var ccol = 0;
var cln = 0;

function writedata(data) {
  if (data.length > 0) {
    var hnl = false;
    var hret = false;
    var s = data.toString();
    console._stdout.write(s);
    if (s.indexOf("\r") > -1) {
      hret = true;
    }
    if (s.indexOf("\n") > -1) {
      hnl = true;
    }
    if (hret) {
      ccol = 0;
    } else {
      ccol += s.length;
    }
    if (hnl) {
      cln++;
    }
  }
}
module.exports.writedata = writedata;

function writedataindent(data) {
  if (data.length > 0) {
    var s = data.toString().split(/[\r\n]+/);
    s.filter(function (l) {
      return l.length > 0;
    }).forEach(function (l) {
      console._stdout.write("\t" + l + "\n");
      cln++;
      ccol = 0;
    });
  }
}
module.exports.writedataindent = writedataindent;

function eo(s1, s2) {
  var anl = false;
  if (s1) {
    writedataindent(s1);
    anl = true;
  }
  if (s2) {
    writedataindent(s2);
    anl = true;
  }
}
module.exports.eo = eo;

function log(s) {
  if (ccol > 0) writedata("\r\n");
  if (typeof s == "string") writedata(s);
  else if (typeof s == "number") writedata(s.toString());
}
module.exports.log = log;

function errlog(e) {
  log(e.toString());
}

function writedataindent(data) {
  if (data.length > 0) {
    var s = data.toString().split(/[\r\n]+/);
    s.filter(function (l) {
      return l.length > 0;
    }).forEach(function (l) {
      console._stdout.write("\t" + l + "\n");
      cln++;
      ccol = 0;
    });
  }
}
module.exports.writedataindent = writedataindent;

function dos2(cmd2, args) {
  var cmd = ["/c"];
  if (cmd2) cmd = cmd.concat(cmd2.split(" "));
  if (args) cmd = cmd.concat(args);
  var dc = cproc.spawnSync("cmd.exe", cmd, {
    encoding: "ascii",
  });
  var t1 = dc.stdout.toString();
  var t2 = dc.stderr.toString();
  if (t1.length > 0 || t2.length > 0) return [t1, t2];
  else return [];
}
module.exports.dos2 = dos2;

function showenv() {
  for (var k in process.env) {
    utils.log(k + " = " + process.env[k]);
  }
}
module.exports.showenv = showenv;

function jake_task(t) {
  var jake = require("jake");
  var args = ["--trace", "--jakefile", "jakefile.js", t];
  jake.run.apply(jake, args);
}
module.exports.jake_task = jake_task;

function jake_tasks(ta) {
  // if (typeof jake === 'undefined') {
  var jake = require("jake");
  // }
  var args = ["--trace", "--jakefile", "jakefile.js"].concat(ta);
  jake.run.apply(jake, args);
}
module.exports.jake_tasks = jake_tasks;

function whereProg(pbn) {
  var res = [];
  var cf = [];
  cf.push(json.readConfig(__dirname + "/plaunch_hd.json"));
  // cf.push(json.readConfig(__dirname + '/plaunch_flash_CODEn.json'));
  cf.push(json.readConfig(__dirname + "/plaunch_flash_CODE0.json"));

  cf.forEach(function (c) {
    for (var k in c.paths) {
      c.paths[k].files.forEach(function (f) {
        if (f.indexOf(pbn) != -1) res.push(k);
      });
    }
  });
  return res;
}
module.exports.whereProg = whereProg;

function makelinks() {
  var ps = [];
  var ns = [];

  for (var k in process.env) {
    var v = process.env[k];
    if (v.substring(0, 2) == "C:") {
      // utils.log(k + '=' + process.env[k]);
      ns.push(k);
      ps.push(v);
    }
  }
  const crlf = "\r\n";
  var s = "";
  ns.forEach(function (n, i, a) {
    s += ":" + n + crlf;
    s +=
      "rem %~d0\\Programs\\Utils\\Shortcut.exe /F:" +
      n +
      '.lnk /A:C /T:"%%' +
      n +
      '%%" /D:"Opens explorer in ' +
      n +
      '"' +
      crlf;
    // s +='rem echo \\plaunch explorer.exe %%' + n + '%% > explore_' + n + '.bat' + crlf;
    s += crlf;
  });
  require("fs").writeFileSync(
    __dirname.substring(0, 2) + "\\.bat\\makelinks.bat",
    s,
    {
      encoding: "ascii",
    }
  );
}
module.exports.makelinks = makelinks;

function prjDir(prj) {
  var s = "%FLASH0%\\Projects";
  if (prj && prj.length > 0) {
    s += "\\" + prj;
  }
  return expES(s);
}
module.exports.prjDir = prjDir;

function gitDir(prj) {
  return expES("%FLASH0%\\GitRepos\\" + prj);
}
module.exports.gitDir = gitDir;

var prjList = ["btest", "elm-test", "jakerun", "py-test", "tools", "Circuit"];
module.exports.prjList = prjList;

function expES(s) {
  // var str = '%LOCALAPPDATA%\\Google\\Chrome\\Application';
  var replaced = s.replace(/%([^%]+)%/gi, function (_, n) {
    return process.env[n];
  });
  return replaced;
}
module.exports.expES = expES;

function pfind(s1) {
  var s2 = s1.toLowerCase();
  sa = process.env.PATH.split(";");
  for (pe1 in sa) {
    var pe2 = pe1.toLowerCase();
    if (pe2.indexOf(s2) != -1) {
      log(pe1);
    }
  }
}
module.exports.pfind = pfind;

function pfind2() {
  pfind1(process.env.argv[0]);
}
module.exports.pfind2 = pfind2;
