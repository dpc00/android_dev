var cproc = require("child_process");
var utils = require("utils");

function Dos4(po) {
  self = this;
  self.args = Array();
  self.cmd = "";
  self.collect = false;
  self.detached = false;
  self.echo = false;
  self.outs = "";
  self.print = true;
  self.shell = false;
  self.stdio = ["pipe", "pipe", "pipe"];
  for (var k in po) {
    this[k] = po[k];
  }
  return new Promise(function (resolve, reject) {
    var rejected = false;
    var opts2 = {
      encoding: "ascii",
      detached: self.detached,
      shell: self.shell,
    };
    if (self.echo) {
      utils.log(utils.chop(self.cmd + " " + self.args.join(" ")));
    }
    var dc = cproc.spawn(self.cmd, self.args, opts2);
    dc.stdout.on("data", function (data) {
      if (self.collect) {
        self.outs += data.toString();
      }
      if (self.print) {
        utils.writedataindent(data);
      }
    });
    dc.stderr.on("data", function (data) {
      self.outs += data.toString();
      utils.writedataindent(data);
    });
    dc.on("error", function (err) {
      rejected = true;
      dc.stdin.end();
      reject(err.message + "\r\n" + self.outs);
    });
    // dc.on('exit', function() {
    //     if (!rejected) {
    //         resolve(self.outs);
    //     }
    // });
    // dc.on('end', function() {
    //     if (!rejected) {
    //         resolve(self.outs);
    //     }
    // });
    dc.on("close", function (code) {
      if (!rejected) {
        if (code == 0) {
          dc.stdin.end();
          resolve(self.outs);
        } else {
          rejected = true;
          dc.stdin.end();
          reject("dos err: " + code);
        }
      }
    });
  });
}
module.exports = Dos4;
//# sourceMappingURL=Dos4.js.map
