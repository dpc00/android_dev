/// <reference path='../typings/main.d.ts'/>


var cp = require("child_process");
var diskutils = require("diskutils");
var Dos4 = require("dos4");
var fs = require("fs");
var utils = require("utils");

class GitRepo {
  constructor(props) {
    this.wt = "";
    this.gd = "";
    for (var k in props) {
      this[k] = props[k];
    }
  }
  gitcmd(args, opts) {
    var opts2 = {
      cmd: "git.exe",
      args: ["--work-tree=" + this.wt, "--git-dir=" + this.gd].concat(args),
      collect: false,
      echo: false,
      print: false,
    };
    ["collect", "echo", "print"].forEach(function (k) {
      if (typeof opts[k] != undefined) opts2[k] = opts[k];
    });
    return new Dos4(opts2);
  }
  dil() {
    utils.log("delete index lock " + this.wt + ", " + this.gd);
    var fn = this.gd + "\\index.lock"; //
    var p1 = diskutils.fileExists(fn);
    var p2 = p1.then(function (fe) {
      if (!fe) return Promise.resolve();
      var p3 = new Promise(function (resolve, reject) {
        fs.unlink(fn, function (err) {
          if (err) reject(err);
          else {
            utils.log("unlinked " + fn);
            resolve();
          }
        });
      });
      return p3;
    });
    return p2;
  }
  status() {
    utils.log("git status " + this.wt + ", " + this.gd);
    var p1 = this.gitcmd(["status", "--porcelain", "--untracked-files=all"], {
      echo: false,
      collect: true,
      print: true,
    });
    var p2 = p1.then(function (s) {
      return s
        .split("\n")
        .filter(function (fn) {
          return fn.length > 0;
        })
        .map(function (e) {
          return e.substring(3);
        });
    });
    return p2;
  }
  add(sa) {
    utils.log("git add " + this.wt + ", " + this.gd);
    var self = this;
    var p1 = self.gitcmd(["add"].concat(sa), {
      echo: false,
      collect: false,
      print: true,
    });
    var p2 = p1.catch(function (reason) {
      utils.log(reason);
      var p3 = sa.map(function (f) {
        var p4 = self
          .gitcmd(["add", f], {
            echo: false,
            collect: false,
            print: true,
          })
          .catch(function (reason) {
            utils.log(reason);
          });
        return p4;
      });
      return Promise.all(p3);
    });
    return p2;
  }
  commit() {
    utils.log("git commit " + this.wt + ", " + this.gd);
    var p1 = this.gitcmd(["commit", "-a", "-m", "'abcde'"], {
      echo: false,
      collect: false,
      print: true,
    });
    return p1;
  }
  push() {
    utils.log("git push " + this.wt + ", " + this.gd);
    var p1 = this.gitcmd(["push", "origin", "master"], {
      echo: false,
      collect: false,
      print: true,
    });
    return p1;
  }
  backup() {
    var self = this;
    var p1 = self.dil();
    var p2 = p1.then(function () {
      return self.status();
    });
    var p3 = p2.then(function (sa) {
      if (sa.length > 0) {
        return self.add(sa);
      } else return Promise.reject("git status returns no files");
    });
    var p4 = p3.then(function () {
      return self.commit();
    });
    var p5 = p4.then(function () {
      return self.push();
    });
    var p6 = p5.catch(function (err) {
      if (err) utils.log(err);
    });
    return p6;
  }
}
exports.GitRepo = GitRepo;
//# sourceMappingURL=GitRepo.js.map
